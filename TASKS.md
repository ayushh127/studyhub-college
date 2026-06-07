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

## Phase 9: Modern SaaS Redesign
- [x] Overwrite global stylesheet `app/static/css/style.css` with new color variables (white/black/blue)
- [x] Link Inter font family and remove Cormorant Garamond font from `base.html`
- [x] Add font-family overrides for inline styles in `style.css`
- [x] Modernize buttons, forms, navigation headers, cards, and bottom nav styles
- [x] Update `UI_UX_GUIDE.md` with new Modern Minimal SaaS style guide

## Phase 10: Community Library
- [x] Step 1: Database models setup (`CommunityMaterial`, `CommunityMaterialLike`, `CommunityMaterialRating`, `CommunityMaterialReport`)
- [x] Step 2: Student library list/search UI
- [x] Step 3: Upload material with PDF/link
- [x] Step 4: Material detail/view/download/copy link
- [x] Step 5: Likes and ratings
- [x] Step 6: Reports + moderation score
- [x] Step 7: Platform admin moderation queue
- [x] Step 8: UX and counting refinements (Unique views, AJAX toggle liking, security)
- [x] Step 9: Public uploader profile and all uploads by same student

## Phase 11: Navbar Cleanup & Mobile UX Polish
- [x] Step 1: Navbar cleanup + mobile-first student/community UI polish
  - [x] Compact top navbar on desktop viewports
  - [x] Unified hover/click profile dropdown with logout
  - [x] Student profile route `/student/profile` & template
  - [x] Mobile bottom-nav update (Home, Subjects, Community, Notifications, Profile)
  - [x] Responsive layout polishing (stacked filters, full-width forms, touch targets, hide mobile header clutter)
- [x] Step 2: Mobile student navigation and Community Library mobile usability cleanup
  - [x] Show notification bell and profile dropdown on mobile headers, hide text links
  - [x] Swap Alerts with Quizzes in student bottom nav (Home, Subjects, Community, Quizzes, Profile)
  - [x] Remove Logout button from student dashboard body
  - [x] Add search row, mobile filters toggle button, and quick chips row to Community Library
  - [x] Hide secondary filters by default on mobile under toggle button
  - [x] Add data attributes to community cards and implement client-side PDF/Link filter JS
- [x] Step 3: Student dashboard subject discovery & mobile nav deduplication
  - [x] Show only subscribed subjects on student dashboard
  - [x] Add empty state for unsubscribed subjects and 'Browse All Subjects' button
  - [x] Remove 'Profile' from mobile bottom navigation
- [x] Step 4: Compact mobile student header cleanup
  - [x] Align brand logo on the left and navigation menu on the right on mobile
  - [x] Place notification bell link with badges on the top-right before profile
  - [x] Make profile dropdown button circular/compact on mobile, hiding username and arrow
  - [x] Shrink header height on mobile student views
- [x] Step 5: Notification detail behavior and auto mark-as-read
  - [x] Create safe official material details view route and page for students
  - [x] Implement `/student/notifications/<id>/open` route
  - [x] Auto mark-as-read on notification click
  - [x] Redirect to detail views (materials, PYQs, community, quiz start) instead of direct downloads
- [x] Step 6: Online Exam Style Quiz Attempt Layout
  - [x] Implement two-column CSS layout for quiz attempts on desktop
  - [x] Sticky mode selector, timer, and question palette on sidebar
  - [x] Implement collapsible question palette drawer on mobile
  - [x] Isolate question rendering using JS for single-question views with next/previous buttons

## Phase 12: Edit & Delete Permissions Audit & Stabilization
- [x] Implement uploader edit community material routes (GET/POST) and validation in `app/routes/student.py`
- [x] Implement uploader soft-delete community material route (POST) in `app/routes/student.py`
- [x] Create uploader edit template `student/community_edit.html`
- [x] Add uploader Edit and Remove buttons on My Shared Materials list page and details view templates
- [x] Clean up cascading references in College Admin deletions (quizzes referencing study materials/PYQs, materials/PYQs/quizzes referencing units)
- [x] Implement quiz soft-delete/unpublish logic when student attempt records exist
- [x] Implement subject soft-delete/deactivation logic and restrict student access to active subjects/units
- [x] Document new community routes in `ROUTES.md`
- [x] Update Community Library design plan in `COMMUNITY_LIBRARY_PLAN.md`
- [x] Update design conventions in `UI_UX_GUIDE.md`
- [x] Update task list in `TASKS.md`
- [x] Update changelog in `CHANGELOG.md`

## Phase 13: UI/UX Redesign Plan
- [x] Formulate modern digital library/SaaS visual direction and layout conventions
- [x] Define design system metrics (palette, typography, spacing, inputs, buttons)
- [x] Plan student dashboard redesign (welcome, subscribed subjects empty states, quick access cards)
- [x] Plan college selection/onboarding flows and subject discovery redesign
- [x] Plan community library browsing/upload improvements and quiz attempt layouts
- [x] Establish lightweight library integration strategy (Alpine.js, HTMX)
- [x] Document structural implementation order and testing checkpoints in `UI_REDESIGN_PLAN.md`
- [x] Synchronize design guidelines in `UI_UX_GUIDE.md` and project/task logs

## Phase 14: Modern SaaS UI/UX Visual Transformation
- [x] Step 1: Global design system CSS (variables, buttons, cards, inputs, navigation, shadows in style.css)
- [x] Step 2: Redesign and polish HTML templates:
  - [x] Public landing (`index.html`) & About page (`about.html`)
  - [x] Login (`login.html`), Register (`register.html`), and College Registration/Success views
  - [x] Student Dashboard (`dashboard.html`) & Onboarding College selection (`select_college.html`)
  - [x] Subject explorer list (`subjects.html`), Subject details (`subject_details.html`), and Unit details (`unit_details.html`)
  - [x] PYQ list (`pyqs.html`), PYQ details (`pyq_details.html`), and Material details (`material_details.html`)
  - [x] Community Library hub (`community_list.html`), Upload form (`community_upload.html`), Edit form (`community_edit.html`), My Uploads (`community_my_uploads.html`), and Public Profile (`community_user_profile.html`)
  - [x] Quiz start page (`quiz_start.html`), Quiz Attempt portal (`quiz_attempt.html`), Quiz Result (`quiz_result.html`), and Review (`quiz_review.html`)
  - [x] Notifications center (`notifications.html`)
  - [x] Custom Error views (403, 404, 413, 500)
  - [x] Platform Admin dashboard (`admin/dashboard.html`) & College Admin dashboard (`college_admin/dashboard.html`)
  - [x] Platform Admin sidebars & College Admin sidebars / layouts

## Phase 15: College Onboarding & Selection Improvements
- [x] Step 1: Add `logo_path` field to the `College` model in `app/models.py`
- [x] Step 2: Configure logo uploads folder in `app/config.py` and `app/__init__.py`
- [x] Step 3: Write and execute migration script `migrate_college_logo.py` to update SQLite schema
- [x] Step 4: Implement secure endpoints for uploading (`/admin/colleges/<id>/logo`), removing (`/admin/colleges/<id>/logo/remove`), and serving (`/files/college-logos/<id>`) college logos
- [x] Step 5: Update manual college creation logic in `app/routes/admin.py` to handle optional logo uploads
- [x] Step 6: Add logo file input to `admin/college_form.html`
- [x] Step 7: Update Platform Admin views `admin/colleges.html` and `admin/college_details.html` to display logo thumbnails and manage logos
- [x] Step 8: Update Student select college page `student/select_college.html` to show logos and initials fallback avatars
- [x] Step 9: Add real-time JS client-side searching and filtering of colleges matching name, code, city, or state
- [x] Step 10: Implement responsive empty state warning on selection page
- [x] Step 11: Display selected college logo on the student dashboard welcome card banner
- [x] Step 12: Add `logo_path` field to `CollegeRequest` model and write/run `migrate_college_request_logo.py`
- [x] Step 13: Add optional logo upload to public college registration form and backend route
- [x] Step 14: Transfer request `logo_path` to `College` model on approval of college request
- [x] Step 15: Add `GET/POST /admin/colleges/<id>/edit` route to allow platform admins to edit all college details and replace logo
- [x] Step 16: Update Platform Admin views with "Edit College" buttons and links
- [x] Step 17: Verify local python code compiles cleanly
- [x] Step 18: Update system documentation (`ROUTES.md`, `UI_UX_GUIDE.md`, `CHANGELOG.md`, `DATABASE_SCHEMA.md`, `DEPLOYMENT_PYTHONANYWHERE_FREE.md`, `TASKS.md`) and walkthrough artifact

## Phase 16: Mobile UI Usability Fixes
- [x] Step 1: Make mobile header always compact and horizontal, showing brand on left and bell/avatar dropdown on right
- [x] Step 2: Hide secondary public text links from the mobile header, keeping only Brand and Login button
- [x] Step 3: Stack grid layouts and stats widgets vertically on mobile viewports
- [x] Step 4: Add a prominent "Browse All Subjects" button directly below subscribed subjects on student dashboard
- [x] Step 5: Overhaul Community Library search/filter on mobile (Search button visible beside input, gears-icon Filters toggle button, full width uploads button row)
- [x] Step 6: Make quiz attempt sidebar non-sticky on mobile to save vertical screen space
- [x] Step 7: Apply compact paddings/margins to quiz options labels and container cards on mobile viewports
- [x] Step 8: Verify Python files compile cleanly and no desktop styles are broken

## Phase 17: Database Migration Improvements
- [x] Step 1: Update `migrate_db.py` to support safe, idempotent database column alterations (e.g. `logo_path`) in SQLite
- [x] Step 2: Update `DEPLOYMENT_PYTHONANYWHERE_FREE.md` to document the simplified migration command
- [x] Step 3: Update `CHANGELOG.md` and `TASKS.md`