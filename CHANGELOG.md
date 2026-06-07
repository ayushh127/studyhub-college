# Changelog

All notable changes to the StudyHub College project will be documented in this file.

## [Unreleased]
- Implemented comprehensive visual frontend redesign across StudyHub College templates. Visual transformations cover public landing (`index.html`), about page (`about.html`), login (`login.html`), register (`register.html`), college registration/success views, student dashboard (`dashboard.html`), college onboarding selection (`select_college.html`), subjects explorer (`subjects.html`), subject details (`subject_details.html`), unit details (`unit_details.html`), PYQ directory (`pyqs.html`), PYQ details (`pyq_details.html`), community library hub (`community_list.html`), upload form (`community_upload.html`), edit form (`community_edit.html`), My Uploads (`community_my_uploads.html`), public uploader profile (`community_user_profile.html`), quiz start (`quiz_start.html`), quiz attempt portal (`quiz_attempt.html`), quiz result (`quiz_result.html`), review (`quiz_review.html`), notifications center (`notifications.html`), error pages (403, 404, 413, 500), and platform/college admin dashboards. Standardized fonts, spacing, shadows, and button transitions for a premium modern SaaS feel, completely purging Cormorant Garamond / serif typography in favor of the Inter sans-serif stack. Added interactive client-side search and filtering for the student PYQ directory.
- Implemented College Logo and Onboarding improvements:
  - Added `logo_path` column to both the `College` and `CollegeRequest` model database schemas.
  - Added support for optional college logo uploads on the public college registration request form, saving request logos securely in the uploads directory and transferring them to the `College` entity upon request approval.
  - Implemented manual college logo upload/validation (PNG, JPG, JPEG, WEBP; <= 2MB) inside Platform Admin creation and edit routes.
  - Added Platform Admin routes `GET /admin/colleges/<id>/edit` and `POST /admin/colleges/<id>/edit` to allow updating college details (name, code, city, state, address, contact email/phone, status, and logo).
  - Updated Platform Admin college directory and details views to feature Edit actions, thumbnails/initials, and clean UI buttons.
  - Added real-time client-side JS filter searching on student onboarding selection matching name, code, city, or state with empty-state messages.

### Fixed
- Fixed `NameError: name 'User' is not defined` when viewing a student uploader's public profile page by adding the missing import to `app/routes/student.py`.

### Added
- Implemented Phase 13 Step 1: Global design system CSS. Overhauled `app/static/css/style.css` to introduce the Indigo-Slate `:root` variables, sans-serif typography scales, modern layout helper classes (grid-3col, grid-responsive, empty-state), clean form field states, and upgraded responsive mobile bottom navigation elements.
- Implemented Phase 12: Edit & Delete Permissions Audit & Stabilization.
  - Added routes `GET /student/community/materials/<id>/edit`, `POST /student/community/materials/<id>/edit`, and `POST /student/community/materials/<id>/delete` for uploader content editing and soft-deleting (status set to `removed_by_uploader`). Enforced strict uploader ownership and active status restrictions.
  - Created `student/community_edit.html` template and added Edit/Remove buttons on the My Shared Materials list page and material details page templates.
  - Refined College Admin content deletion behaviors: soft-deletes subjects (`is_active = False`) and units (nullifies references in materials/PYQs/quizzes), unpublishes quizzes with student attempts instead of deleting, nullifies file references in quizzes on material/PYQ deletion, and purges physical files from disk.
  - Enforced active subject restrictions on student subject/unit details views to block access to deactivated content.
- Implemented Phase 10 Step 9: Community Uploader Profile. Added a new route `GET /student/community/users/<user_id>` and template `community_user_profile.html` to display a student's public community profile, showing their active uploads, total views, total likes, and average rating. Added profile links to the material details page, community list cards, and 'My Uploads' page for seamless navigation. Ensures privacy by only exposing non-sensitive data and hiding inactive materials.
- Implemented Phase 11 Step 6: Online Exam Style Quiz Attempt Layout. Redesigned `quiz_attempt.html` to feature a two-column layout on desktop and a compact, collapsible palette drawer on mobile. Added a sticky sidebar containing a timer, mode toggle (Learning/Exam), and an interactive question palette for quick navigation. Isolated question rendering using client-side JavaScript to display single questions sequentially with previous/next buttons while preserving full-form submission logic.
- Implemented auto mark-as-read and detail redirection for notifications. Added the `/student/notifications/<id>/open` endpoint which automatically logs a `NotificationRead` status entry before redirecting the student safely to the corresponding item's details view (study material detail, PYQ details, community details, or quiz start page) instead of initiating direct file downloads.
- Added a student-specific official study material details page (`/student/materials/<id>`) and template (`student/material_details.html`) showing unit/subject metadata, description, and download controls.
- Refined mobile student header to align StudyHub College logo on the left and notification bell plus compact circular profile dropdown on the top-right (no text links or redundant dropdown elements).
- Implemented Phase 11 Step 2: Mobile student navigation and Community Library mobile usability cleanup. Modified base layout `base.html` header to show only Brand, compact notification bell icon, and profile dropdown icon on mobile (hiding text links). Swapped "Alerts" bottom nav tab with a direct link to student "Quizzes" (bottom nav tabs: Home, Subjects, Community, Quizzes, Profile). Removed the redundant large Logout button from the student dashboard body (`dashboard.html`). In Community Library list page (`community_list.html`), collapsed the secondary filter controls group behind a toggle button on mobile, keeping search bar and chips row visible. Added quick filter chips (Latest, Most Liked, Top Rated, PDFs, Links) as rounded pills. Integrated client-side filtering script to hide/show community cards matching PDFs and Links selection via `file_filter` parameter. Added viewport display helper classes and responsive card padding modifiers in `style.css`.
- Implemented Phase 11 Step 1: Navbar Cleanup & Mobile UX Polish. Replaced the cluttered header navigation links with a compact layout, hiding student links on mobile. Designed a unified Profile Dropdown showing the user's name, role, profile link, My Uploads (if student), and Logout. Added a click-toggle JavaScript handler for mobile and touch devices. Updated the student mobile bottom navigation bar to display five actions: Home, Subjects, Community, Notifications, and Profile. Added student profile endpoint `/student/profile` and template `student/profile.html` showing subscriptions, uploads, and quiz attempt statistics. Removed inline serif (Cormorant Garamond) style overrides from student templates (dashboard, community list, my uploads, notifications, pyq details, pyqs, select college, subjects, unit details, quiz attempt).
- Implemented Phase 10 Step 8: Community Library UX and Counting Refinements. Added `CommunityMaterialView` model to track unique student views per material. Updated route `/student/community/materials/<id>` to increment views once per logged-in student. Modified `/student/community/materials/<id>/like` to support AJAX JSON response. Redesigned Like buttons in explorer list cards and details page to support instantaneous AJAX toggling with heart icons (♥/♡) without reloading. Added uploader notice banners and student access restrictions for non-active materials (hidden, under review, removed). Made titles clickable links on student My Uploads and Explorer list cards.
- Implemented Phase 10 Step 5: Interactions (Likes & Ratings) for Community Library. Added `POST /student/community/materials/<id>/like` and `POST /student/community/materials/<id>/rate` routes to `app/routes/student.py`. Updated `community_details.html` to display interactable rating drop-downs and like buttons. Integrated unique constraints to prevent duplicate entries and re-calculate average rating and counts dynamically.
- Implemented Phase 10 Step 3: Student Upload Material for Community Library. Added routes `/student/community/upload` and `/student/community/my-uploads` in `app/routes/student.py` and templates `community_upload.html` and `community_my_uploads.html`. Configured secure file saving under `uploads/community/` with Werkzeug's `secure_filename`. Integrated upload constraints (PDF format only, 5MB limit, and dual PDF or link requirement). Added working upload and listing navigation items.
- Implemented Phase 10 Step 2: Student Browsing & Searching for Community Library. Created student route `/student/community` in `app/routes/student.py` and browsing template `app/templates/student/community_list.html`. Integrated search, filtering by material type and college tags, and sorting options. Added link to student navigation header.
- Implemented Phase 10 Step 1: Database Setup for Community Library. Added `CommunityMaterial`, `CommunityMaterialLike`, `CommunityMaterialRating`, and `CommunityMaterialReport` models.
- Implemented Modern Minimal SaaS Redesign. Replaced the old cream/brown theme with a clean white/black/blue modern UI design system. Overwrote CSS variables in `style.css`, globally overridden serif/Cormorant Garamond styling with clean sans-serif/Inter font stacks, modernized buttons, borders, shadow cards, and form inputs. Removed decorative Cormorant Garamond Google Font references, and updated `UI_UX_GUIDE.md` design parameters.
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
# # #   P h a s e   1 0 :   S t e p   7   -   P l a t f o r m   A d m i n   M o d e r a t i o n 
 -   I m p l e m e n t e d   \ G E T   / a d m i n / c o m m u n i t y \   a n d   \ G E T   / a d m i n / c o m m u n i t y / q u e u e \   f o r   m o d e r a t i o n   o v e r v i e w . 
 -   A d d e d   a d m i n   m a t e r i a l   i n t e r a c t i o n   r o u t e s :   h i d e ,   r e s t o r e ,   a n d   r e m o v e . 
 -   A d d e d   t e m p l a t e s   f o r   t h e   m o d e r a t i o n   U I   ( \ c o m m u n i t y _ l i s t . h t m l \ ,   \ c o m m u n i t y _ q u e u e . h t m l \ ,   \ c o m m u n i t y _ r e p o r t s . h t m l \ ) . 
 -   I n c l u d e d   m o d e r a t i o n   a c t i o n s   i n   t h e   A u d i t   L o g .  
 