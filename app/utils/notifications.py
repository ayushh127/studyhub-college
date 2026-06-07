from flask import url_for
from app.extensions import db

def create_notification(college_id, subject_id, unit_id, notification_type, title, message, link, created_by):
    """
    Creates a Notification record in the database.
    """
    from app.models import Notification
    notification = Notification(
        college_id=college_id,
        subject_id=subject_id,
        unit_id=unit_id,
        notification_type=notification_type,
        title=title,
        message=message,
        link=link,
        created_by=created_by
    )
    db.session.add(notification)
    db.session.commit()
    return notification

def notify_material_published(material):
    """
    Triggers an in-app notification when a study material is published.
    """
    subject = material.subject
    unit = material.unit
    
    # E.g., "DBMS Unit 2: Normalization Notes is now available."
    if unit:
        message = f"{subject.name} Unit {unit.unit_number}: {material.title} is now available."
    else:
        message = f"{subject.name}: {material.title} is now available."
        
    link = url_for('student.material_details', id=material.id)
    
    return create_notification(
        college_id=material.college_id,
        subject_id=material.subject_id,
        unit_id=material.unit_id,
        notification_type='material',
        title="New study material uploaded",
        message=message,
        link=link,
        created_by=material.uploaded_by
    )

def notify_pyq_published(pyq):
    """
    Triggers an in-app notification when a PYQ paper is published.
    """
    subject = pyq.subject
    
    # E.g., "DBMS 2024 End Sem PYQ is now available."
    message = f"{subject.name} {pyq.title} is now available."
    link = url_for('student.pyq_details', id=pyq.id)
    
    return create_notification(
        college_id=pyq.college_id,
        subject_id=pyq.subject_id,
        unit_id=pyq.unit_id,
        notification_type='pyq',
        title="New PYQ uploaded",
        message=message,
        link=link,
        created_by=pyq.uploaded_by
    )

def notify_quiz_published(quiz):
    """
    Triggers an in-app notification when a quiz is published.
    """
    subject = quiz.subject
    
    # E.g., "DBMS Unit 2 Practice Quiz is now available."
    message = f"{subject.name} {quiz.title} is now available."
    link = url_for('student.start_quiz', id=quiz.id)
    
    return create_notification(
        college_id=quiz.college_id,
        subject_id=quiz.subject_id,
        unit_id=quiz.unit_id,
        notification_type='quiz',
        title="New quiz published",
        message=message,
        link=link,
        created_by=quiz.created_by
    )
