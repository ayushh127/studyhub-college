from functools import wraps
from flask import abort, session
from flask_login import current_user

def role_required(*roles):
    """
    Decorator to restrict access to users with specific roles.
    Example: @role_required('platform_admin', 'college_admin')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            
            # Allow platform_admin if they are impersonating someone else?
            # Usually impersonation means they have the role of the person they impersonate.
            # But they might still want to access admin routes if they are in impersonation mode? 
            # It's better they exit impersonation.
            # We'll just check current_user.role since we will load the impersonated user via user_loader.
            
            if current_user.role not in roles:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    return role_required('platform_admin')(f)

def college_admin_required(f):
    return role_required('college_admin', 'platform_admin')(f)

def student_required(f):
    return role_required('student', 'platform_admin')(f)
