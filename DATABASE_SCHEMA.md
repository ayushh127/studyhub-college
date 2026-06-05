# Database Schema

The StudyHub College MVP uses SQLite (via Flask-SQLAlchemy). Below is the schema structure based on the project requirements.

## 1. User
- `id` (PK)
- `full_name`
- `email` (Unique)
- `password_hash`
- `role` (Enum: `platform_admin`, `college_admin`, `student`)
- `college_id` (FK to College, nullable for platform_admin)
- `is_active` (Boolean)
- `created_at`
- `updated_at`

## 2. College
- `id` (PK)
- `name`
- `code` (Unique)
- `city`
- `state`
- `address`
- `contact_email`
- `contact_phone`
- `status` (Enum: `active`, `inactive`, `pending`, `rejected`)
- `created_by_admin_id` (FK to User)
- `created_at`
- `updated_at`

## 3. CollegeRequest
- `id` (PK)
- `college_name`
- `college_code`
- `city`
- `state`
- `address`
- `admin_full_name`
- `admin_email`
- `admin_phone`
- `admin_password_hash`
- `message`
- `status` (Enum: `pending`, `approved`, `rejected`)
- `reviewed_by_admin_id` (FK to User)
- `reviewed_at`
- `created_at`

## 4. Subject
- `id` (PK)
- `college_id` (FK to College)
- `name`
- `code`
- `description`
- `semester`
- `is_active` (Boolean)
- `created_by` (FK to User)
- `created_at`
- `updated_at`

## 5. Unit
- `id` (PK)
- `subject_id` (FK to Subject)
- `title`
- `unit_number`
- `description`
- `created_by` (FK to User)
- `created_at`
- `updated_at`

## 6. StudyMaterial
- `id` (PK)
- `college_id` (FK to College)
- `subject_id` (FK to Subject)
- `unit_id` (FK to Unit)
- `title`
- `description`
- `file_path`
- `file_type` (Enum: `pdf`, `notes`, `assignment`, `important_questions`, `other`)
- `uploaded_by` (FK to User)
- `is_published` (Boolean)
- `created_at`
- `updated_at`

## 7. PYQPaper
- `id` (PK)
- `college_id` (FK to College)
- `subject_id` (FK to Subject)
- `unit_id` (FK to Unit, Nullable)
- `title`
- `year`
- `exam_type` (Enum: `mid_sem`, `end_sem`, `internal`, `practical`, `other`)
- `file_path`
- `uploaded_by` (FK to User)
- `is_published` (Boolean)
- `created_at`
- `updated_at`

## 8. Quiz
- `id` (PK)
- `college_id` (FK to College)
- `subject_id` (FK to Subject)
- `unit_id` (FK to Unit, Nullable)
- `study_material_id` (FK to StudyMaterial, Nullable)
- `pyq_paper_id` (FK to PYQPaper, Nullable)
- `title`
- `description`
- `quiz_type` (Enum: `practice`, `pyq`, `unit_test`, `subject_test`)
- `difficulty` (Enum: `easy`, `medium`, `hard`, `mixed`)
- `time_limit_minutes` (Integer, Nullable)
- `is_published` (Boolean)
- `created_by` (FK to User)
- `created_at`
- `updated_at`

## 9. Question
- `id` (PK)
- `quiz_id` (FK to Quiz)
- `question_text`
- `explanation`
- `marks`
- `order_number`
- `created_at`
- `updated_at`

## 10. QuestionOption
- `id` (PK)
- `question_id` (FK to Question)
- `option_text`
- `is_correct` (Boolean)
- `order_number`

## 11. QuizAttempt
- `id` (PK)
- `student_id` (FK to User)
- `quiz_id` (FK to Quiz)
- `mode` (Enum: `learning`, `exam`)
- `score`
- `total_marks`
- `percentage`
- `started_at`
- `submitted_at`
- `status` (Enum: `in_progress`, `submitted`, `abandoned`)

## 12. AnswerSubmission
- `id` (PK)
- `attempt_id` (FK to QuizAttempt)
- `question_id` (FK to Question)
- `selected_option_id` (FK to QuestionOption)
- `is_correct` (Boolean)
- `marks_awarded`
- `answered_at`

## 13. StudentProgress
- `id` (PK)
- `student_id` (FK to User)
- `college_id` (FK to College)
- `subject_id` (FK to Subject)
- `unit_id` (FK to Unit)
- `quizzes_attempted`
- `average_score`
- `best_score`
- `last_activity_at`
- `updated_at`

## 14. AuditLog
- `id` (PK)
- `actor_user_id` (FK to User, Nullable)
- `action`
- `target_type`
- `target_id`
- `details`
- `ip_address`
- `created_at`
