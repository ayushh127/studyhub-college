from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    from flask import session
    from .models import User
    
    # Check if we are impersonating someone
    if 'impersonated_user_id' in session:
        return User.query.get(int(session['impersonated_user_id']))
        
    return User.query.get(int(user_id))
