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
- **Current Phase:** Completed MVP release (v1) and Subject-Wise Notifications (Phase 7).
- **Next Step:** Ready for production deployment and pilot phase.

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
