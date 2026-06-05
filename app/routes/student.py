from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.models import College, Subject, Unit, StudyMaterial, PYQPaper, Quiz, QuizAttempt, Question, QuestionOption, AnswerSubmission, StudentProgress, SubjectSubscription, Notification, NotificationRead
from app.extensions import db
from datetime import datetime
from functools import wraps

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
    subjects = Subject.query.filter_by(college_id=current_user.college_id, is_active=True).all()
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

