from flask import render_template, redirect, url_for, flash, request, session
from flask_login import current_user
from . import admin_bp
from ..models import User, College, CollegeRequest, AuditLog, Subject, CommunityMaterial, CommunityMaterialReport
from ..extensions import db
from ..utils.decorators import admin_required
from ..utils.audit import log_action

@admin_bp.before_request
@admin_required
def before_request():
    pass

@admin_bp.route('/dashboard')
def dashboard():
    stats = {
        'users': User.query.count(),
        'colleges': College.query.count(),
        'pending_requests': CollegeRequest.query.filter_by(status='pending').count()
    }
    return render_template('admin/dashboard.html', stats=stats)

@admin_bp.route('/college-requests')
def college_requests():
    requests = CollegeRequest.query.order_by(CollegeRequest.created_at.desc()).all()
    return render_template('admin/college_requests.html', requests=requests)

@admin_bp.route('/college-requests/<int:id>/approve', methods=['POST'])
def approve_college_request(id):
    req = CollegeRequest.query.get_or_404(id)
    if req.status != 'pending':
        flash('Request already processed.', 'warning')
        return redirect(url_for('admin.college_requests'))
        
    req.status = 'approved'
    req.reviewed_by_admin_id = current_user.id
    
    # Create College
    college = College(
        name=req.college_name,
        code=req.college_code.upper(),
        city=req.city,
        state=req.state,
        address=req.address,
        contact_email=req.admin_email,
        contact_phone=req.admin_phone,
        status='active',
        logo_path=req.logo_path,
        created_by_admin_id=current_user.id
    )
    db.session.add(college)
    db.session.commit() # Commit to get college id
    
    # Create College Admin
    admin_user = User(
        full_name=req.admin_full_name,
        email=req.admin_email,
        role='college_admin',
        college_id=college.id
    )
    if req.admin_password_hash:
        admin_user.password_hash = req.admin_password_hash
    else:
        admin_user.set_password('admin123') # Fallback for old requests
    db.session.add(admin_user)
    db.session.commit()
    
    log_action(current_user.id, 'college_approved', 'college_request', req.id, f'Approved college {college.name}')
    flash(f'College {college.name} approved successfully. Admin account created.', 'success')
    return redirect(url_for('admin.college_requests'))

@admin_bp.route('/college-requests/<int:id>/reject', methods=['POST'])
def reject_college_request(id):
    req = CollegeRequest.query.get_or_404(id)
    req.status = 'rejected'
    req.reviewed_by_admin_id = current_user.id
    db.session.commit()
    log_action(current_user.id, 'college_rejected', 'college_request', req.id)
    flash('College request rejected.', 'success')
    return redirect(url_for('admin.college_requests'))

@admin_bp.route('/users')
def users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/users/<int:id>/impersonate', methods=['POST'])
def impersonate(id):
    # Do not allow impersonating another platform admin unless needed, for now just allow any for support.
    target_user = User.query.get_or_404(id)
    if target_user.role == 'platform_admin':
        flash('Cannot impersonate another platform admin.', 'danger')
        return redirect(url_for('admin.users'))
        
    session['original_admin_id'] = current_user.id
    session['impersonated_user_id'] = target_user.id
    
    log_action(current_user.id, 'impersonation_started', 'user', target_user.id)
    flash(f'You are now impersonating {target_user.full_name}.', 'warning')
    
    if target_user.role == 'college_admin':
        return redirect(url_for('college_admin.dashboard'))
    return redirect(url_for('student.dashboard'))

@admin_bp.route('/impersonation/exit')
def exit_impersonation():
    original_id = session.pop('original_admin_id', None)
    impersonated_id = session.pop('impersonated_user_id', None)
    
    if original_id:
        log_action(original_id, 'impersonation_ended', 'user', impersonated_id)
        
    flash('Exited impersonation mode.', 'info')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/audit-logs')
def audit_logs():
    logs = AuditLog.query.order_by(AuditLog.created_at.desc()).limit(100).all()
    return render_template('admin/audit_logs.html', logs=logs)

@admin_bp.route('/users/create-platform-admin', methods=['GET', 'POST'])
def create_platform_admin():
    if current_user.role != 'platform_admin':
        flash('Only platform admins can create other platform admins.', 'danger')
        return redirect(url_for('admin.users'))

    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not all([full_name, email, password, confirm_password]):
            flash('All fields are required.', 'danger')
            return render_template('admin/create_platform_admin.html')

        if User.query.filter_by(email=email).first():
            flash('Email already in use.', 'danger')
            return render_template('admin/create_platform_admin.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return render_template('admin/create_platform_admin.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('admin/create_platform_admin.html')

        new_admin = User(
            full_name=full_name,
            email=email,
            role='platform_admin',
            is_active=True
        )
        new_admin.set_password(password)
        db.session.add(new_admin)
        db.session.commit()

        log_action(current_user.id, 'platform_admin_created', 'user', new_admin.id, f'Created platform admin {email}')
        flash(f'Platform admin {full_name} created successfully.', 'success')
        return redirect(url_for('admin.users'))

    return render_template('admin/create_platform_admin.html')

@admin_bp.route('/colleges')
def colleges():
    colleges_list = College.query.order_by(College.name.asc()).all()
    return render_template('admin/colleges.html', colleges=colleges_list)

@admin_bp.route('/colleges/create', methods=['GET', 'POST'])
def create_college():
    if request.method == 'POST':
        name = request.form.get('name')
        code = request.form.get('code')
        city = request.form.get('city')
        state = request.form.get('state')
        address = request.form.get('address')
        contact_email = request.form.get('contact_email')
        contact_phone = request.form.get('contact_phone')
        status = request.form.get('status', 'active')
        
        # Validation
        if not all([name, code, city, state, address, contact_email, contact_phone]):
            flash('All fields are required.', 'danger')
            return render_template('admin/college_form.html', college=None)
            
        existing = College.query.filter_by(code=code.upper()).first()
        if existing:
            flash(f'College code "{code}" already exists. Please choose a unique code.', 'danger')
            return render_template('admin/college_form.html', college=None, form_data=request.form)
            
        logo = request.files.get('logo')
        logo_filename = None
        if logo and logo.filename != '':
            if not ('.' in logo.filename and logo.filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'webp'}):
                flash('Invalid logo file type. Allowed formats: PNG, JPG, JPEG, WEBP.', 'danger')
                return render_template('admin/college_form.html', college=None, form_data=request.form)
            
            import os
            logo.seek(0, os.SEEK_END)
            size = logo.tell()
            logo.seek(0)
            if size > 2 * 1024 * 1024:
                flash('Logo file size must be less than 2MB.', 'danger')
                return render_template('admin/college_form.html', college=None, form_data=request.form)
            
            from werkzeug.utils import secure_filename
            from flask import current_app
            import time
            ext = logo.filename.rsplit('.', 1)[1].lower()
            logo_filename = secure_filename(f"logo_{code.upper()}_{int(time.time())}.{ext}")
            logo.save(os.path.join(current_app.config['UPLOAD_FOLDER_LOGOS'], logo_filename))

        college = College(
            name=name,
            code=code.upper(),
            city=city,
            state=state,
            address=address,
            contact_email=contact_email,
            contact_phone=contact_phone,
            status=status,
            logo_path=logo_filename,
            created_by_admin_id=current_user.id
        )
        db.session.add(college)
        db.session.commit()
        
        # Create default College Admin for this college
        admin_user = User(
            full_name=f"Admin {name}",
            email=contact_email,
            role='college_admin',
            college_id=college.id
        )
        admin_user.set_password('admin123')
        db.session.add(admin_user)
        db.session.commit()
        
        log_action(current_user.id, 'college_created_manually', 'college', college.id, f'Manually created college {college.name} with default admin.')
        flash(f'College {college.name} created successfully. Default admin account ({contact_email}) created with password "admin123".', 'success')
        return redirect(url_for('admin.college_detail', id=college.id))
        
    return render_template('admin/college_form.html', college=None)

@admin_bp.route('/colleges/<int:id>/edit', methods=['GET', 'POST'])
def edit_college(id):
    import os
    import time
    from flask import current_app
    from werkzeug.utils import secure_filename
    
    college = College.query.get_or_404(id)
    
    if request.method == 'POST':
        name = request.form.get('name')
        code = request.form.get('code')
        city = request.form.get('city')
        state = request.form.get('state')
        address = request.form.get('address')
        contact_email = request.form.get('contact_email')
        contact_phone = request.form.get('contact_phone')
        status = request.form.get('status', 'active')
        
        # Validation
        if not all([name, code, city, state, address, contact_email, contact_phone]):
            flash('All fields are required.', 'danger')
            return render_template('admin/college_form.html', college=college)
            
        existing = College.query.filter_by(code=code.upper()).first()
        if existing and existing.id != college.id:
            flash(f'College code "{code}" already exists. Please choose a unique code.', 'danger')
            return render_template('admin/college_form.html', college=college)
            
        logo = request.files.get('logo')
        logo_filename = college.logo_path
        logo_updated = False
        if logo and logo.filename != '':
            if not ('.' in logo.filename and logo.filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'webp'}):
                flash('Invalid logo file type. Allowed formats: PNG, JPG, JPEG, WEBP.', 'danger')
                return render_template('admin/college_form.html', college=college)
            
            logo.seek(0, os.SEEK_END)
            size = logo.tell()
            logo.seek(0)
            if size > 2 * 1024 * 1024:
                flash('Logo file size must be less than 2MB.', 'danger')
                return render_template('admin/college_form.html', college=college)
                
            # Delete old logo if exists
            if college.logo_path:
                old_path = os.path.join(current_app.config['UPLOAD_FOLDER_LOGOS'], college.logo_path)
                if os.path.exists(old_path):
                    try:
                        os.remove(old_path)
                    except Exception:
                        pass
                        
            ext = logo.filename.rsplit('.', 1)[1].lower()
            logo_filename = secure_filename(f"logo_{code.upper()}_{int(time.time())}.{ext}")
            logo.save(os.path.join(current_app.config['UPLOAD_FOLDER_LOGOS'], logo_filename))
            logo_updated = True
            
        # Update details
        college.name = name
        college.code = code.upper()
        college.city = city
        college.state = state
        college.address = address
        college.contact_email = contact_email
        college.contact_phone = contact_phone
        college.status = status
        college.logo_path = logo_filename
        
        db.session.commit()
        
        log_action(current_user.id, 'college_updated', 'college', college.id, f'Updated details for college {college.name}')
        if logo_updated:
            log_action(current_user.id, 'college_logo_updated', 'college', college.id, f'Updated logo for college {college.name}')
            
        flash(f'College {college.name} updated successfully.', 'success')
        return redirect(url_for('admin.college_detail', id=college.id))
        
    return render_template('admin/college_form.html', college=college)

@admin_bp.route('/colleges/<int:id>/logo', methods=['POST'])
def upload_college_logo(id):
    import os
    import time
    from flask import current_app
    from werkzeug.utils import secure_filename
    
    college = College.query.get_or_404(id)
    logo = request.files.get('logo')
    
    if not logo or logo.filename == '':
        flash('No logo file selected.', 'danger')
        return redirect(url_for('admin.college_detail', id=college.id))
        
    if not ('.' in logo.filename and logo.filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'webp'}):
        flash('Invalid logo file type. Allowed formats: PNG, JPG, JPEG, WEBP.', 'danger')
        return redirect(url_for('admin.college_detail', id=college.id))
        
    logo.seek(0, os.SEEK_END)
    size = logo.tell()
    logo.seek(0)
    if size > 2 * 1024 * 1024:
        flash('Logo file size must be less than 2MB.', 'danger')
        return redirect(url_for('admin.college_detail', id=college.id))
        
    # Delete old logo if exists
    if college.logo_path:
        old_path = os.path.join(current_app.config['UPLOAD_FOLDER_LOGOS'], college.logo_path)
        if os.path.exists(old_path):
            try:
                os.remove(old_path)
            except Exception as e:
                pass
                
    ext = logo.filename.rsplit('.', 1)[1].lower()
    logo_filename = secure_filename(f"logo_{college.code}_{int(time.time())}.{ext}")
    logo.save(os.path.join(current_app.config['UPLOAD_FOLDER_LOGOS'], logo_filename))
    
    college.logo_path = logo_filename
    db.session.commit()
    
    log_action(current_user.id, 'college_logo_updated', 'college', college.id, f"Uploaded logo '{logo_filename}' for college {college.name}")
    flash('College logo updated successfully.', 'success')
    return redirect(url_for('admin.college_detail', id=college.id))

@admin_bp.route('/colleges/<int:id>/logo/remove', methods=['POST'])
def remove_college_logo(id):
    import os
    from flask import current_app
    
    college = College.query.get_or_404(id)
    if college.logo_path:
        old_path = os.path.join(current_app.config['UPLOAD_FOLDER_LOGOS'], college.logo_path)
        if os.path.exists(old_path):
            try:
                os.remove(old_path)
            except Exception as e:
                pass
        
        college.logo_path = None
        db.session.commit()
        log_action(current_user.id, 'college_logo_removed', 'college', college.id, f"Removed logo for college {college.name}")
        flash('College logo removed successfully.', 'success')
    else:
        flash('No logo exists for this college.', 'warning')
        
    return redirect(url_for('admin.college_detail', id=college.id))

@admin_bp.route('/colleges/<int:id>')
def college_detail(id):
    college = College.query.get_or_404(id)
    subject_count = Subject.query.filter_by(college_id=college.id).count()
    student_count = User.query.filter_by(college_id=college.id, role='student').count()
    admin_count = User.query.filter_by(college_id=college.id, role='college_admin').count()
    college_admins = User.query.filter_by(college_id=college.id, role='college_admin').all()
    
    return render_template('admin/college_details.html', 
                           college=college, 
                           subject_count=subject_count, 
                           student_count=student_count, 
                           admin_count=admin_count,
                           college_admins=college_admins)

@admin_bp.route('/colleges/<int:id>/admins/create', methods=['GET', 'POST'])
def create_college_admin(id):
    college = College.query.get_or_404(id)
    
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone = request.form.get('phone') # Optional
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not all([full_name, email, password, confirm_password]):
            flash('All required fields must be filled.', 'danger')
            return render_template('admin/create_college_admin.html', college=college)
            
        if User.query.filter_by(email=email).first():
            flash('Email already in use.', 'danger')
            return render_template('admin/create_college_admin.html', college=college)
            
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return render_template('admin/create_college_admin.html', college=college)
            
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('admin/create_college_admin.html', college=college)
            
        new_admin = User(
            full_name=full_name,
            email=email,
            role='college_admin',
            college_id=college.id,
            is_active=True
        )
        new_admin.set_password(password)
        db.session.add(new_admin)
        db.session.commit()
        
        log_action(current_user.id, 'college_admin_created', 'user', new_admin.id, f'Created college admin {email} for college {college.name}')
        flash(f'College admin {full_name} created successfully.', 'success')
        return redirect(url_for('admin.college_detail', id=college.id))
        
    return render_template('admin/create_college_admin.html', college=college)

@admin_bp.route('/colleges/<int:id>/activate', methods=['POST'])
def activate_college(id):
    college = College.query.get_or_404(id)
    college.status = 'active'
    db.session.commit()
    log_action(current_user.id, 'college_activated', 'college', college.id, f'Activated college {college.name}')
    flash(f'College {college.name} activated.', 'success')
    return redirect(url_for('admin.college_detail', id=college.id))

@admin_bp.route('/colleges/<int:id>/deactivate', methods=['POST'])
def deactivate_college(id):
    college = College.query.get_or_404(id)
    college.status = 'inactive'
    db.session.commit()
    log_action(current_user.id, 'college_deactivated', 'college', college.id, f'Deactivated college {college.name}')
    flash(f'College {college.name} deactivated.', 'success')
    return redirect(url_for('admin.college_detail', id=college.id))

@admin_bp.route('/settings')
def settings():
    return render_template('admin/settings.html')

@admin_bp.route('/community')
def community_list():
    status_filter = request.args.get('status')
    material_type = request.args.get('material_type')
    subject_name = request.args.get('subject_name')
    college_tag_id = request.args.get('college_tag_id', type=int)
    sort_by = request.args.get('sort', 'latest')

    query = CommunityMaterial.query

    if status_filter:
        query = query.filter_by(status=status_filter)
    if material_type:
        query = query.filter_by(material_type=material_type)
    if subject_name:
        query = query.filter(CommunityMaterial.subject_name.ilike(f'%{subject_name}%'))
    if college_tag_id:
        query = query.filter_by(college_tag_id=college_tag_id)

    if sort_by == 'reported':
        query = query.order_by(CommunityMaterial.reports_count.desc())
    elif sort_by == 'score':
        query = query.order_by(CommunityMaterial.moderation_score.desc())
    else:
        query = query.order_by(CommunityMaterial.created_at.desc())

    materials = query.all()
    colleges = College.query.all()
    
    return render_template('admin/community_list.html', materials=materials, colleges=colleges,
                           current_status=status_filter, current_type=material_type, 
                           current_subject=subject_name, current_college=college_tag_id, current_sort=sort_by)

@admin_bp.route('/community/queue')
def community_queue():
    materials = CommunityMaterial.query.filter_by(status='under_review').order_by(CommunityMaterial.moderation_score.desc()).all()
    return render_template('admin/community_queue.html', materials=materials)

@admin_bp.route('/community/reports/<int:id>')
def community_reports(id):
    material = CommunityMaterial.query.get_or_404(id)
    reports = CommunityMaterialReport.query.filter_by(material_id=material.id).order_by(CommunityMaterialReport.created_at.desc()).all()
    return render_template('admin/community_reports.html', material=material, reports=reports)

@admin_bp.route('/community/materials/<int:id>/hide', methods=['POST'])
def hide_community_material(id):
    material = CommunityMaterial.query.get_or_404(id)
    material.status = 'hidden'
    db.session.commit()
    log_action(current_user.id, 'community_material_hidden', 'community_material', material.id, f'Hidden community material {material.title}')
    flash(f'Material "{material.title}" is now hidden.', 'success')
    return redirect(request.referrer or url_for('admin.community_queue'))

@admin_bp.route('/community/materials/<int:id>/restore', methods=['POST'])
def restore_community_material(id):
    material = CommunityMaterial.query.get_or_404(id)
    material.status = 'active'
    # Optional: Reset moderation score so it doesn't immediately get flagged again
    material.moderation_score = 0.0
    db.session.commit()
    log_action(current_user.id, 'community_material_restored', 'community_material', material.id, f'Restored community material {material.title}')
    flash(f'Material "{material.title}" has been restored to active status.', 'success')
    return redirect(request.referrer or url_for('admin.community_queue'))

@admin_bp.route('/community/materials/<int:id>/remove', methods=['POST'])
def remove_community_material(id):
    material = CommunityMaterial.query.get_or_404(id)
    material.status = 'removed'
    db.session.commit()
    log_action(current_user.id, 'community_material_removed', 'community_material', material.id, f'Removed community material {material.title}')
    flash(f'Material "{material.title}" has been permanently removed.', 'danger')
    return redirect(request.referrer or url_for('admin.community_queue'))
