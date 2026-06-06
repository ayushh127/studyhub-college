# Changelog

All notable changes to the StudyHub College project will be documented in this file.

## [Unreleased]
### Added
- Implemented Phase 8: PythonAnywhere & PWA Support. Configured file upload size limits to 5MB, created custom 413 error templates, added PWA `manifest.json` and `sw.js` registration, generated solid-color placeholder icons, and wrote detailed hosting/installation guides.
- Implemented and verified Phase 7 Step 5: Notification E2E QA Verification. Validated all 17 target notification flows, resolved database subquery coercion SQL warnings, and documented results in `NOTIFICATION_QA_REPORT.md`.
- Implemented Phase 7 Step 4: Notification Dispatch Triggers. Added automatic in-app notification creation when college admins publish Study Materials, PYQ Papers, or Quizzes.
- Removed demo credentials from login page UI.
- Implemented student notifications UI components (header and bottom navigation bell alerts, dynamic unread badge count, subject-details subscribe/unsubscribe button, notifications list page, and mark read actions).
- Implemented student mobile-first UI/UX polish (responsive dashboard grids, responsive subject columns, touch-friendly radio option inputs, mobile sticky footer offset, full-width stacking action buttons, and student bottom navigation bar).
- Added `create_admin.py` script for secure platform admin creation.
- Added UI to create additional platform admins from the Admin Dashboard.
- Updated documentation with warnings regarding demo accounts.
- Added `.gitignore` and `.env.example` configurations for deployment security.
- Checked configuration to ensure environment variables are utilized for sensitive variables.
- Implemented secure password hashing and handling for the first college admin during public college registration.
- Added Platform Admin routes to create multiple College Admins per college (`/admin/colleges/<id>/admins/create`).
- Updated College Details page to list all College Admins linked to a specific college.
- Created `FINAL_MVP_QA_REPORT.md` following a comprehensive regression review.
- Implemented real-time subject search/filter on student subjects page (`student/subjects.html`) and college admin subjects page (`college_admin/subjects.html`).
- Created unified student quiz attempt page (`student/quiz_attempt.html`) featuring client-side mode toggling switcher (Learning vs Exam), "Show Answer" buttons, correct option highlighting, and question explanations.
- Added context-aware smart return navigation options (Back to Unit, Back to Subject, Retry Quiz, Review Answers) to student quiz result and review pages.
- Implemented Platform Admin manual college creation routes: `/admin/colleges`, `/admin/colleges/create`, `/admin/colleges/<id>`, `/admin/colleges/<id>/activate`, and `/admin/colleges/<id>/deactivate`.
- Added Platform Admin templates: colleges list (`colleges.html`), details view (`college_details.html`), registration form (`college_form.html`), and a placeholder settings page (`settings.html`).
- Implemented dedicated College Admin Unit Details view (`college_admin/unit_details.html`) displaying unit-specific resources and prefilled creation links.
- Added Student Unit Details page support for published unit-specific PYQs.
- Added dynamic breadcrumbs (`Dashboard -> Subjects -> Subject -> Unit`) across Subject and Unit detail views for both Admin and Student.
- Added disk-level file existence checks and logged missing files to the audit system before serving materials or PYQs.

### Changed
- Refined manual college creation by Platform Admins to automatically generate and assign a default College Admin account using the provided contact email.
- Added JavaScript auto-dismiss logic to global flash messages (timeout 5s) for cleaner UI experiences.
- Patched student dashboard subjects query to exclusively display active subjects.

### Changed
- Updated student dashboard subject cards to be fully clickable, supporting interactive hover scales and displaying dynamic stats (units, quizzes, and resources counts).
- Updated student dashboard quizzes list to "Available Quizzes", providing complete hierarchical context (Subject Name • Unit Details or Overall Quiz • Quiz Type • Difficulty).
- Refactored student backend routes in `app/routes/student.py` to leverage the unified client-side attempt template and handle submissions all-at-once.

### Changed
- Updated the Platform Admin sidebar navigation (`admin_sidebar.html`) with Colleges, Add College, and Settings links.
- Restructured information architecture from flat lists to a nested academic hierarchy (Subject -> Unit -> Resources).
- Filtered Subject detail views to only show subject-level resources (where unit_id is null).
- Integrated `preselected_subject_id` and `preselected_unit_id` parameters into Quiz, Study Material, and PYQ form creation routes.
- Added javascript-based dropdown unit filtering to the Quiz creation/edit forms.
- Re-seeded the SQLite database to include both subject-level and unit-level materials, PYQs, and quizzes.
- Implemented secure file serving endpoint (`app/routes/files.py`) supporting PDF download & view requests with strict login, role permissions, and publication controls.
- Implemented comprehensive college admin Subject CRUD pages (`subject_details.html`, `subject_form.html`, `subjects.html`).
- Implemented college admin Unit CRUD pages (`unit_form.html`) to link units with parent subjects.
- Implemented college admin Study Material upload and edit views (`material_form.html`, `material_details.html`) restricting uploads to safe PDF extensions.
- Implemented college admin PYQ Paper upload and edit views (`pyqs.html`, `pyq_form.html`, `pyq_details.html`) with year and exam type categorization.
- Implemented student course content browsing pages (`subjects.html`, `subject_details.html`, `unit_details.html`, `pyqs.html`, `pyq_details.html`) showing active college-specific published resources.
- Added programmatic seed generation of placeholder study materials and PYQ documents inside `seed.py` database setup.
- Added custom academic-themed error pages for HTTP 403, 404, and 500 statuses.
- Added shared sidebar component files for platform administrator (`admin_sidebar.html`) and college administrator (`college_admin_sidebar.html`).
- Added styled demo credentials callout block on the unified login form.

### Changed
- Added student navbar links to "Subjects" and "PYQs" in the global navigation layout.
- Integrated college-level ownership validations on all content editing, deleting, and publishing routes (preventing IDOR attacks).
- Implemented fully dynamic navigation header responding to the user's role status (Platform Admin, College Admin, Student).
- Integrated shared sidebar layouts across all platform administration and college administration views to synchronize user profile information and links.
- Rendered visible "Logout" buttons and student selected college badges on the student dashboard layout.

### Fixed
- Fixed broken redirect path reference (`main.index` corrected to `public.index`) in the student requirement check decorator.
- Fixed critical SQLite IntegrityError constraint failure inside `StudentProgress` database entries during quiz submissions by providing the active `college_id` argument.
- Improved media queries and responsive styling for the navbar wrap behavior and button layout on mobile viewports.

- Initial project documentation (README, AGENTS, PROJECT_PLAN, TASKS, CHANGELOG, DATABASE_SCHEMA, ROUTES, UI_UX_GUIDE, SETUP, FUTURE_AI_FEATURES).
- Flask application factory, database models, configuration.
- Base UI layouts with Classical Minimal Academic theme.
- Multi-role authentication (Admin, College Admin, Student) with Flask-Login.
- Admin dashboard, impersonation, and college request system.
- Basic College Admin dashboard with materials, subjects, and quiz metadata management.
- Basic Student dashboard with college selection.
- Complete SQLite seed dataset for demonstration.

### Changed
- Re-opened Phase 5 and Phase 6 tasks based on `MVP_TEST_REPORT.md` audit findings to address missing quiz engine logic, secure file serving, and remaining CRUD operations.
- Completed **Priority 1: Quiz Engine Core**: Added full quiz/question builder for college admins and learning/exam mode attempt engine for students.

### Fixed
- **Emergency Stabilization (June 2026):** Recovered `student.py` and all student-facing HTML templates (`dashboard.html`, `quizzes.html`, `quiz_start.html`, `quiz_attempt_learning.html`, `quiz_attempt_exam.html`, `quiz_result.html`, `quiz_review.html`, `select_college.html`) that were accidentally truncated during a bug fix attempt.
- Fixed blueprint registration conflict in `student.py`.
- Fixed missing ORM relationship attributes (`attempt.quiz_rel` and `attempt.answers`) across student route and templates.

### Changed
- Replaced public placeholder pages with real themed templates (index, about, college registration).
- Finalized auth page themes.
