# StudyHub College MVP

StudyHub College is a multi-college study platform designed to help colleges manage their academic materials (PDFs, notes, assignments), previous year question papers (PYQs), and quizzes. It provides a seamless experience for students to select their college, access subject-specific content, and prepare for exams through comprehensive learning and exam modes.

The MVP release is fully completed, featuring a responsive, clean interface tailored to the "Classical Minimal Academic" theme, secure backend-level role permissions, college administration CRUD controls, a client-side mode-switching quiz engine, and tools for secure, production-safe platform admin provisioning.

## Tech Stack
- **Backend:** Python Flask
- **Database:** SQLite (development), Flask-SQLAlchemy
- **Authentication:** Flask-Login, Werkzeug Security
- **Frontend:** HTML5, CSS3 (Vanilla), JavaScript, Jinja2 Templates
- **Design:** Mobile-first, Responsive
- **Theme:** Classical Minimal Academic

## Key Features
- **Multi-Role Access:** Platform Admin, College Admin, Student
- **College Management:** Registration, approval workflow, manual provisioning, and activation/deactivation controls.
- **Multiple College Admins:** Support for multiple administrators per college with secure password configuration during registration and dashboard management.
- **Material Hosting:** Upload and view PDFs, Notes, and PYQ papers mapped to specific subjects or unit chapters.
- **Quizzes:** Interactive quiz engine supporting Learning Mode (with immediate correct option highlights and detailed explanations) and Exam Mode (with scoring, timers, and progress tracking).
- **Secure File Serving:** Dedicated permission-controlled routes (`/files/...`) with disk file checks and audit logs to prevent directory exposure and IDOR attacks.
- **Impersonation:** Platform Admin can temporarily view the app as a student or college admin for testing and support.
- **Audit Logging:** System logging for registrations, logins, impersonation actions, and missing files.
- **In-App Notifications (Phase 7):** Subject-wise subscription model notifying students when new materials, PYQs, or quizzes are published, complete with unread badge counters.
- **Progressive Web App (PWA):** Basic mobile installation support allowing users to save the portal directly to their home screens, running in standalone full-screen windows matching the academic theme.

## Getting Started
* For local setup and development credentials: See [SETUP.md](file:///d:/StudyHub/SETUP.md).
* For free hosting setup: See [DEPLOYMENT_PYTHONANYWHERE_FREE.md](file:///d:/StudyHub/DEPLOYMENT_PYTHONANYWHERE_FREE.md).
* For mobile home screen installation instructions: See [PWA_MOBILE_INSTALL_GUIDE.md](file:///d:/StudyHub/PWA_MOBILE_INSTALL_GUIDE.md).
