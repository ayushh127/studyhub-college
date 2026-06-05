from flask import render_template
from . import public_bp

@public_bp.route('/')
def index():
    return render_template('public/index.html')

@public_bp.route('/about')
def about():
    return render_template('public/about.html')

@public_bp.route('/college/register', methods=['GET', 'POST'])
def college_register():
    from flask import request, redirect, url_for, flash
    from werkzeug.security import generate_password_hash
    from ..models import CollegeRequest
    from ..extensions import db

    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password and len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return redirect(url_for('public.college_register'))
            
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('public.college_register'))

        new_req = CollegeRequest(
            college_name=request.form.get('college_name'),
            college_code=request.form.get('college_code'),
            city=request.form.get('city'),
            state=request.form.get('state'),
            address=request.form.get('address'),
            admin_full_name=request.form.get('admin_full_name'),
            admin_email=request.form.get('admin_email'),
            admin_phone=request.form.get('admin_phone'),
            message=request.form.get('message'),
            admin_password_hash=generate_password_hash(password) if password else None
        )
        db.session.add(new_req)
        db.session.commit()
        
        return redirect(url_for('public.college_request_success'))
    return render_template('public/college_register.html')

@public_bp.route('/college/request-success')
def college_request_success():
    return render_template('public/college_request_success.html')

@public_bp.app_errorhandler(403)
def forbidden_error(error):
    return render_template('errors/403.html'), 403

@public_bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@public_bp.app_errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500

