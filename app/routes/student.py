from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, current_app
from flask_login import login_required, current_user
from app.models import User, College, Subject, Unit, StudyMaterial, PYQPaper, Quiz, QuizAttempt, Question, QuestionOption, AnswerSubmission, StudentProgress, SubjectSubscription, Notification, NotificationRead, CommunityMaterial, CommunityMaterialLike, CommunityMaterialRating, CommunityMaterialReport, CommunityMaterialView
from app.extensions import db
from sqlalchemy import or_
from datetime import datetime
from functools import wraps
import os
import time
from werkzeug.utils import secure_filename
from ..utils.audit import log_action
from ..utils.community import update_community_material_moderation

from . import student_bp

def student_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != 'student' and current_user.role != 'platform_admin':
            flash('Access denied. Student only.', 'danger')
            return redirect(url_for('public.index'))
        return f(*args, **kwargs)
    return decorated_function

def check_college_access(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.college_id:
            flash('Please select your college first.', 'warning')
            return redirect(url_for('student.select_college'))
        return f(*args, **kwargs)
    return decorated_function

@student_bp.before_request
@login_required
@student_required
def before_request():
    pass

@student_bp.route('/select-college', methods=['GET', 'POST'])
def select_college():
    if request.method == 'POST':
        college_id = request.form.get('college_id', type=int)
        college = College.query.filter_by(id=college_id, status='active').first()
        if college:
            current_user.college_id = college.id
            db.session.commit()
            flash(f'College selected: {college.name}', 'success')
            return redirect(url_for('student.dashboard'))
        flash('Invalid college selected.', 'danger')
        
    colleges = College.query.filter_by(status='active').all()
    return render_template('student/select_college.html', colleges=colleges)

@student_bp.route('/dashboard')
@check_college_access
def dashboard():
    subscribed_subject_ids = [sub.subject_id for sub in current_user.subscriptions]
    if subscribed_subject_ids:
        subjects = Subject.query.filter(Subject.id.in_(subscribed_subject_ids), Subject.is_active==True, Subject.college_id==current_user.college_id).all()
    else:
        subjects = []
    recent_quizzes = Quiz.query.filter_by(college_id=current_user.college_id, is_published=True).order_by(Quiz.created_at.desc()).limit(5).all()
    return render_template('student/dashboard.html', subjects=subjects, recent_quizzes=recent_quizzes)

@student_bp.route('/quizzes')
@check_college_access
def quizzes():
    quizzes = Quiz.query.filter_by(college_id=current_user.college_id, is_published=True).all()
    return render_template('student/quizzes.html', quizzes=quizzes)

@student_bp.route('/quizzes/<int:id>/start', methods=['GET', 'POST'])
@check_college_access
def start_quiz(id):
    quiz = Quiz.query.filter_by(id=id, college_id=current_user.college_id, is_published=True).first_or_404()
    if request.method == 'POST':
        mode = request.form.get('mode', 'learning')
        
        attempt = QuizAttempt(
            quiz_id=quiz.id,
            student_id=current_user.id,
            mode=mode,
            score=0,
            total_marks=0,
            percentage=0.0
        )
        db.session.add(attempt)
        db.session.commit()
        return redirect(url_for('student.attempt_quiz', attempt_id=attempt.id))
        
    return render_template('student/quiz_start.html', quiz=quiz)

@student_bp.route('/attempts/<int:attempt_id>', methods=['GET'])
@check_college_access
def attempt_quiz(attempt_id):
    attempt = QuizAttempt.query.filter_by(id=attempt_id, student_id=current_user.id).first_or_404()
    if attempt.submitted_at:
        return redirect(url_for('student.quiz_result', attempt_id=attempt.id))
        
    quiz = attempt.quiz_rel
    answered_options = {ans.question_id: ans.selected_option_id for ans in attempt.answers}
    
    return render_template('student/quiz_attempt.html', quiz=quiz, attempt=attempt, answered_options=answered_options)

@student_bp.route('/attempts/<int:attempt_id>/answer', methods=['POST'])
@check_college_access
def submit_answer(attempt_id):
    attempt = QuizAttempt.query.filter_by(id=attempt_id, student_id=current_user.id).first_or_404()
    if attempt.submitted_at:
        return redirect(url_for('student.quiz_result', attempt_id=attempt.id))
    question_id = request.form.get('question_id', type=int)
    selected_option_id = request.form.get('selected_option_id', type=int)
    
    question = Question.query.get_or_404(question_id)
    selected_option = QuestionOption.query.get(selected_option_id)
    
    is_correct = selected_option.is_correct if selected_option else False
    marks_awarded = question.marks if is_correct else 0
    
    submission = AnswerSubmission(
        attempt_id=attempt.id,
        question_id=question.id,
        selected_option_id=selected_option_id,
        is_correct=is_correct,
        marks_awarded=marks_awarded
    )
    db.session.add(submission)
    db.session.commit()
    
    if is_correct:
        flash('Correct answer!', 'success')
    else:
        flash('Incorrect answer.', 'danger')
        
    return redirect(url_for('student.attempt_quiz', attempt_id=attempt.id))

@student_bp.route('/attempts/<int:attempt_id>/submit', methods=['POST'])
@check_college_access
def submit_quiz(attempt_id):
    attempt = QuizAttempt.query.filter_by(id=attempt_id, student_id=current_user.id).first_or_404()
    if attempt.submitted_at:
        return redirect(url_for('student.quiz_result', attempt_id=attempt.id))
    
    final_mode = request.form.get('final_mode', attempt.mode)
    if final_mode in ['learning', 'exam']:
        attempt.mode = final_mode
        
    # Clear any previous answers for this attempt before saving new ones
    AnswerSubmission.query.filter_by(attempt_id=attempt.id).delete()
    
    for question in attempt.quiz_rel.questions:
        selected_id = request.form.get(f'q_{question.id}', type=int)
        if selected_id:
            selected_option = QuestionOption.query.get(selected_id)
            is_correct = selected_option.is_correct if selected_option else False
            marks_awarded = question.marks if is_correct else 0
            
            sub = AnswerSubmission(
                attempt_id=attempt.id,
                question_id=question.id,
                selected_option_id=selected_id,
                is_correct=is_correct,
                marks_awarded=marks_awarded
            )
            db.session.add(sub)
            
    total_marks = sum(q.marks for q in attempt.quiz_rel.questions)
    db.session.commit()
    
    earned_marks = sum(s.marks_awarded for s in attempt.answers)
    attempt.score = earned_marks
    attempt.total_marks = total_marks
    attempt.percentage = (earned_marks / total_marks * 100) if total_marks > 0 else 0
    attempt.submitted_at = datetime.utcnow()
    attempt.status = 'submitted'
    
    progress = StudentProgress.query.filter_by(student_id=current_user.id, subject_id=attempt.quiz_rel.subject_id).first()
    if not progress:
        progress = StudentProgress(student_id=current_user.id, college_id=current_user.college_id, subject_id=attempt.quiz_rel.subject_id, quizzes_attempted=0, average_score=0.0)
        db.session.add(progress)
    
    old_total = progress.average_score * progress.quizzes_attempted
    progress.quizzes_attempted += 1
    progress.average_score = (old_total + attempt.percentage) / progress.quizzes_attempted
    
    db.session.commit()
    return redirect(url_for('student.quiz_result', attempt_id=attempt.id))

@student_bp.route('/attempts/<int:attempt_id>/result', methods=['GET'])
@check_college_access
def quiz_result(attempt_id):
    attempt = QuizAttempt.query.filter(QuizAttempt.id == attempt_id, QuizAttempt.student_id == current_user.id, QuizAttempt.submitted_at.isnot(None)).first_or_404()
    return render_template('student/quiz_result.html', attempt=attempt, total_marks=attempt.total_marks)

@student_bp.route('/attempts/<int:attempt_id>/review', methods=['GET'])
@check_college_access
def quiz_review(attempt_id):
    attempt = QuizAttempt.query.filter(QuizAttempt.id == attempt_id, QuizAttempt.student_id == current_user.id, QuizAttempt.submitted_at.isnot(None)).first_or_404()
    submissions = {s.question_id: s for s in attempt.answers}
    return render_template('student/quiz_review.html', attempt=attempt, submissions=submissions)

@student_bp.route('/subjects', methods=['GET'])
@check_college_access
def subjects():
    subs = Subject.query.filter_by(college_id=current_user.college_id, is_active=True).all()
    return render_template('student/subjects.html', subjects=subs)

@student_bp.route('/subjects/<int:id>', methods=['GET'])
@check_college_access
def subject_details(id):
    subject = Subject.query.get_or_404(id)
    if subject.college_id != current_user.college_id:
        abort(403)
    if not subject.is_active:
        abort(404)
    # Get published materials, PYQs, and quizzes with no unit_id
    materials = StudyMaterial.query.filter_by(subject_id=subject.id, unit_id=None, is_published=True).all()
    pyqs = PYQPaper.query.filter_by(subject_id=subject.id, unit_id=None, is_published=True).all()
    quizzes = Quiz.query.filter_by(subject_id=subject.id, unit_id=None, is_published=True).all()
    return render_template('student/subject_details.html', subject=subject, materials=materials, pyqs=pyqs, quizzes=quizzes)

@student_bp.route('/units/<int:id>', methods=['GET'])
@check_college_access
def unit_details(id):
    unit = Unit.query.get_or_404(id)
    if unit.subject.college_id != current_user.college_id:
        abort(403)
    if not unit.subject.is_active:
        abort(404)
    materials = StudyMaterial.query.filter_by(unit_id=unit.id, is_published=True).all()
    pyqs = PYQPaper.query.filter_by(unit_id=unit.id, is_published=True).all()
    quizzes = Quiz.query.filter_by(unit_id=unit.id, is_published=True).all()
    return render_template('student/unit_details.html', unit=unit, materials=materials, pyqs=pyqs, quizzes=quizzes)

@student_bp.route('/pyqs', methods=['GET'])
@check_college_access
def pyqs():
    pyqs_list = PYQPaper.query.filter_by(college_id=current_user.college_id, is_published=True).all()
    return render_template('student/pyqs.html', pyqs=pyqs_list)

@student_bp.route('/pyqs/<int:id>', methods=['GET'])
@check_college_access
def pyq_details(id):
    pyq = PYQPaper.query.get_or_404(id)
    if pyq.college_id != current_user.college_id:
        abort(403)
    if not pyq.is_published:
        abort(403)
    return render_template('student/pyq_details.html', pyq=pyq)

@student_bp.route('/materials/<int:id>', methods=['GET'])
@check_college_access
def material_details(id):
    material = StudyMaterial.query.get_or_404(id)
    if material.college_id != current_user.college_id:
        abort(403)
    if not material.is_published:
        abort(403)
    return render_template('student/material_details.html', material=material)

@student_bp.route('/notifications/<int:id>/open', methods=['GET'])
@check_college_access
def open_notification(id):
    import re
    notification = Notification.query.get_or_404(id)
    if notification.college_id != current_user.college_id:
        abort(403)
        
    # Check if subscription exists for that subject
    sub = SubjectSubscription.query.filter_by(user_id=current_user.id, subject_id=notification.subject_id).first()
    if not sub:
        flash('You are not subscribed to this subject.', 'warning')
        return redirect(url_for('student.notifications'))
        
    # Mark as read automatically
    already_read = NotificationRead.query.filter_by(user_id=current_user.id, notification_id=notification.id).first()
    if not already_read:
        read_entry = NotificationRead(user_id=current_user.id, notification_id=notification.id)
        db.session.add(read_entry)
        db.session.commit()

    # Determine safe target URL
    target_url = None
    if notification.link:
        material_match = re.search(r'/materials/(\d+)', notification.link)
        pyq_match = re.search(r'/pyqs/(\d+)', notification.link)
        quiz_match = re.search(r'/quizzes/(\d+)', notification.link)
        comm_match = re.search(r'/community/materials/(\d+)', notification.link)
        
        if material_match and (notification.notification_type == 'material' or not notification.notification_type):
            mat_id = int(material_match.group(1))
            mat = StudyMaterial.query.get(mat_id)
            if mat and mat.is_published and mat.college_id == current_user.college_id:
                target_url = url_for('student.material_details', id=mat_id)
            else:
                flash('This study material is no longer available.', 'warning')
                return redirect(url_for('student.notifications'))
                
        elif pyq_match and (notification.notification_type == 'pyq' or not notification.notification_type):
            pq_id = int(pyq_match.group(1))
            pq = PYQPaper.query.get(pq_id)
            if pq and pq.is_published and pq.college_id == current_user.college_id:
                target_url = url_for('student.pyq_details', id=pq_id)
            else:
                flash('This PYQ paper is no longer available.', 'warning')
                return redirect(url_for('student.notifications'))
                
        elif quiz_match and (notification.notification_type == 'quiz' or not notification.notification_type):
            qz_id = int(quiz_match.group(1))
            qz = Quiz.query.get(qz_id)
            if qz and qz.is_published and qz.college_id == current_user.college_id:
                target_url = url_for('student.start_quiz', id=qz_id)
            else:
                flash('This quiz is no longer available.', 'warning')
                return redirect(url_for('student.notifications'))
                
        elif comm_match:
            c_id = int(comm_match.group(1))
            c_mat = CommunityMaterial.query.get(c_id)
            if c_mat and c_mat.status == 'active':
                target_url = url_for('student.community_material_details', id=c_id)
            else:
                flash('This community material is no longer available.', 'warning')
                return redirect(url_for('student.notifications'))

    if not target_url:
        target_url = notification.link if notification.link else url_for('student.notifications')
        
    return redirect(target_url)

@student_bp.route('/notifications', methods=['GET'])
@check_college_access
def notifications():
    sub_ids = [s.subject_id for s in current_user.subscriptions]
    if not sub_ids:
        notifications_list = []
    else:
        notifications_list = Notification.query.filter(
            Notification.college_id == current_user.college_id,
            Notification.subject_id.in_(sub_ids)
        ).order_by(Notification.created_at.desc()).all()
    
    # Get read notification IDs for this user
    read_notification_ids = {r.notification_id for r in NotificationRead.query.filter_by(user_id=current_user.id).all()}
    
    return render_template('student/notifications.html', 
                           notifications=notifications_list, 
                           read_notification_ids=read_notification_ids)


@student_bp.route('/notifications/<int:id>/read', methods=['POST'])
@check_college_access
def read_notification(id):
    notification = Notification.query.get_or_404(id)
    if notification.college_id != current_user.college_id:
        abort(403)
        
    # Check if a subscription exists for that subject
    sub = SubjectSubscription.query.filter_by(user_id=current_user.id, subject_id=notification.subject_id).first()
    if not sub:
        flash('You are not subscribed to this subject.', 'warning')
        return redirect(url_for('student.notifications'))
        
    already_read = NotificationRead.query.filter_by(user_id=current_user.id, notification_id=notification.id).first()
    if not already_read:
        read_entry = NotificationRead(user_id=current_user.id, notification_id=notification.id)
        db.session.add(read_entry)
        db.session.commit()
        
    flash('Notification marked as read.', 'success')
    return redirect(url_for('student.notifications'))


@student_bp.route('/notifications/read-all', methods=['POST'])
@check_college_access
def read_all_notifications():
    sub_ids = [s.subject_id for s in current_user.subscriptions]
    if not sub_ids:
        unread_notifications = []
    else:
        unread_notifications = Notification.query.filter(
            Notification.college_id == current_user.college_id,
            Notification.subject_id.in_(sub_ids)
        ).all()
    
    read_notification_ids = {r.notification_id for r in NotificationRead.query.filter_by(user_id=current_user.id).all()}
    
    count = 0
    for notification in unread_notifications:
        if notification.id not in read_notification_ids:
            read_entry = NotificationRead(user_id=current_user.id, notification_id=notification.id)
            db.session.add(read_entry)
            count += 1
            
    if count > 0:
        db.session.commit()
        flash(f'Marked {count} notifications as read.', 'success')
    else:
        flash('No new notifications to mark as read.', 'info')
        
    return redirect(url_for('student.notifications'))


@student_bp.route('/subjects/<int:id>/toggle-subscription', methods=['POST'])
@check_college_access
def toggle_subscription(id):
    subject = Subject.query.get_or_404(id)
    if subject.college_id != current_user.college_id:
        abort(403)
        
    sub = SubjectSubscription.query.filter_by(user_id=current_user.id, subject_id=subject.id).first()
    if sub:
        db.session.delete(sub)
        db.session.commit()
        flash(f'Unsubscribed from {subject.name} notifications.', 'info')
    else:
        new_sub = SubjectSubscription(user_id=current_user.id, subject_id=subject.id)
        db.session.add(new_sub)
        db.session.commit()
        flash(f'Subscribed to {subject.name} notifications.', 'success')
        
    return redirect(url_for('student.subject_details', id=subject.id))


@student_bp.route('/community', methods=['GET'])
@check_college_access
def community_library():
    search_query = request.args.get('q', '', type=str)
    material_type = request.args.get('material_type', '', type=str)
    college_tag_id = request.args.get('college_tag_id', type=int)
    sort_by = request.args.get('sort', 'latest', type=str)

    # Base query: active status only
    query = CommunityMaterial.query.filter_by(status='active')

    # Apply search filter
    if search_query:
        query = query.filter(
            or_(
                CommunityMaterial.title.ilike(f'%{search_query}%'),
                CommunityMaterial.description.ilike(f'%{search_query}%'),
                CommunityMaterial.subject_name.ilike(f'%{search_query}%')
            )
        )

    # Apply material type filter
    if material_type:
        query = query.filter_by(material_type=material_type)

    # Apply college tag filter
    if college_tag_id:
        query = query.filter_by(college_tag_id=college_tag_id)

    # Apply sorting
    if sort_by == 'views':
        query = query.order_by(CommunityMaterial.views_count.desc(), CommunityMaterial.created_at.desc())
    elif sort_by == 'likes':
        query = query.order_by(CommunityMaterial.likes_count.desc(), CommunityMaterial.created_at.desc())
    elif sort_by == 'rating':
        query = query.order_by(CommunityMaterial.average_rating.desc(), CommunityMaterial.created_at.desc())
    else: # default latest
        query = query.order_by(CommunityMaterial.created_at.desc())

    materials = query.all()
    colleges = College.query.filter_by(status='active').all()

    liked_material_ids = set()
    if current_user.is_authenticated:
        likes = CommunityMaterialLike.query.filter_by(user_id=current_user.id).all()
        liked_material_ids = {l.material_id for l in likes}

    return render_template(
        'student/community_list.html',
        materials=materials,
        colleges=colleges,
        search_query=search_query,
        selected_material_type=material_type,
        selected_college_tag_id=college_tag_id,
        sort_by=sort_by,
        liked_material_ids=liked_material_ids
    )


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'


@student_bp.route('/community/upload', methods=['GET', 'POST'])
@check_college_access
def upload_community_material():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        subject_name = request.form.get('subject_name', '').strip()
        college_tag_id = request.form.get('college_tag_id', type=int)
        material_type = request.form.get('material_type', 'notes').strip()
        external_url = request.form.get('external_url', '').strip()
        file = request.files.get('file')

        # Validation checks
        if not title:
            flash('Title is required.', 'danger')
            return redirect(url_for('student.upload_community_material'))

        if not subject_name:
            flash('Subject name is required.', 'danger')
            return redirect(url_for('student.upload_community_material'))

        has_file = file and file.filename != ''
        if not has_file and not external_url:
            flash('You must either upload a PDF file or provide an external URL.', 'danger')
            return redirect(url_for('student.upload_community_material'))

        if external_url and not (external_url.startswith('http://') or external_url.startswith('https://')):
            flash('External URL must start with http:// or https://', 'danger')
            return redirect(url_for('student.upload_community_material'))

        filename = None
        if has_file:
            if not allowed_file(file.filename):
                flash('Only PDF files are allowed in the Community Library.', 'danger')
                return redirect(url_for('student.upload_community_material'))

            filename = secure_filename(f"{int(time.time())}_{file.filename}")
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER_COMMUNITY'], filename)
            file.save(filepath)

        # Create model instance
        material = CommunityMaterial(
            title=title,
            description=description if description else None,
            subject_name=subject_name,
            college_tag_id=college_tag_id if college_tag_id else None,
            uploaded_by=current_user.id,
            material_type=material_type,
            file_path=filename,
            external_url=external_url if external_url else None,
            status='active'
        )

        db.session.add(material)
        db.session.commit()

        # Audit logging
        log_action(current_user.id, 'community_material_uploaded', 'community_material', material.id, f"Uploaded: {title}")
        flash('Material shared with the community successfully!', 'success')
        return redirect(url_for('student.my_community_uploads'))

    colleges = College.query.filter_by(status='active').all()
    return render_template('student/community_upload.html', colleges=colleges)


@student_bp.route('/community/materials/<int:id>/edit', methods=['GET', 'POST'])
@check_college_access
def edit_community_material(id):
    material = CommunityMaterial.query.get_or_404(id)
    if material.uploaded_by != current_user.id:
        abort(403)
    if material.status != 'active':
        flash('You can only edit active community materials.', 'danger')
        return redirect(url_for('student.my_community_uploads'))
        
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        subject_name = request.form.get('subject_name', '').strip()
        college_tag_id = request.form.get('college_tag_id', type=int)
        material_type = request.form.get('material_type', 'notes').strip()
        external_url = request.form.get('external_url', '').strip()
        file = request.files.get('file')
        
        # Validation checks
        if not title:
            flash('Title is required.', 'danger')
            return redirect(url_for('student.edit_community_material', id=material.id))
            
        if not subject_name:
            flash('Subject name is required.', 'danger')
            return redirect(url_for('student.edit_community_material', id=material.id))
            
        has_new_file = file and file.filename != ''
        
        # Check if we have at least one valid resource (either existing or new)
        has_file = has_new_file or material.file_path
        has_url = external_url or material.external_url
        if not has_file and not has_url:
            flash('You must either upload a PDF file or provide an external URL.', 'danger')
            return redirect(url_for('student.edit_community_material', id=material.id))
            
        if external_url and not (external_url.startswith('http://') or external_url.startswith('https://')):
            flash('External URL must start with http:// or https://', 'danger')
            return redirect(url_for('student.edit_community_material', id=material.id))
            
        # If new file is uploaded
        if has_new_file:
            if not allowed_file(file.filename):
                flash('Only PDF files are allowed in the Community Library.', 'danger')
                return redirect(url_for('student.edit_community_material', id=material.id))
                
            # Optionally remove the old file if it existed
            if material.file_path:
                old_filepath = os.path.join(current_app.config['UPLOAD_FOLDER_COMMUNITY'], material.file_path)
                if os.path.exists(old_filepath):
                    try:
                        os.remove(old_filepath)
                    except Exception:
                        pass
                        
            filename = secure_filename(f"{int(time.time())}_{file.filename}")
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER_COMMUNITY'], filename)
            file.save(filepath)
            material.file_path = filename

        # If they want to clear the link (but we have a file)
        if not external_url and material.file_path:
            material.external_url = None
        elif external_url:
            material.external_url = external_url
            
        # If they want to clear the file (but we have a link)
        clear_file = request.form.get('clear_file') == 'true'
        if clear_file and material.external_url:
            if material.file_path:
                old_filepath = os.path.join(current_app.config['UPLOAD_FOLDER_COMMUNITY'], material.file_path)
                if os.path.exists(old_filepath):
                    try:
                        os.remove(old_filepath)
                    except Exception:
                        pass
                material.file_path = None
                
        material.title = title
        material.description = description if description else None
        material.subject_name = subject_name
        material.college_tag_id = college_tag_id if college_tag_id else None
        material.material_type = material_type
        
        db.session.commit()
        log_action(current_user.id, 'community_material_edited', 'community_material', material.id, f"Edited: {title}")
        flash('Material updated successfully!', 'success')
        return redirect(url_for('student.community_material_details', id=material.id))
        
    colleges = College.query.filter_by(status='active').all()
    return render_template('student/community_edit.html', colleges=colleges, material=material)


@student_bp.route('/community/materials/<int:id>/delete', methods=['POST'])
@check_college_access
def delete_community_material(id):
    material = CommunityMaterial.query.get_or_404(id)
    if material.uploaded_by != current_user.id:
        abort(403)
    if material.status != 'active':
        flash('You can only remove active community materials.', 'danger')
        return redirect(url_for('student.my_community_uploads'))
        
    material.status = 'removed_by_uploader'
    db.session.commit()
    log_action(current_user.id, 'community_material_removed_by_uploader', 'community_material', material.id, f"Removed by uploader: {material.title}")
    flash('Material removed from the Community Library.', 'success')
    return redirect(url_for('student.my_community_uploads'))


@student_bp.route('/community/my-uploads', methods=['GET'])
@check_college_access
def my_community_uploads():
    materials = CommunityMaterial.query.filter(
        CommunityMaterial.uploaded_by == current_user.id,
        CommunityMaterial.status.notin_(['removed', 'removed_by_uploader'])
    ).order_by(CommunityMaterial.created_at.desc()).all()
    return render_template('student/community_my_uploads.html', materials=materials)


@student_bp.route('/community/materials/<int:id>', methods=['GET'])
@check_college_access
def community_material_details(id):
    material = CommunityMaterial.query.get_or_404(id)
    
    # Allow uploader or platform_admin to see it regardless of active status,
    # otherwise only 'active' materials can be viewed by others.
    if material.status != 'active':
        if current_user.id != material.uploaded_by and current_user.role != 'platform_admin':
            flash('This material is currently unavailable.', 'danger')
            return redirect(url_for('student.community_library'))

    # Record unique view
    if current_user.is_authenticated:
        # Check if already viewed
        existing_view = CommunityMaterialView.query.filter_by(
            user_id=current_user.id,
            material_id=material.id
        ).first()
        if not existing_view:
            new_view = CommunityMaterialView(
                user_id=current_user.id,
                material_id=material.id
            )
            db.session.add(new_view)
            material.views_count += 1
            db.session.commit()

    user_liked = False
    user_rating = None
    user_reported = False
    if current_user.is_authenticated:
        like = CommunityMaterialLike.query.filter_by(user_id=current_user.id, material_id=material.id).first()
        if like:
            user_liked = True
        rating = CommunityMaterialRating.query.filter_by(user_id=current_user.id, material_id=material.id).first()
        if rating:
            user_rating = rating.rating
        report = CommunityMaterialReport.query.filter_by(user_id=current_user.id, material_id=material.id).first()
        if report:
            user_reported = True

    return render_template('student/community_details.html', material=material, user_liked=user_liked, user_rating=user_rating, user_reported=user_reported)


@student_bp.route('/community/users/<int:user_id>', methods=['GET'])
@check_college_access
def community_user_profile(user_id):
    uploader = User.query.get_or_404(user_id)
    # Only show active students
    if not uploader.is_active or uploader.role != 'student':
        flash('User profile not found or unavailable.', 'danger')
        return redirect(url_for('student.community_library'))

    # Get active materials by this user
    materials = CommunityMaterial.query.filter_by(
        uploaded_by=uploader.id, 
        status='active'
    ).order_by(CommunityMaterial.created_at.desc()).all()

    # Calculate stats
    total_active_uploads = len(materials)
    total_likes = sum(m.likes_count for m in materials)
    total_views = sum(m.views_count for m in materials)
    
    materials_with_ratings = [m for m in materials if m.ratings_count > 0]
    avg_rating = 0.0
    if materials_with_ratings:
        avg_rating = round(sum(m.average_rating for m in materials_with_ratings) / len(materials_with_ratings), 1)

    liked_material_ids = set()
    if current_user.is_authenticated:
        likes = CommunityMaterialLike.query.filter_by(user_id=current_user.id).all()
        liked_material_ids = {l.material_id for l in likes}

    return render_template(
        'student/community_user_profile.html',
        uploader=uploader,
        materials=materials,
        total_active_uploads=total_active_uploads,
        total_likes=total_likes,
        total_views=total_views,
        avg_rating=avg_rating,
        liked_material_ids=liked_material_ids
    )


@student_bp.route('/community/materials/<int:id>/like', methods=['POST'])
@check_college_access
def like_community_material(id):
    from flask import jsonify
    material = CommunityMaterial.query.get_or_404(id)
    if material.status != 'active':
        if request.headers.get('Accept') == 'application/json':
            return jsonify({'success': False, 'message': 'Cannot like an inactive material.'}), 400
        flash('Cannot like an inactive material.', 'danger')
        return redirect(url_for('student.community_library'))
        
    like = CommunityMaterialLike.query.filter_by(user_id=current_user.id, material_id=material.id).first()
    liked = False
    if like:
        db.session.delete(like)
        material.likes_count = max(0, material.likes_count - 1)
        liked = False
    else:
        new_like = CommunityMaterialLike(user_id=current_user.id, material_id=material.id)
        db.session.add(new_like)
        material.likes_count += 1
        liked = True
        
    db.session.commit()
    
    # Check if request expects JSON (AJAX)
    if request.headers.get('Accept') == 'application/json' or request.is_json:
        return jsonify({
            'success': True,
            'liked': liked,
            'likes_count': material.likes_count
        })
        
    if liked:
        flash('You liked this material.', 'success')
    else:
        flash('You unliked this material.', 'info')
        
    return redirect(url_for('student.community_material_details', id=material.id))

@student_bp.route('/community/materials/<int:id>/rate', methods=['POST'])
@check_college_access
def rate_community_material(id):
    material = CommunityMaterial.query.get_or_404(id)
    if material.status != 'active':
        flash('Cannot rate an inactive material.', 'danger')
        return redirect(url_for('student.community_library'))
        
    rating_val = request.form.get('rating', type=int)
    if not rating_val or rating_val < 1 or rating_val > 5:
        flash('Invalid rating value. Must be between 1 and 5.', 'danger')
        return redirect(url_for('student.community_material_details', id=material.id))
        
    rating = CommunityMaterialRating.query.filter_by(user_id=current_user.id, material_id=material.id).first()
    if rating:
        rating.rating = rating_val
        flash('Your rating was updated.', 'success')
    else:
        new_rating = CommunityMaterialRating(user_id=current_user.id, material_id=material.id, rating=rating_val)
        db.session.add(new_rating)
        flash('Your rating was submitted.', 'success')
        
    db.session.commit()
    
    # Recalculate average rating
    all_ratings = CommunityMaterialRating.query.filter_by(material_id=material.id).all()
    if all_ratings:
        material.ratings_count = len(all_ratings)
        material.average_rating = sum(r.rating for r in all_ratings) / material.ratings_count
    else:
        material.ratings_count = 0
        material.average_rating = 0.0
        
    db.session.commit()
    return redirect(url_for('student.community_material_details', id=material.id))

@student_bp.route('/community/materials/<int:id>/report', methods=['POST'])
@check_college_access
def report_community_material(id):
    material = CommunityMaterial.query.get_or_404(id)
    if material.status != 'active':
        flash('You cannot report an inactive material.', 'danger')
        return redirect(url_for('student.community_library'))
        
    existing_report = CommunityMaterialReport.query.filter_by(user_id=current_user.id, material_id=material.id).first()
    if existing_report:
        flash('You have already reported this material.', 'warning')
        return redirect(url_for('student.community_material_details', id=material.id))
        
    reason = request.form.get('reason', '').strip()
    details = request.form.get('details', '').strip()
    
    if not reason:
        flash('A reason is required to report.', 'danger')
        return redirect(url_for('student.community_material_details', id=material.id))
        
    if reason == 'Other' and details:
        reason_text = f"Other: {details}"
    else:
        reason_text = reason
        
    new_report = CommunityMaterialReport(user_id=current_user.id, material_id=material.id, reason=reason_text)
    db.session.add(new_report)
    
    material.reports_count += 1
    
    # Calculate risk score and handle escalations
    update_community_material_moderation(material)
    
    db.session.commit()
    
    if material.status == 'under_review':
        flash('Thank you for your report. The material has been flagged for review by moderators.', 'warning')
        # If it's under review, it shouldn't show in the normal list, so send them back to the list
        return redirect(url_for('student.community_library'))
    else:
        flash('Thank you for reporting this material.', 'success')
        return redirect(url_for('student.community_material_details', id=material.id))


@student_bp.route('/profile')
@check_college_access
def profile():
    uploads_count = CommunityMaterial.query.filter_by(uploaded_by=current_user.id).count()
    quiz_attempts_count = QuizAttempt.query.filter_by(student_id=current_user.id).count()
    return render_template('student/profile.html', 
                           uploads_count=uploads_count, 
                           quiz_attempts_count=quiz_attempts_count)

