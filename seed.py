from app import create_app
from app.extensions import db
from app.models import User, College, Subject, Unit, Quiz, Question, QuestionOption, StudyMaterial, PYQPaper
import os

app = create_app()
parent_dir = os.path.abspath(os.path.dirname(__file__))

with app.app_context():
    # 1. Create database tables
    db.drop_all()
    db.create_all()

    # 2. Platform Admin
    platform_admin = User(
        full_name='Platform Admin',
        email='admin@studyhub.local',
        role='platform_admin'
    )
    platform_admin.set_password('admin123')
    db.session.add(platform_admin)
    db.session.commit()

    # 3. Example College
    example_college = College(
        name='Global Tech Institute',
        code='GTI',
        city='Metropolis',
        state='Tech State',
        address='123 Innovation Drive',
        contact_email='contact@gti.edu',
        contact_phone='1234567890',
        status='active',
        created_by_admin_id=platform_admin.id
    )
    db.session.add(example_college)
    db.session.commit()

    # 4. College Admin
    college_admin = User(
        full_name='College Admin GTI',
        email='collegeadmin@studyhub.local',
        role='college_admin',
        college_id=example_college.id
    )
    college_admin.set_password('admin123')
    db.session.add(college_admin)
    db.session.commit()

    # 5. Example Student
    student = User(
        full_name='Student Demo',
        email='student@studyhub.local',
        role='student',
        college_id=example_college.id
    )
    student.set_password('student123')
    db.session.add(student)
    db.session.commit()

    # 6. Example Subject
    subject = Subject(
        name='Introduction to Computer Science',
        code='CS101',
        college_id=example_college.id,
        created_by=college_admin.id
    )
    db.session.add(subject)
    db.session.commit()

    # 7. Example Unit
    unit = Unit(
        title='Basics of Programming',
        unit_number=1,
        subject_id=subject.id,
        created_by=college_admin.id
    )
    db.session.add(unit)
    db.session.commit()

    # Ensure directories exist
    os.makedirs(os.path.join(parent_dir, 'uploads', 'materials'), exist_ok=True)
    os.makedirs(os.path.join(parent_dir, 'uploads', 'pyqs'), exist_ok=True)
    
    # Create dummy PDF files
    dummy_mat_path = os.path.join(parent_dir, 'uploads', 'materials', 'dummy_lecture_notes.pdf')
    with open(dummy_mat_path, 'w') as f:
        f.write("%PDF-1.4 dummy lecture notes pdf contents")
        
    dummy_pyq_path = os.path.join(parent_dir, 'uploads', 'pyqs', 'dummy_exam_paper.pdf')
    with open(dummy_pyq_path, 'w') as f:
        f.write("%PDF-1.4 dummy exam paper pdf contents")

    # 7b. Example Study Material
    material = StudyMaterial(
        college_id=example_college.id,
        subject_id=subject.id,
        unit_id=unit.id,
        title='Lecture Notes: Introduction to Algorithms',
        description='Detailed analysis of programming constructs, logic, and basic sorting algorithms.',
        file_path='dummy_lecture_notes.pdf',
        file_type='pdf',
        uploaded_by=college_admin.id,
        is_published=True
    )
    db.session.add(material)
    
    # Subject-level study material (no unit_id)
    subject_material = StudyMaterial(
        college_id=example_college.id,
        subject_id=subject.id,
        unit_id=None,
        title='CS101 Course Syllabus & Guidelines',
        description='General syllabus outline, recommended reading, and evaluation guidelines.',
        file_path='dummy_lecture_notes.pdf',
        file_type='pdf',
        uploaded_by=college_admin.id,
        is_published=True
    )
    db.session.add(subject_material)
    
    # 7c. Example PYQ Paper
    pyq = PYQPaper(
        college_id=example_college.id,
        subject_id=subject.id,
        unit_id=unit.id,
        title='CS101 Mid-Sem Question Paper (2024)',
        year=2024,
        exam_type='mid_sem',
        file_path='dummy_exam_paper.pdf',
        uploaded_by=college_admin.id,
        is_published=True
    )
    db.session.add(pyq)
    
    # Subject-level PYQ (no unit_id)
    subject_pyq = PYQPaper(
        college_id=example_college.id,
        subject_id=subject.id,
        unit_id=None,
        title='CS101 Final Sem Question Paper (2023)',
        year=2023,
        exam_type='end_sem',
        file_path='dummy_exam_paper.pdf',
        uploaded_by=college_admin.id,
        is_published=True
    )
    db.session.add(subject_pyq)
    db.session.commit()

    # 8. Example Quiz & Questions
    quiz = Quiz(
        title='CS101 Unit 1 Test',
        college_id=example_college.id,
        subject_id=subject.id,
        unit_id=unit.id,
        quiz_type='practice',
        difficulty='easy',
        is_published=True,
        created_by=college_admin.id
    )
    db.session.add(quiz)
    
    # Subject-level quiz (no unit_id)
    subject_quiz = Quiz(
        title='CS101 General Mock Test',
        college_id=example_college.id,
        subject_id=subject.id,
        unit_id=None,
        quiz_type='subject_test',
        difficulty='medium',
        is_published=True,
        created_by=college_admin.id
    )
    db.session.add(subject_quiz)
    db.session.commit()

    # Q1
    q1 = Question(quiz_id=quiz.id, question_text='What is a variable in programming?', explanation='A variable is a named storage location in memory used to hold data.', marks=1, order_number=1)
    db.session.add(q1)
    db.session.commit()
    db.session.add(QuestionOption(question_id=q1.id, option_text='A box to store data', is_correct=True, order_number=1))
    db.session.add(QuestionOption(question_id=q1.id, option_text='A type of coffee', is_correct=False, order_number=2))
    db.session.add(QuestionOption(question_id=q1.id, option_text='A mathematical constant', is_correct=False, order_number=3))
    db.session.add(QuestionOption(question_id=q1.id, option_text='A computer hardware component', is_correct=False, order_number=4))
    
    # Q2
    q2 = Question(quiz_id=quiz.id, question_text='Which of the following is not a standard data type in Python?', explanation='List, Dictionary, and Tuple are standard Python data types. Array is typically provided by the array or numpy module, not a standard built-in type in the same way (though list is similar).', marks=2, order_number=2)
    db.session.add(q2)
    db.session.commit()
    db.session.add(QuestionOption(question_id=q2.id, option_text='List', is_correct=False, order_number=1))
    db.session.add(QuestionOption(question_id=q2.id, option_text='Dictionary', is_correct=False, order_number=2))
    db.session.add(QuestionOption(question_id=q2.id, option_text='Array', is_correct=True, order_number=3))
    db.session.add(QuestionOption(question_id=q2.id, option_text='Tuple', is_correct=False, order_number=4))
    
    # Q for subject-level quiz
    sq1 = Question(quiz_id=subject_quiz.id, question_text='What does CPU stand for?', explanation='CPU stands for Central Processing Unit.', marks=1, order_number=1)
    db.session.add(sq1)
    db.session.commit()
    db.session.add(QuestionOption(question_id=sq1.id, option_text='Central Processing Unit', is_correct=True, order_number=1))
    db.session.add(QuestionOption(question_id=sq1.id, option_text='Computer Personal Unit', is_correct=False, order_number=2))
    db.session.add(QuestionOption(question_id=sq1.id, option_text='Central Power Unit', is_correct=False, order_number=3))
    db.session.add(QuestionOption(question_id=sq1.id, option_text='Central Processor Utility', is_correct=False, order_number=4))

    db.session.commit()

    print("Database seeded successfully with example data!")
    print("Test credentials:")
    print("Platform Admin: admin@studyhub.local / admin123")
    print("College Admin : collegeadmin@studyhub.local / admin123")
    print("Student       : student@studyhub.local / student123")
