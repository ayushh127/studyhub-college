from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash
from . import auth_bp
from ..models import User, College
from ..extensions import db
from urllib.parse import urlsplit

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role == 'platform_admin':
            return redirect(url_for('admin.dashboard'))
        elif current_user.role == 'college_admin':
            return redirect(url_for('college_admin.dashboard'))
        else:
            return redirect(url_for('student.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            if not user.is_active:
                flash('Your account has been deactivated. Please contact an administrator.', 'danger')
                return render_template('auth/login.html')
                
            login_user(user)
            
            # Record login in audit log (simplified for now)
            from ..utils.audit import log_action
            log_action(user.id, 'login', 'user', user.id, 'User logged in')
            
            next_page = request.args.get('next')
            if not next_page or urlsplit(next_page).netloc != '':
                if user.role == 'platform_admin':
                    next_page = url_for('admin.dashboard')
                elif user.role == 'college_admin':
                    next_page = url_for('college_admin.dashboard')
                else:
                    next_page = url_for('student.dashboard')
            return redirect(next_page)
        
        flash('Invalid email or password', 'danger')
        
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('student.dashboard'))
        
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'warning')
            return redirect(url_for('auth.register'))
            
        new_user = User(
            full_name=full_name,
            email=email,
            role='student'
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        from ..utils.audit import log_action
        log_action(new_user.id, 'user_registered', 'user', new_user.id, 'New student registered')
        
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    # If in impersonation mode, maybe just exit impersonation instead of total logout?
    # Actually, we should just clear session.
    if 'impersonated_user_id' in session:
        session.pop('impersonated_user_id', None)
        session.pop('original_admin_id', None)
        
    if current_user.is_authenticated:
        from ..utils.audit import log_action
        log_action(current_user.id, 'logout', 'user', current_user.id, 'User logged out')
        logout_user()
        
    flash('You have been logged out.', 'info')
    return redirect(url_for('public.index'))

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    return render_template('auth/forgot_password.html')
