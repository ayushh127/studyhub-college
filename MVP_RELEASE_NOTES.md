# StudyHub College MVP - Release Notes (v1)

Welcome to the official release documentation for **StudyHub College MVP v1**. This document outlines the system architecture, completed features, role permissions, main user flows, deployment readiness guidelines, and checklists for pushing to GitHub and production hosting (e.g., PythonAnywhere).

---

## Release Information
* **Version Name:** StudyHub College MVP v1
* **Release Date:** June 2026
* **Primary Theme:** Classical Minimal Academic
* **Target Audience:** College administrators, educators, and students

---

## Completed Features
1. **Academic Hierarchy Content System**: Support for creating Subjects, linking Units/Chapters as children, and organizing uploads under them.
2. **Document & PYQ Manager**: Secure PDF uploading and metadata setup (Semester, Code, Year, Exam Type).
3. **Interactive Quiz Attempt Engine**:
   - **Learning Mode**: Instant client-side check-answers, green/red highlight indicators, and creator-written question explanations.
   - **Exam Mode**: Formal timer-based test layout with scoring logic on submission.
   - **Mode Toggler**: Real-time client-side switching during attempts.
4. **Student Dashboard & Subject Discovery**: Clickable subject metrics cards, context-rich available quizzes, and real-time subject list search filter.
5. **Secure File Routing**: Serving uploaded materials and PYQs via Flask routing (`/files/...`) with user college-bound permission validation instead of open public folders.
6. **Platform Admin Tools**: Approve/reject public requests, manually create colleges (auto-provisioning first college admin), list/activate/deactivate instances.
7. **Support Impersonation**: Platform admins can temporarily view the system through a Student or College Admin session.
8. **Secure Admin Provisioning**: Added `create_admin.py` CLI script and `/admin/users/create-platform-admin` dashboard form to securely register administrators using Werkzeug password hashing.
9. **In-App Notifications (Phase 7)**: Subject-wise subscription model notifying students when new materials, PYQs, or quizzes are published, complete with unread badge counters and read status tracking.
10. **Progressive Web App (PWA) Support**: Basic mobile installation support allowing users to save the portal directly to their home screens, running in standalone full-screen windows matching the academic theme.

---

## Roles & Permissions

| Role | Permissions & Access | Default Home Route |
| :--- | :--- | :--- |
| **Platform Admin** | Full access to approve requests, manually provision colleges, manage activation states, add platform admins, audit logs, and support impersonation. | `/admin/dashboard` |
| **College Admin** | Complete CRUD over college-bound subjects, units, quizzes, study materials, and PYQs. Can manage additional college admin accounts. | `/college-admin/dashboard` |
| **Student** | Choose college, search active subjects, browse unit materials/PYQs, attempt quizzes, and track personal scores/averages. | `/student/dashboard` |

---

## Main User Flows
1. **Public College Registration & Platform Approvals**:
   - Public College registers at `/college/register` (specifying college info + initial admin email & secure password).
   - Platform Admin reviews at `/admin/college-requests` and clicks **Approve**.
   - College is created and bounds the newly provisioned College Admin account.
2. **Academic Setup**:
   - College Admin logs in &rarr; creates **Subject** (semester specific) &rarr; adds **Units**.
   - Uploads PDFs to specific units, or creates a **Quiz** with MCQ questions.
   - Sets visibility to **Published** so students can view.
3. **Student Learning & Practice**:
   - Student signs up &rarr; selects **College** (only active ones listed).
   - Searches for **Subject** &rarr; views unit study materials, past papers, or takes quizzes.
   - Conducts practice attempts, submits, reviews explanations, and tracks performance averages.

---

## Known Limitations
* **Single File Format**: Current document uploads are restricted to `.pdf` formats.
* **Local File Storage**: Materials and PYQs are saved locally on disk (suitable for MVP/single-server setups, needs S3/blob integration for distributed hosting).
* **Reset Password Flow**: Currently utilizes placeholder views; full email-bound token resets are deferred.

---

## Future Features (Post-MVP AI Integration)
* **AI Quiz Generation**: Automatic quiz creation from uploaded unit PDF study materials or notes.
* **AI Chat Assistant**: In-context sidebar assistant to answer student questions about unit chapters.
* **AI Summary Generator**: Quick key-takeaways generator for textbooks and lecture notes.

---

## Deployment Readiness Checklist

### 1. Security & Configuration
- [ ] Ensure `SECRET_KEY` in `app/config.py` is loaded from environment variables in production.
- [ ] Turn off Flask debug mode (`debug=False`).
- [ ] Ensure database files (`instance/studyhub.db`) are properly backed up.
- [ ] Verify that no demo credentials are exposed on `/login` UI (Complete).
- [ ] Remove default credentials from database seeds or change passwords for production deployment.

### 2. GitHub Push Checklist
- [ ] Verify `.gitignore` excludes local virtual environments (`venv/`), SQLite files (`*.db`, `*.db-journal`), uploads directories (`uploads/`), and development caches (`__pycache__/`).
- [ ] Do **NOT** push production database files (`studyhub.db`).
- [ ] Commit only sanitized configuration templates.
- [ ] Execute `python create_admin.py` locally or run commands on target environments for the initial setup.

### 3. PythonAnywhere Deployment
For detailed step-by-step instructions on deploying the application to the PythonAnywhere Free Tier, setting up environment variables, WSGI files, static mapping, and managing live updates, see the dedicated [DEPLOYMENT_PYTHONANYWHERE_FREE.md](file:///d:/StudyHub/DEPLOYMENT_PYTHONANYWHERE_FREE.md) guide.

### 4. PWA Installation
For details on installing the web app as a Progressive Web App (PWA) on iOS and Android devices, see the [PWA_MOBILE_INSTALL_GUIDE.md](file:///d:/StudyHub/PWA_MOBILE_INSTALL_GUIDE.md).
