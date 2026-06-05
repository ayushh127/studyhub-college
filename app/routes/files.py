import os
from flask import send_from_directory, abort, current_app
from flask_login import login_required, current_user
from . import files_bp
from ..models import StudyMaterial, PYQPaper
from ..utils.audit import log_action

@files_bp.route('/materials/<int:id>')
@login_required
def serve_material(id):
    material = StudyMaterial.query.get_or_404(id)
    
    # Ownership/Access check
    if current_user.role == 'platform_admin':
        pass
    elif current_user.role == 'college_admin':
        if current_user.college_id != material.college_id:
            abort(403)
    elif current_user.role == 'student':
        if current_user.college_id != material.college_id:
            abort(403)
        if not material.is_published:
            abort(403)
    else:
        abort(403)
        
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER_MATERIALS'], material.file_path)
    if not os.path.exists(filepath):
        log_action(current_user.id, 'file_missing_on_disk', 'study_material', material.id, f"File {material.file_path} is missing from materials folder on disk.")
        abort(404, description="Requested Study Material PDF file was not found on the server.")
        
    return send_from_directory(current_app.config['UPLOAD_FOLDER_MATERIALS'], material.file_path)

@files_bp.route('/pyqs/<int:id>')
@login_required
def serve_pyq(id):
    pyq = PYQPaper.query.get_or_404(id)
    
    # Ownership/Access check
    if current_user.role == 'platform_admin':
        pass
    elif current_user.role == 'college_admin':
        if current_user.college_id != pyq.college_id:
            abort(403)
    elif current_user.role == 'student':
        if current_user.college_id != pyq.college_id:
            abort(403)
        if not pyq.is_published:
            abort(403)
    else:
        abort(403)
        
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER_PYQS'], pyq.file_path)
    if not os.path.exists(filepath):
        log_action(current_user.id, 'file_missing_on_disk', 'pyq_paper', pyq.id, f"File {pyq.file_path} is missing from pyqs folder on disk.")
        abort(404, description="Requested PYQ Paper PDF file was not found on the server.")
        
    return send_from_directory(current_app.config['UPLOAD_FOLDER_PYQS'], pyq.file_path)
