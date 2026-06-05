from flask import Blueprint

public_bp = Blueprint('public', __name__)
auth_bp = Blueprint('auth', __name__)
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
college_admin_bp = Blueprint('college_admin', __name__, url_prefix='/college-admin')
student_bp = Blueprint('student', __name__, url_prefix='/student')
files_bp = Blueprint('files', __name__, url_prefix='/files')

def register_blueprints(app):
    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(college_admin_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(files_bp)

# Import routes so they are registered on the blueprints
from . import public, auth, admin, college_admin, student, files
