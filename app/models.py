from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False) # platform_admin, college_admin, student
    college_id = db.Column(db.Integer, db.ForeignKey('colleges.id'), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    onboarding_completed = db.Column(db.Boolean, default=False, nullable=False)
    profile_completed = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    college = db.relationship('College', foreign_keys=[college_id], backref='users')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_unread_notification_count(self):
        if self.role != 'student' or not self.college_id:
            return 0
        from .models import Notification, SubjectSubscription, NotificationRead
        sub_ids = [s.subject_id for s in self.subscriptions]
        if not sub_ids:
            return 0
        total_notifications = Notification.query.filter(
            Notification.college_id == self.college_id,
            Notification.subject_id.in_(sub_ids)
        ).all()
        read_ids = {r.notification_id for r in NotificationRead.query.filter_by(user_id=self.id).all()}
        return sum(1 for n in total_notifications if n.id not in read_ids)


class College(db.Model):
    __tablename__ = 'colleges'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text, nullable=False)
    contact_email = db.Column(db.String(120), nullable=False)
    contact_phone = db.Column(db.String(20), nullable=False)
    logo_path = db.Column(db.String(256), nullable=True)
    status = db.Column(db.String(20), default='active') # active, inactive, pending, rejected
    created_by_admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    created_by_admin = db.relationship('User', foreign_keys=[created_by_admin_id])


class CollegeRequest(db.Model):
    __tablename__ = 'college_requests'
    id = db.Column(db.Integer, primary_key=True)
    college_name = db.Column(db.String(150), nullable=False)
    college_code = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text, nullable=False)
    admin_full_name = db.Column(db.String(100), nullable=False)
    admin_email = db.Column(db.String(120), nullable=False)
    admin_phone = db.Column(db.String(20), nullable=False)
    admin_password_hash = db.Column(db.String(256), nullable=True)
    message = db.Column(db.Text, nullable=True)
    logo_path = db.Column(db.String(256), nullable=True)
    status = db.Column(db.String(20), default='pending') # pending, approved, rejected
    reviewed_by_admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    college_id = db.Column(db.Integer, db.ForeignKey('colleges.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    semester = db.Column(db.Integer, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    college = db.relationship('College', backref='subjects')
    creator = db.relationship('User', foreign_keys=[created_by])


class Unit(db.Model):
    __tablename__ = 'units'
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    unit_number = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    subject = db.relationship('Subject', backref='units')
    creator = db.relationship('User', foreign_keys=[created_by])


class StudyMaterial(db.Model):
    __tablename__ = 'study_materials'
    id = db.Column(db.Integer, primary_key=True)
    college_id = db.Column(db.Integer, db.ForeignKey('colleges.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id'), nullable=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    file_path = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50), nullable=False) # pdf, notes, assignment, important_questions, other
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    subject = db.relationship('Subject', backref='materials')
    unit = db.relationship('Unit', backref='materials')
    uploader = db.relationship('User', foreign_keys=[uploaded_by])


class PYQPaper(db.Model):
    __tablename__ = 'pyq_papers'
    id = db.Column(db.Integer, primary_key=True)
    college_id = db.Column(db.Integer, db.ForeignKey('colleges.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id'), nullable=True)
    title = db.Column(db.String(150), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    exam_type = db.Column(db.String(50), nullable=False) # mid_sem, end_sem, internal, practical, other
    file_path = db.Column(db.String(255), nullable=False)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    subject = db.relationship('Subject', backref='pyqs')
    unit = db.relationship('Unit', backref='pyqs')
    uploader = db.relationship('User', foreign_keys=[uploaded_by])


class Quiz(db.Model):
    __tablename__ = 'quizzes'
    id = db.Column(db.Integer, primary_key=True)
    college_id = db.Column(db.Integer, db.ForeignKey('colleges.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id'), nullable=True)
    study_material_id = db.Column(db.Integer, db.ForeignKey('study_materials.id'), nullable=True)
    pyq_paper_id = db.Column(db.Integer, db.ForeignKey('pyq_papers.id'), nullable=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    quiz_type = db.Column(db.String(50), nullable=False) # practice, pyq, unit_test, subject_test
    difficulty = db.Column(db.String(20), nullable=False) # easy, medium, hard, mixed
    time_limit_minutes = db.Column(db.Integer, nullable=True)
    is_published = db.Column(db.Boolean, default=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    subject = db.relationship('Subject', backref='quizzes')
    unit = db.relationship('Unit', backref='quizzes')
    creator = db.relationship('User', foreign_keys=[created_by])
    questions = db.relationship('Question', backref='quiz', cascade='all, delete-orphan')


class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    explanation = db.Column(db.Text, nullable=True)
    marks = db.Column(db.Integer, default=1)
    order_number = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    options = db.relationship('QuestionOption', backref='question', cascade='all, delete-orphan')


class QuestionOption(db.Model):
    __tablename__ = 'question_options'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    option_text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    order_number = db.Column(db.Integer, default=1)


class QuizAttempt(db.Model):
    __tablename__ = 'quiz_attempts'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    mode = db.Column(db.String(20), nullable=False) # learning, exam
    score = db.Column(db.Integer, nullable=True)
    total_marks = db.Column(db.Integer, nullable=True)
    percentage = db.Column(db.Float, nullable=True)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    submitted_at = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default='in_progress') # in_progress, submitted, abandoned

    student = db.relationship('User', foreign_keys=[student_id])
    quiz_rel = db.relationship('Quiz', foreign_keys=[quiz_id])
    answers = db.relationship('AnswerSubmission', backref='attempt', cascade='all, delete-orphan')


class AnswerSubmission(db.Model):
    __tablename__ = 'answer_submissions'
    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('quiz_attempts.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    selected_option_id = db.Column(db.Integer, db.ForeignKey('question_options.id'), nullable=True)
    is_correct = db.Column(db.Boolean, nullable=True)
    marks_awarded = db.Column(db.Integer, default=0)
    answered_at = db.Column(db.DateTime, default=datetime.utcnow)


class StudentProgress(db.Model):
    __tablename__ = 'student_progress'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    college_id = db.Column(db.Integer, db.ForeignKey('colleges.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=True)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id'), nullable=True)
    quizzes_attempted = db.Column(db.Integer, default=0)
    average_score = db.Column(db.Float, default=0.0)
    best_score = db.Column(db.Float, default=0.0)
    last_activity_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    id = db.Column(db.Integer, primary_key=True)
    actor_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    action = db.Column(db.String(100), nullable=False)
    target_type = db.Column(db.String(50), nullable=False)
    target_id = db.Column(db.Integer, nullable=True)
    details = db.Column(db.Text, nullable=True)
    ip_address = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    actor = db.relationship('User', foreign_keys=[actor_user_id])


class SubjectSubscription(db.Model):
    __tablename__ = 'subject_subscriptions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    is_enabled = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('user_id', 'subject_id', name='_user_subject_uc'),)

    user = db.relationship('User', backref='subscriptions')
    subject = db.relationship('Subject', backref='subscribers')


class CollegeSubscription(db.Model):
    __tablename__ = 'college_subscriptions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    college_id = db.Column(db.Integer, db.ForeignKey('colleges.id'), nullable=False)
    is_enabled = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('user_id', 'college_id', name='_user_college_uc'),)

    user = db.relationship('User', backref=db.backref('college_subscriptions', cascade='all, delete-orphan'))
    college = db.relationship('College', backref=db.backref('college_subscriptions', cascade='all, delete-orphan'))



class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    college_id = db.Column(db.Integer, db.ForeignKey('colleges.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id'), nullable=True)
    notification_type = db.Column(db.String(50), nullable=True) # material, pyq, quiz
    title = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(255), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    college = db.relationship('College', backref='notifications')
    subject = db.relationship('Subject', backref='notifications')
    unit = db.relationship('Unit', backref='notifications')
    creator = db.relationship('User', foreign_keys=[created_by], backref='created_notifications')


class NotificationRead(db.Model):
    __tablename__ = 'notification_reads'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    notification_id = db.Column(db.Integer, db.ForeignKey('notifications.id'), nullable=False)
    read_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('user_id', 'notification_id', name='_user_notification_uc'),)

    user = db.relationship('User', backref='reads')
    notification = db.relationship('Notification', backref='reads')


class CommunityMaterial(db.Model):
    __tablename__ = 'community_materials'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    subject_name = db.Column(db.String(100), nullable=False)
    college_tag_id = db.Column(db.Integer, db.ForeignKey('colleges.id'), nullable=True)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    material_type = db.Column(db.String(50), default='notes')
    file_path = db.Column(db.String(255), nullable=True)
    external_url = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), default='active')
    views_count = db.Column(db.Integer, default=0)
    likes_count = db.Column(db.Integer, default=0)
    reports_count = db.Column(db.Integer, default=0)
    ratings_count = db.Column(db.Integer, default=0)
    average_rating = db.Column(db.Float, default=0.0)
    moderation_score = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    college_tag = db.relationship('College', foreign_keys=[college_tag_id])
    uploader = db.relationship('User', foreign_keys=[uploaded_by])


class CommunityMaterialLike(db.Model):
    __tablename__ = 'community_material_likes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('community_materials.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('user_id', 'material_id', name='_user_community_material_like_uc'),)

    user = db.relationship('User', backref='community_likes')
    material = db.relationship('CommunityMaterial', backref='likes_rel')


class CommunityMaterialView(db.Model):
    __tablename__ = 'community_material_views'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('community_materials.id'), nullable=False)
    viewed_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('user_id', 'material_id', name='_user_community_material_view_uc'),)

    user = db.relationship('User', backref='community_views')
    material = db.relationship('CommunityMaterial', backref='views_rel')


class CommunityMaterialRating(db.Model):
    __tablename__ = 'community_material_ratings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('community_materials.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('user_id', 'material_id', name='_user_community_material_rating_uc'),)

    user = db.relationship('User', backref='community_ratings')
    material = db.relationship('CommunityMaterial', backref='ratings_rel')


class CommunityMaterialReport(db.Model):
    __tablename__ = 'community_material_reports'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('community_materials.id'), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('user_id', 'material_id', name='_user_community_material_report_uc'),)

    user = db.relationship('User', backref='community_reports')
    material = db.relationship('CommunityMaterial', backref='reports_rel')

