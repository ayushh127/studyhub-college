import os

basedir = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.dirname(basedir)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-studyhub-secret-key-123'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(parent_dir, 'instance', 'studyhub.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File uploads configuration
    UPLOAD_FOLDER_BASE = os.path.join(parent_dir, 'uploads')
    UPLOAD_FOLDER_MATERIALS = os.path.join(UPLOAD_FOLDER_BASE, 'materials')
    UPLOAD_FOLDER_PYQS = os.path.join(UPLOAD_FOLDER_BASE, 'pyqs')
    UPLOAD_FOLDER_COMMUNITY = os.path.join(UPLOAD_FOLDER_BASE, 'community')
    UPLOAD_FOLDER_LOGOS = os.path.join(UPLOAD_FOLDER_BASE, 'college_logos')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB max upload for free-tier testing
