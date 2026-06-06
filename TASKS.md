# Tasks

This document tracks the granular development tasks for the StudyHub College MVP. AI Agents should update this file as tasks are completed.

## Phase 1: Project Initialization
- [x] Generate initial documentation files (README, AGENTS, PROJECT_PLAN, TASKS, CHANGELOG, DATABASE_SCHEMA, ROUTES, UI_UX_GUIDE, SETUP, FUTURE_AI_FEATURES)
- [x] Initialize Python virtual environment and requirements.txt (Optional/Depends on setup script)

## Phase 2: Application Structure & Configuration
- [x] Create folder structure (app, static, templates, uploads)
- [x] Create `app/__init__.py` for application factory
- [x] Create `app/config.py` for settings
- [x] Create `app/extensions.py` (db, login_manager, etc.)

## Phase 3: Database & Models
- [x] Define User, College, CollegeRequest models
- [x] Define Subject, Unit, StudyMaterial, PYQPaper models
- [x] Define Quiz, Question, QuestionOption models
- [x] Define QuizAttempt, AnswerSubmission, StudentProgress, AuditLog models

## Phase 4: Authentication & Roles
- [x] Implement decorators (`@admin_required`, `@college_admin_required`, `@student_required`)
- [x] Implement auth routes (login, register, logout)
- [x] Implement impersonation logic (store `original_admin_id` in session)

## Phase 5: Core Features
- [x] Platform Admin UI (Dashboards, Requests, Users, Audit Logs)
- [x] College Admin UI (Subjects, Units, Uploads, Quiz Maker)
- [x] Student UI (Dashboard, Content Viewer, Quiz Interface)
- [x] Quiz Engine (Learning Mode & Exam Mode logic)
- [x] Secure File Routing (`/files/...`)
- [x] **Phase 5: Core Features Implementation (Re-opened)**
  - [x] Implement Platform Admin Dashboard & flows.
  - [x] Implement College Admin Dashboard & flows (Units and PYQs pending, Quiz engine complete).
  - [x] Implement Student Dashboard & flows (Quiz attempts complete, Secure file viewing pending).
  - [x] Implement secure file serving (`app/routes/files.py`) with IDOR checks.

## Phase 6: Seed & Polish
- [x] Create seed script with example data
- [x] Test mobile responsiveness
- [x] Final bug fixes
- [x] Implement Student UX Refinements (Interactive quiz mode toggle, dashboard cards, available quizzes context, real-time subject search filter, smart return navigation)
- [x] **Phase 6: Seed Data & Testing (Re-opened)**
  - [x] Create seed script with example data and default accounts.
  - [x] Perform manual testing of core flows.
  - [x] Update `CHANGELOG.md` and `PROJECT_PLAN.md`.
  - [x] Implement custom Error Pages (403, 404, 500).
  - [x] Perform Final MVP Regression Review and Quality Pass.

## Emergency Stabilization
- [x] Recover lost files (student routes, templates)
- [x] Ensure app starts without errors
- [x] Compile and verify routes

## UI Refinement
- [x] Replace placeholder public pages (Landing, About, College Registration) with actual templates.
- [x] Replace auth pages (Login, Register, Forgot Password) with themed templates.

## Auth & Navigation Refinement
- [x] Implement unified login credentials display and instructions.
- [x] Ensure role-based routing and redirects on login.
- [x] Design a dynamic responsive header navbar in `base.html` for all roles.
- [x] Synchronize admin and college admin sidebars using shared components.
- [x] Add clear logout buttons on Student Dashboard and sidebars.
- [x] Create custom error templates (403, 404, 500) and register handlers.
- [x] Fix database integrity issue on `StudentProgress` creation.

## MVP Content Management Foundation
- [x] Implement Subject CRUD operations for college admins with ownership validation.
- [x] Implement Unit/Chapter CRUD operations for college admins.
- [x] Implement secure PDF upload, view, edit, and publication controls for Study Materials.
- [x] Implement secure PDF upload, view, edit, and publication controls for PYQ papers.
- [x] Establish secure download endpoints with strict file access validations in `files.py`.
- [x] Build student browsing layouts for active college subjects, subject details, and PYQs list.
- [x] Pre-populate seed data with example documents and media placeholders.

## Academic Hierarchy & Information Architecture Restructure
- [x] Restructured Subject Details views to only display subject-level resources (materials, PYQs, quizzes).
- [x] Created dedicated College Admin Unit Details page and route.
- [x] Implemented preselected fields and redirects for Quiz, Material, and PYQ uploads from Unit pages.
- [x] Added PYQ support to Student Unit details page and updated navigation with breadcrumbs.
- [x] Seeded both subject-level and unit-level resources in the SQLite database.

## Platform Admin Manual College Creation
- [x] Implement backend routes for listing, creating, viewing details, activating, and deactivating colleges.
- [x] Create administrative HTML templates (`colleges.html`, `college_details.html`, `college_form.html`, `settings.html`).
- [x] Update the Platform Admin sidebar layout with new dashboard items.

## Secure File Serving Validation
- [x] Integrate disk file existence check before streaming study materials or PYQs.
- [x] Implement audit logging for missing documents (`file_missing_on_disk`) inside secure routing.

## College Admin Creation Improvements
- [x] Integrate secure password hashing during public college registrations.
- [x] Allow Platform Admins to add multiple College Admins per college via `/admin/colleges/<id>/admins/create`.
- [x] Display all associated College Admins on the Platform Admin college details view.

## Platform Admin Flow & Demo Cleanup
- [x] Remove demo credentials from login page UI
- [x] Create `create_admin.py` script for secure platform admin creation
- [x] Add command-line arguments to `create_admin.py` for non-interactive scripting
- [x] Add Platform Admin creation form in the Admin Dashboard
- [x] Add audit log tracking for `platform_admin_created` actions
- [x] Restrict Platform Admin creation to `platform_admin` role only

## GitHub & Deployment Safety Cleanup
- [x] Create `.gitignore` to prevent committing virtual envs, SQLite DBs, and file uploads
- [x] Check database and uploads directories to verify no local files are committed
- [x] Verify no real passwords or sensitive credentials are hardcoded in app configuration
- [x] Add `.env.example` file with placeholder values
- [x] Verify `SECRET_KEY` reads from environment variables with fallback
- [x] Update documentation with deployment instructions and safety warnings

## Student Mobile UX Polish
- [x] Implement responsive layout column switching for student dashboard grid
- [x] Implement responsive layout column switching for student subject details grid
- [x] Create touch-friendly option labels for quiz attempt radio selectors
- [x] Offset fixed quiz submission sticky footer above the bottom navigation bar on mobile
- [x] Implement bottom navigation bar specifically for logged-in students on mobile viewports
- [x] Hide redundant student header links on mobile to save screen space
- [x] Implement auto-stacking behavior for result and review action button groups on small screens

## Phase 7: Subject-Wise Notifications
- [x] Implement `SubjectSubscription`, `Notification`, and `NotificationRead` database models in `app/models.py`
- [x] Create and run migration script for new database tables
- [x] Implement student endpoints (`/student/notifications`, read status actions, and subscription toggle) in `app/routes/student.py`
- [x] Add subscription action button on student subject details view
- [x] Add interactive bell notification counts pill to student layout header
- [x] Implement notifications list template (`student/notifications.html`)
- [x] Integrate trigger dispatch calls in College Admin material, PYQ, and quiz publishing routes
- [x] Conduct end-to-end verification checks for isolation and read states

## Phase 8: PythonAnywhere & PWA Support
- [x] Configure file upload size limit (5MB) in `app/config.py` and register custom 413 error handler
- [x] Create PWA `manifest.json` and minimal service worker `sw.js` in `app/static`
- [x] Link manifest and register service worker in base template `base.html`
- [x] Write step-by-step deployment guide `DEPLOYMENT_PYTHONANYWHERE_FREE.md` with git workflows
- [x] Write PWA installation guide `PWA_MOBILE_INSTALL_GUIDE.md` for iOS/Android
- [x] Update project documentation (README, SETUP, MVP_RELEASE_NOTES, PROJECT_PLAN, CHANGELOG)
