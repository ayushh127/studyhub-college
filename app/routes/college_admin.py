from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import current_user
import os
from werkzeug.utils import secure_filename
from . import college_admin_bp
from ..models import Subject, Unit, StudyMaterial, PYQPaper, Quiz, User, College, Question, QuestionOption
from ..extensions import db
from ..utils.decorators import college_admin_required
from ..utils.audit import log_action

@college_admin_bp.before_request
@college_admin_required
def before_request():
    pass

@college_admin_bp.route('/dashboard')
def dashboard():
    stats = {
        'subjects': Subject.query.filter_by(college_id=current_user.college_id).count(),
        'materials': StudyMaterial.query.filter_by(college_id=current_user.college_id).count(),
        'quizzes': Quiz.query.filter_by(college_id=current_user.college_id).count(),
        'students': User.query.filter_by(college_id=current_user.college_id, role='student').count()
    }
    return render_template('college_admin/dashboard.html', stats=stats)

import time
from werkzeug.utils import secure_filename
from flask import abort

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'

@college_admin_bp.route('/subjects', methods=['GET'])
def subjects():
    subs = Subject.query.filter_by(college_id=current_user.college_id).all()
    return render_template('college_admin/subjects.html', subjects=subs)

@college_admin_bp.route('/subjects/create', methods=['GET', 'POST'])
def create_subject():
    if request.method == 'POST':
        name = request.form.get('name')
        code = request.form.get('code')
        description = request.form.get('description')
        semester = request.form.get('semester', type=int)
        
        subject = Subject(
            name=name,
            code=code,
            description=description,
            semester=semester,
            college_id=current_user.college_id,
            created_by=current_user.id
        )
        db.session.add(subject)
        db.session.commit()
        log_action(current_user.id, 'subject_created', 'subject', subject.id)
        flash('Subject created successfully.', 'success')
        return redirect(url_for('college_admin.subjects'))
    return render_template('college_admin/subject_form.html', subject=None)

@college_admin_bp.route('/subjects/<int:id>', methods=['GET'])
def subject_detail(id):
    subject = Subject.query.get_or_404(id)
    if subject.college_id != current_user.college_id:
        abort(403)
    materials = StudyMaterial.query.filter_by(subject_id=subject.id, unit_id=None).all()
    pyqs = PYQPaper.query.filter_by(subject_id=subject.id, unit_id=None).all()
    quizzes = Quiz.query.filter_by(subject_id=subject.id, unit_id=None).all()
    return render_template('college_admin/subject_details.html', subject=subject, materials=materials, pyqs=pyqs, quizzes=quizzes)

@college_admin_bp.route('/subjects/<int:id>/edit', methods=['GET', 'POST'])
def edit_subject(id):
    subject = Subject.query.get_or_404(id)
    if subject.college_id != current_user.college_id:
        abort(403)
        
    if request.method == 'POST':
        subject.name = request.form.get('name')
        subject.code = request.form.get('code')
        subject.description = request.form.get('description')
        subject.semester = request.form.get('semester', type=int)
        
        db.session.commit()
        log_action(current_user.id, 'subject_updated', 'subject', subject.id)
        flash('Subject updated successfully.', 'success')
        return redirect(url_for('college_admin.subject_detail', id=subject.id))
    return render_template('college_admin/subject_form.html', subject=subject)

@college_admin_bp.route('/subjects/<int:id>/delete', methods=['POST'])
def delete_subject(id):
    subject = Subject.query.get_or_404(id)
    if subject.college_id != current_user.college_id:
        abort(403)
        
    db.session.delete(subject)
    db.session.commit()
    log_action(current_user.id, 'subject_deleted', 'subject', id)
    flash('Subject deleted successfully.', 'success')
    return redirect(url_for('college_admin.subjects'))

# Units CRUD
@college_admin_bp.route('/subjects/<int:subject_id>/units/create', methods=['GET', 'POST'])
def create_unit(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    if subject.college_id != current_user.college_id:
        abort(403)
        
    if request.method == 'POST':
        title = request.form.get('title')
        unit_number = request.form.get('unit_number', type=int)
        description = request.form.get('description')
        
        unit = Unit(
            subject_id=subject.id,
            title=title,
            unit_number=unit_number,
            description=description,
            created_by=current_user.id
        )
        db.session.add(unit)
        db.session.commit()
        log_action(current_user.id, 'unit_created', 'unit', unit.id)
        flash('Unit created successfully.', 'success')
        return redirect(url_for('college_admin.subject_detail', id=subject.id))
    return render_template('college_admin/unit_form.html', subject=subject, unit=None)

@college_admin_bp.route('/units/<int:id>', methods=['GET'])
def unit_detail(id):
    unit = Unit.query.get_or_404(id)
    if unit.subject.college_id != current_user.college_id:
        abort(403)
    # Get materials, PYQs, and quizzes for this unit
    materials = StudyMaterial.query.filter_by(unit_id=unit.id).all()
    pyqs = PYQPaper.query.filter_by(unit_id=unit.id).all()
    quizzes = Quiz.query.filter_by(unit_id=unit.id).all()
    return render_template('college_admin/unit_details.html', unit=unit, materials=materials, pyqs=pyqs, quizzes=quizzes)

@college_admin_bp.route('/units/<int:id>/edit', methods=['GET', 'POST'])
def edit_unit(id):
    unit = Unit.query.get_or_404(id)
    if unit.subject.college_id != current_user.college_id:
        abort(403)
        
    if request.method == 'POST':
        unit.title = request.form.get('title')
        unit.unit_number = request.form.get('unit_number', type=int)
        unit.description = request.form.get('description')
        
        db.session.commit()
        log_action(current_user.id, 'unit_updated', 'unit', unit.id)
        flash('Unit updated successfully.', 'success')
        return redirect(url_for('college_admin.subject_detail', id=unit.subject_id))
    return render_template('college_admin/unit_form.html', subject=unit.subject, unit=unit)

@college_admin_bp.route('/units/<int:id>/delete', methods=['POST'])
def delete_unit(id):
    unit = Unit.query.get_or_404(id)
    if unit.subject.college_id != current_user.college_id:
        abort(403)
    subject_id = unit.subject_id
    
    db.session.delete(unit)
    db.session.commit()
    log_action(current_user.id, 'unit_deleted', 'unit', id)
    flash('Unit deleted successfully.', 'success')
    return redirect(url_for('college_admin.subject_detail', id=subject_id))

# Study Materials CRUD
@college_admin_bp.route('/materials', methods=['GET'])
def materials():
    mats = StudyMaterial.query.filter_by(college_id=current_user.college_id).all()
    return render_template('college_admin/materials.html', materials=mats)

@college_admin_bp.route('/materials/upload', methods=['GET', 'POST'])
def upload_material():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
            
        subject_id = request.form.get('subject_id', type=int)
        unit_id = request.form.get('unit_id', type=int)
        unit_id = unit_id if unit_id else None
        title = request.form.get('title')
        description = request.form.get('description')
        file_type = request.form.get('file_type', 'pdf')
        
        subject = Subject.query.get_or_404(subject_id)
        if subject.college_id != current_user.college_id:
            abort(403)
            
        if unit_id:
            unit = Unit.query.get_or_404(unit_id)
            if unit.subject_id != subject.id:
                abort(403)
                
        if file and allowed_file(file.filename):
            filename = secure_filename(f"{int(time.time())}_{file.filename}")
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER_MATERIALS'], filename)
            file.save(filepath)
            
            mat = StudyMaterial(
                college_id=current_user.college_id,
                subject_id=subject.id,
                unit_id=unit_id,
                title=title,
                description=description,
                file_path=filename,
                file_type=file_type,
                uploaded_by=current_user.id,
                is_published=False
            )
            db.session.add(mat)
            db.session.commit()
            log_action(current_user.id, 'material_uploaded', 'study_material', mat.id)
            flash('Material uploaded successfully as draft.', 'success')
            if unit_id:
                return redirect(url_for('college_admin.unit_detail', id=unit_id))
            return redirect(url_for('college_admin.subject_detail', id=subject.id))
        else:
            flash('Only PDF files are allowed.', 'danger')
            
    subs = Subject.query.filter_by(college_id=current_user.college_id).all()
    units = Unit.query.join(Subject).filter(Subject.college_id == current_user.college_id).all()
    preselected_subject_id = request.args.get('subject_id', type=int)
    preselected_unit_id = request.args.get('unit_id', type=int)
    return render_template('college_admin/material_form.html', subjects=subs, units=units, material=None,
                           preselected_subject_id=preselected_subject_id, preselected_unit_id=preselected_unit_id)

@college_admin_bp.route('/materials/<int:id>', methods=['GET'])
def material_detail(id):
    material = StudyMaterial.query.get_or_404(id)
    if material.college_id != current_user.college_id:
        abort(403)
    return render_template('college_admin/material_details.html', material=material)

@college_admin_bp.route('/materials/<int:id>/edit', methods=['GET', 'POST'])
def edit_material(id):
    material = StudyMaterial.query.get_or_404(id)
    if material.college_id != current_user.college_id:
        abort(403)
        
    if request.method == 'POST':
        material.title = request.form.get('title')
        material.description = request.form.get('description')
        material.subject_id = request.form.get('subject_id', type=int)
        unit_id = request.form.get('unit_id', type=int)
        material.unit_id = unit_id if unit_id else None
        material.file_type = request.form.get('file_type', 'pdf')
        
        subject = Subject.query.get_or_404(material.subject_id)
        if subject.college_id != current_user.college_id:
            abort(403)
            
        if material.unit_id:
            unit = Unit.query.get_or_404(material.unit_id)
            if unit.subject_id != subject.id:
                abort(403)
                
        file = request.files.get('file')
        if file and file.filename != '':
            if allowed_file(file.filename):
                filename = secure_filename(f"{int(time.time())}_{file.filename}")
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER_MATERIALS'], filename)
                file.save(filepath)
                material.file_path = filename
            else:
                flash('Only PDF files are allowed.', 'danger')
                return redirect(request.url)
                
        db.session.commit()
        log_action(current_user.id, 'material_updated', 'study_material', material.id)
        flash('Material details updated successfully.', 'success')
        return redirect(url_for('college_admin.material_detail', id=material.id))
        
    subs = Subject.query.filter_by(college_id=current_user.college_id).all()
    units = Unit.query.join(Subject).filter(Subject.college_id == current_user.college_id).all()
    return render_template('college_admin/material_form.html', subjects=subs, units=units, material=material)

@college_admin_bp.route('/materials/<int:id>/delete', methods=['POST'])
def delete_material(id):
    material = StudyMaterial.query.get_or_404(id)
    if material.college_id != current_user.college_id:
        abort(403)
        
    db.session.delete(material)
    db.session.commit()
    log_action(current_user.id, 'material_deleted', 'study_material', id)
    flash('Material deleted successfully.', 'success')
    return redirect(url_for('college_admin.materials'))

@college_admin_bp.route('/materials/<int:id>/publish', methods=['POST'])
def publish_material(id):
    material = StudyMaterial.query.get_or_404(id)
    if material.college_id != current_user.college_id:
        abort(403)
        
    material.is_published = True
    db.session.commit()
    log_action(current_user.id, 'material_published', 'study_material', material.id)
    flash('Material published successfully.', 'success')
    return redirect(url_for('college_admin.material_detail', id=material.id))

@college_admin_bp.route('/materials/<int:id>/unpublish', methods=['POST'])
def unpublish_material(id):
    material = StudyMaterial.query.get_or_404(id)
    if material.college_id != current_user.college_id:
        abort(403)
        
    material.is_published = False
    db.session.commit()
    log_action(current_user.id, 'material_unpublished', 'study_material', material.id)
    flash('Material unpublished successfully.', 'success')
    return redirect(url_for('college_admin.material_detail', id=material.id))

# PYQs CRUD
@college_admin_bp.route('/pyqs', methods=['GET'])
def pyqs():
    pyqs_list = PYQPaper.query.filter_by(college_id=current_user.college_id).all()
    return render_template('college_admin/pyqs.html', pyqs=pyqs_list)

@college_admin_bp.route('/pyqs/upload', methods=['GET', 'POST'])
def upload_pyq():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
            
        subject_id = request.form.get('subject_id', type=int)
        unit_id = request.form.get('unit_id', type=int)
        unit_id = unit_id if unit_id else None
        title = request.form.get('title')
        year = request.form.get('year', type=int)
        exam_type = request.form.get('exam_type', 'end_sem')
        
        subject = Subject.query.get_or_404(subject_id)
        if subject.college_id != current_user.college_id:
            abort(403)
            
        if unit_id:
            unit = Unit.query.get_or_404(unit_id)
            if unit.subject_id != subject.id:
                abort(403)
                
        if file and allowed_file(file.filename):
            filename = secure_filename(f"{int(time.time())}_{file.filename}")
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER_PYQS'], filename)
            file.save(filepath)
            
            pyq = PYQPaper(
                college_id=current_user.college_id,
                subject_id=subject.id,
                unit_id=unit_id,
                title=title,
                year=year,
                exam_type=exam_type,
                file_path=filename,
                uploaded_by=current_user.id,
                is_published=False
            )
            db.session.add(pyq)
            db.session.commit()
            log_action(current_user.id, 'pyq_uploaded', 'pyq_paper', pyq.id)
            flash('PYQ uploaded successfully as draft.', 'success')
            if unit_id:
                return redirect(url_for('college_admin.unit_detail', id=unit_id))
            return redirect(url_for('college_admin.subject_detail', id=subject.id))
        else:
            flash('Only PDF files are allowed.', 'danger')
            
    subs = Subject.query.filter_by(college_id=current_user.college_id).all()
    units = Unit.query.join(Subject).filter(Subject.college_id == current_user.college_id).all()
    preselected_subject_id = request.args.get('subject_id', type=int)
    preselected_unit_id = request.args.get('unit_id', type=int)
    return render_template('college_admin/pyq_form.html', subjects=subs, units=units, pyq=None,
                           preselected_subject_id=preselected_subject_id, preselected_unit_id=preselected_unit_id)

@college_admin_bp.route('/pyqs/<int:id>', methods=['GET'])
def pyq_detail(id):
    pyq = PYQPaper.query.get_or_404(id)
    if pyq.college_id != current_user.college_id:
        abort(403)
    return render_template('college_admin/pyq_details.html', pyq=pyq)

@college_admin_bp.route('/pyqs/<int:id>/edit', methods=['GET', 'POST'])
def edit_pyq(id):
    pyq = PYQPaper.query.get_or_404(id)
    if pyq.college_id != current_user.college_id:
        abort(403)
        
    if request.method == 'POST':
        pyq.title = request.form.get('title')
        pyq.year = request.form.get('year', type=int)
        pyq.exam_type = request.form.get('exam_type')
        pyq.subject_id = request.form.get('subject_id', type=int)
        unit_id = request.form.get('unit_id', type=int)
        pyq.unit_id = unit_id if unit_id else None
        
        subject = Subject.query.get_or_404(pyq.subject_id)
        if subject.college_id != current_user.college_id:
            abort(403)
            
        if pyq.unit_id:
            unit = Unit.query.get_or_404(pyq.unit_id)
            if unit.subject_id != subject.id:
                abort(403)
                
        file = request.files.get('file')
        if file and file.filename != '':
            if allowed_file(file.filename):
                filename = secure_filename(f"{int(time.time())}_{file.filename}")
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER_PYQS'], filename)
                file.save(filepath)
                pyq.file_path = filename
            else:
                flash('Only PDF files are allowed.', 'danger')
                return redirect(request.url)
                
        db.session.commit()
        log_action(current_user.id, 'pyq_updated', 'pyq_paper', pyq.id)
        flash('PYQ updated successfully.', 'success')
        return redirect(url_for('college_admin.pyq_detail', id=pyq.id))
        
    subs = Subject.query.filter_by(college_id=current_user.college_id).all()
    units = Unit.query.join(Subject).filter(Subject.college_id == current_user.college_id).all()
    return render_template('college_admin/pyq_form.html', subjects=subs, units=units, pyq=pyq)

@college_admin_bp.route('/pyqs/<int:id>/delete', methods=['POST'])
def delete_pyq(id):
    pyq = PYQPaper.query.get_or_404(id)
    if pyq.college_id != current_user.college_id:
        abort(403)
        
    db.session.delete(pyq)
    db.session.commit()
    log_action(current_user.id, 'pyq_deleted', 'pyq_paper', id)
    flash('PYQ deleted successfully.', 'success')
    return redirect(url_for('college_admin.pyqs'))

@college_admin_bp.route('/pyqs/<int:id>/publish', methods=['POST'])
def publish_pyq(id):
    pyq = PYQPaper.query.get_or_404(id)
    if pyq.college_id != current_user.college_id:
        abort(403)
        
    pyq.is_published = True
    db.session.commit()
    log_action(current_user.id, 'pyq_published', 'pyq_paper', pyq.id)
    flash('PYQ published successfully.', 'success')
    return redirect(url_for('college_admin.pyq_detail', id=pyq.id))

@college_admin_bp.route('/pyqs/<int:id>/unpublish', methods=['POST'])
def unpublish_pyq(id):
    pyq = PYQPaper.query.get_or_404(id)
    if pyq.college_id != current_user.college_id:
        abort(403)
        
    pyq.is_published = False
    db.session.commit()
    log_action(current_user.id, 'pyq_unpublished', 'pyq_paper', pyq.id)
    flash('PYQ unpublished successfully.', 'success')
    return redirect(url_for('college_admin.pyq_detail', id=pyq.id))


@college_admin_bp.route('/quizzes', methods=['GET'])
def quizzes():
    quizzes_list = Quiz.query.filter_by(college_id=current_user.college_id).all()
    return render_template('college_admin/quizzes.html', quizzes=quizzes_list)

@college_admin_bp.route('/quizzes/create', methods=['GET', 'POST'])
def create_quiz():
    if request.method == 'POST':
        title = request.form.get('title')
        subject_id = request.form.get('subject_id')
        unit_id = request.form.get('unit_id') or None
        study_material_id = request.form.get('study_material_id') or None
        pyq_paper_id = request.form.get('pyq_paper_id') or None
        quiz_type = request.form.get('quiz_type', 'practice')
        difficulty = request.form.get('difficulty', 'medium')
        time_limit_minutes = request.form.get('time_limit_minutes') or None
        
        subject = Subject.query.get_or_404(subject_id)
        if subject.college_id != current_user.college_id:
            abort(403)
            
        if unit_id:
            unit = Unit.query.get_or_404(unit_id)
            if unit.subject_id != subject.id:
                abort(403)
                
        quiz = Quiz(
            college_id=current_user.college_id,
            subject_id=subject.id,
            unit_id=unit_id,
            study_material_id=study_material_id,
            pyq_paper_id=pyq_paper_id,
            title=title,
            quiz_type=quiz_type,
            difficulty=difficulty,
            time_limit_minutes=int(time_limit_minutes) if time_limit_minutes else None,
            created_by=current_user.id,
            is_published=False
        )
        db.session.add(quiz)
        db.session.commit()
        log_action(current_user.id, 'quiz_created', 'quiz', quiz.id)
        flash('Quiz created successfully.', 'success')
        return redirect(url_for('college_admin.quiz_details', id=quiz.id))
        
    subjects = Subject.query.filter_by(college_id=current_user.college_id).all()
    units = Unit.query.join(Subject).filter(Subject.college_id == current_user.college_id).all()
    preselected_subject_id = request.args.get('subject_id', type=int)
    preselected_unit_id = request.args.get('unit_id', type=int)
    return render_template('college_admin/quiz_form.html', subjects=subjects, units=units, quiz=None,
                           preselected_subject_id=preselected_subject_id, preselected_unit_id=preselected_unit_id)

@college_admin_bp.route('/quizzes/<int:id>', methods=['GET'])
def quiz_details(id):
    quiz = Quiz.query.filter_by(id=id, college_id=current_user.college_id).first_or_404()
    return render_template('college_admin/quiz_details.html', quiz=quiz)

@college_admin_bp.route('/quizzes/<int:id>/edit', methods=['GET', 'POST'])
def edit_quiz(id):
    quiz = Quiz.query.filter_by(id=id, college_id=current_user.college_id).first_or_404()
    if request.method == 'POST':
        quiz.title = request.form.get('title')
        quiz.subject_id = request.form.get('subject_id')
        unit_id = request.form.get('unit_id') or None
        quiz.unit_id = unit_id if unit_id else None
        quiz.study_material_id = request.form.get('study_material_id') or None
        quiz.pyq_paper_id = request.form.get('pyq_paper_id') or None
        quiz.quiz_type = request.form.get('quiz_type')
        quiz.difficulty = request.form.get('difficulty')
        time_limit = request.form.get('time_limit_minutes')
        quiz.time_limit_minutes = int(time_limit) if time_limit else None
        
        subject = Subject.query.get_or_404(quiz.subject_id)
        if subject.college_id != current_user.college_id:
            abort(403)
            
        if quiz.unit_id:
            unit = Unit.query.get_or_404(quiz.unit_id)
            if unit.subject_id != subject.id:
                abort(403)
                
        db.session.commit()
        flash('Quiz updated.', 'success')
        return redirect(url_for('college_admin.quiz_details', id=quiz.id))
        
    subjects = Subject.query.filter_by(college_id=current_user.college_id).all()
    units = Unit.query.join(Subject).filter(Subject.college_id == current_user.college_id).all()
    return render_template('college_admin/quiz_form.html', subjects=subjects, units=units, quiz=quiz)

@college_admin_bp.route('/quizzes/<int:id>/delete', methods=['POST'])
def delete_quiz(id):
    quiz = Quiz.query.filter_by(id=id, college_id=current_user.college_id).first_or_404()
    db.session.delete(quiz)
    db.session.commit()
    flash('Quiz deleted.', 'success')
    return redirect(url_for('college_admin.quizzes'))

@college_admin_bp.route('/quizzes/<int:id>/publish', methods=['POST'])
def publish_quiz(id):
    quiz = Quiz.query.filter_by(id=id, college_id=current_user.college_id).first_or_404()
    if not quiz.questions:
        flash('Cannot publish a quiz with 0 questions.', 'danger')
        return redirect(url_for('college_admin.quiz_details', id=quiz.id))
    
    quiz.is_published = True
    db.session.commit()
    flash('Quiz published.', 'success')
    return redirect(url_for('college_admin.quiz_details', id=quiz.id))

@college_admin_bp.route('/quizzes/<int:id>/unpublish', methods=['POST'])
def unpublish_quiz(id):
    quiz = Quiz.query.filter_by(id=id, college_id=current_user.college_id).first_or_404()
    quiz.is_published = False
    db.session.commit()
    flash('Quiz unpublished.', 'success')
    return redirect(url_for('college_admin.quiz_details', id=quiz.id))

@college_admin_bp.route('/quizzes/<int:quiz_id>/questions/create', methods=['GET', 'POST'])
def create_question(quiz_id):
    quiz = Quiz.query.filter_by(id=quiz_id, college_id=current_user.college_id).first_or_404()
    if request.method == 'POST':
        question_text = request.form.get('question_text')
        explanation = request.form.get('explanation')
        marks = request.form.get('marks', 1, type=int)
        order_number = request.form.get('order_number', len(quiz.questions) + 1, type=int)
        
        q = Question(quiz_id=quiz.id, question_text=question_text, explanation=explanation, marks=marks, order_number=order_number)
        db.session.add(q)
        db.session.commit() # Get q.id
        
        # Expect options to be submitted as lists
        option_texts = request.form.getlist('option_text[]')
        correct_index = request.form.get('correct_option_index', type=int)
        
        for i, text in enumerate(option_texts):
            is_correct = (i == correct_index)
            opt = QuestionOption(question_id=q.id, option_text=text, is_correct=is_correct, order_number=i+1)
            db.session.add(opt)
            
        db.session.commit()
        flash('Question added.', 'success')
        return redirect(url_for('college_admin.quiz_details', id=quiz.id))
        
    return render_template('college_admin/question_form.html', quiz=quiz, question=None)

@college_admin_bp.route('/questions/<int:id>/edit', methods=['GET', 'POST'])
def edit_question(id):
    question = Question.query.join(Quiz).filter(Question.id == id, Quiz.college_id == current_user.college_id).first_or_404()
    quiz = question.quiz
    
    if request.method == 'POST':
        question.question_text = request.form.get('question_text')
        question.explanation = request.form.get('explanation')
        question.marks = request.form.get('marks', 1, type=int)
        question.order_number = request.form.get('order_number', type=int)
        
        # Update options (assume they send option_id[] and option_text[])
        option_ids = request.form.getlist('option_id[]')
        option_texts = request.form.getlist('option_text[]')
        correct_index = request.form.get('correct_option_index', type=int)
        
        for i, opt_id in enumerate(option_ids):
            opt = QuestionOption.query.get(int(opt_id))
            if opt and opt.question_id == question.id:
                opt.option_text = option_texts[i]
                opt.is_correct = (i == correct_index)
                opt.order_number = i + 1
                
        db.session.commit()
        flash('Question updated.', 'success')
        return redirect(url_for('college_admin.quiz_details', id=quiz.id))
        
    return render_template('college_admin/question_form.html', quiz=quiz, question=question)

@college_admin_bp.route('/questions/<int:id>/delete', methods=['POST'])
def delete_question(id):
    question = Question.query.join(Quiz).filter(Question.id == id, Quiz.college_id == current_user.college_id).first_or_404()
    quiz_id = question.quiz_id
    db.session.delete(question)
    db.session.commit()
    flash('Question deleted.', 'success')
    return redirect(url_for('college_admin.quiz_details', id=quiz_id))
