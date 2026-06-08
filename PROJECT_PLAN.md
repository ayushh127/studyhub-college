# Project Plan

## Overview
Build the StudyHub College MVP, a multi-role web platform for college content management and student test preparation.

## Milestones

### Phase 1: Foundation (Current)
- [x] Create project documentation (README, AGENTS, etc.)
- [x] Setup Flask application structure
- [x] Configure database models (SQLAlchemy)
- [x] Implement UI/UX base theme (CSS)

### Phase 2: Authentication & Core Setup
- [x] Setup User roles (Platform Admin, College Admin, Student)
- [x] Implement registration and login flows
- [x] Setup role-based access control and impersonation mechanism

### Phase 3: College Admin Features
- [x] College registration request flow
- [x] Subject and Unit management
- [x] Material and PYQ file upload/management
- [x] Manual quiz creation (MCQ)

### Phase 4: Student Features
- [x] College selection
- [x] Content browsing (Subjects, Units, Materials, PYQs)
- [x] Quiz attempts (Learning Mode & Exam Mode)
- [x] Score and progress tracking

### Phase 5: Platform Admin Features & Finalization
- [x] Admin dashboards (Colleges, Users, Approvals)
- [x] Audit Logging display
- [x] Seed script for demo data
- [x] End-to-end testing

### Phase 7: Notifications (Completed)
- [x] Implement SubjectSubscription, Notification, and NotificationRead database models
- [x] Build student notification listing, toggle, and read routes
- [x] Design header bell count badge and notification lists template
- [x] Hook content publisher routes to trigger notifications

## Status
- **Current Status:** Version 1 Stable Release. All planned Jinja/Flask core features, onboarding wizards, mobile polishes, security audits, and notification timing fixes are fully implemented, verified, and locked.
- **V2 Roadmap:** Initiating Version 2 React frontend migration. This migration will proceed page-by-page to keep the system continuously stable. The first page targeted for React refactoring is the student dashboard.

### Phase 10: Community Library
- [x] Step 1: Database models setup (`CommunityMaterial`, `CommunityMaterialLike`, `CommunityMaterialRating`, `CommunityMaterialReport`)
- [x] Step 2: Student library list/search UI
- [x] Step 3: Upload material with PDF/link
- [x] Step 4: Material detail/view/download/copy link
- [x] Step 5: Likes and ratings
- [x] Step 6: Reports + moderation score
- [x] Step 7: Platform admin moderation queue
- [x] Step 8: UX and counting refinements (Unique views, AJAX toggle liking, security)

### Phase 11: Navbar Cleanup & Mobile UX Polish
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

## Emergency Stabilization
- App was stabilized to ensure all routes and templates run without errors.
- No further feature work will be conducted until confirmed stable.

## UI Refinement
- Implemented public/auth pages with Classical Minimal Academic theme.

## Auth & Navigation Refinement
- Resolved unified login layouts, role-based redirects, dynamic header navbars, and sidebars.
- Resolved database IntegrityError for new student progress creation during quiz submissions.
- Enhanced College Admin creation flow: Secure password handling during public registration and ability for Platform Admins to create multiple college admins per college.

## MVP Content Management Foundation
- Implemented full Subject CRUD, Unit CRUD, Study Material PDF Upload & CRUD, and PYQ PDF Upload & CRUD.
- Enforced backend-level ownership validation checks on all detail/edit/delete/publish routes.
- Securely streamed files using strict permission rules inside files routing, avoiding exposure of upload folders.
- Implemented student course subjects directory, subject units, PYQs browser, and document views.

## Academic Hierarchy & Information Architecture Restructure
- Restructured information architecture from flat pages to a nested academic hierarchy: Subject -> Unit -> Resources.
- Added College Admin Unit Details page and route, and updated Student Unit Details page.
- Prefilled forms and handled context-aware redirects when creating resources from specific units.
- Refined navigation with academic breadcrumbs across subject and unit detail views.

## Platform Admin Manual College Creation
- Implemented manual college registration endpoints for listing, creating, and viewing details of colleges.
- Added activate/deactivate action controls for colleges to manage system-wide access.
- Expanded sidebar components with direct access links to all colleges and settings pages.

## Secure File Serving Validation
- Integrated disk file existence checks in secure serving routes.
- Configured audit logging for missing documents to aid server diagnostics.

## Student UX, Dashboard & Search Refinements
- Implemented unified quiz attempt layout allowing real-time switching between Learning and Exam modes client-side.
- Enabled correct answer highlights and creator-written explanations on clicking "Show Answer" in Learning Mode.
- Restructured student dashboard cards: subject cards are now clickable with dynamic stats, and quizzes display Subject/Unit/Type/Difficulty details.
- Integrated instant search filters on student subjects directory and college admin subjects list.
- Configured smart context-aware navigation return buttons on quiz completion result and review views.

## GitHub & Deployment Safety Cleanup
- Created `.gitignore` to protect instance database, virtual environment, and upload assets.
- Added `.env.example` file for configuring production environmental variables.
- Verified that all credentials and session secrets utilize clean fallback options reading from environment values.

## PythonAnywhere & PWA Support
- Documented complete step-by-step setup guides for production-ready deployment on PythonAnywhere Free Tier.
- Configured maximum upload limits (5MB) and custom 413 error templates to manage disk quota consumption safely.
- Added basic PWA manifest and service worker files to enable home screen mobile installation.
- Created step-by-step mobile installation guide for students/teachers on iOS Safari and Android Chrome.

## Phase 12: Edit & Delete Permissions Audit & Stabilization
- Audited and secured edit/delete capabilities for student community library uploads, allowing uploaders to safely modify contents or soft-delete them (status set to `removed_by_uploader`).
- Resolved college admin cascade deletion issues, nullifying unit and study material references in quizzes to prevent DB constraint exceptions on delete.
- Implemented soft deletion/deactivation for subjects, preventing direct student URL access to deactivated content.
- Blocked hard deletion of quizzes with attempts, unpublishing them instead.
- Conducted full final QA pass, resolving outstanding bugs, and documenting release readiness in `FINAL_QA_REPORT.md`.

## Phase 13: UI/UX Redesign Plan
- Created a comprehensive UI/UX Redesign Plan (`UI_REDESIGN_PLAN.md`) outlining a modern digital library/SaaS visual direction, lightweight frontend library strategy (Alpine.js and HTMX), and structured implementation steps to transition StudyHub College into a professional product-level app.

## Phase 14: Modern SaaS UI/UX Visual Transformation
- [x] Implemented comprehensive visual frontend redesign across StudyHub College templates, standardizing Inter sans-serif fonts, slate backgrounds, shadows, and button transitions for a premium modern SaaS feel.

## Phase 15: College Onboarding & Selection Improvements
- [x] Added `logo_path` field to both the `College` and `CollegeRequest` model database schemas and wrote/executed migration scripts.
- [x] Implemented secure college logo uploading and serving logic (validating PNG, JPG, JPEG, and WEBP formats up to 2MB).
- [x] Added optional logo upload support to the public college registration request form, saving request logos securely on the server and transferring them to the `College` entity upon request approval.
- [x] Implemented manual college creation and edit routes for Platform Admins (GET/POST `/admin/colleges/<id>/edit`), allowing full customization of college name, code, city, state, address, contact email/phone, status, and logo.
- [x] Show logo thumbnails in the platform admin college directory, college details views, student college selection/onboarding portal, and student dashboard welcome headers. Renders initials-based fallback avatars when no logo exists.
- [x] Added real-time search box on the student college selection page, dynamically filtering matching colleges by name, code, city, or state in the browser using client-side JavaScript.
- [x] Designed clean empty-state placeholder matching the Modern Minimal SaaS theme when no search results match.

## Phase 16: Mobile UI Usability Fixes
- [x] Restored compact, horizontal mobile headers (showing brand on left, notifications bell and dropdown on right).
- [x] Hid secondary public text navigation links on mobile to prevent header wrapping.
- [x] Overhauled mobile grids (stats widgets, subject list) to stack cleanly in single column layouts.
- [x] Added a clear, touch-friendly "Browse All Subjects" button below student dashboard subject cards.
- [x] Improved mobile Community Library filters: made the Search button visible beside the input, added a gears-icon Filters toggle button, and optimized the action buttons row.
- [x] Refined quiz attempts: made the sidebar non-sticky on mobile, and reduced container and option label padding.

## Phase 17: Database Migration Improvements
- [x] Updated database migration script `migrate_db.py` to be fully robust and idempotent.
- [x] Documented the simplified post-pull migration workflow in `DEPLOYMENT_PYTHONANYWHERE_FREE.md`.

## Phase 18: Student Onboarding and Subscription Flow (Completed)
- [x] Create database models & safe idempotent SQLite migrations (added `User.onboarding_completed`, `User.profile_completed`, `SubjectSubscription.is_enabled`, and `CollegeSubscription` table).
- [x] Implement onboarding progress check (redirect new students with incomplete profiles).
- [x] Create searchable college selection card grid and subject checkbox grid.
- [x] Build follow/unfollow college updates routes and controls.
- [x] Refactor notification center queries to seamlessly deduplicate college and subject alerts.
- [x] Customize the student dashboard to display the selected college logo and hide unsubscribed subjects.
- [x] Fix notification subscription timing logic to ensure students only see notifications created after subscription activation (`created_at >= followed_at`).

## Phase 19: React Frontend Migration (Version 2 - In Progress)
- [x] Implement dynamic Flask API route `GET /api/student/dashboard` serving complete JSON data for the React student dashboard
- [ ] Migrate Student Dashboard page (First page targeted for React)
- [ ] Migrate Onboarding Flow pages
- [ ] Migrate Subjects Directory & Course pages
- [ ] Migrate Community Library pages
- [ ] Migrate Quiz Engine solver interface
