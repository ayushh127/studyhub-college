from flask import request
from ..extensions import db
from ..models import AuditLog
from flask_login import current_user

def log_action(actor_id, action, target_type, target_id=None, details=None):
    """
    Helper function to record an action in the audit log.
    """
    ip_address = request.remote_addr if request else None
    
    log = AuditLog(
        actor_user_id=actor_id,
        action=action,
        target_type=target_type,
        target_id=target_id,
        details=details,
        ip_address=ip_address
    )
    db.session.add(log)
    db.session.commit()
