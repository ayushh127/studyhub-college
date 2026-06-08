# VERSION 1 RELEASE NOTES: StudyHub College v1 Stable

This document marks the stable, production-ready release of **StudyHub College v1** before transitioning to the v2 React page-by-page migration.

---

## Version Info
* **Version Name:** StudyHub College v1 Stable
* **Framework:** Python Flask, Flask-SQLAlchemy, Jinja2, Vanilla CSS/JS
* **Database:** SQLite (local / single node)
* **Date:** June 8, 2026

---

## Completed Features
1. **Multi-Role Access Control & Security:**
   - Platform Admin (Approvals, user/college control, audit logs, student impersonation for support).
   - College Admin (Subjects CRUD, Unit CRUD, resource uploading, manual quiz builder, multiple admins per college).
   - Student (Dashboard, content browser, notifications, quiz solver, community library uploader).
2. **Academic Hierarchy Restructuring:**
   - Restructured all courses into a logical hierarchy: `Subject -> Unit -> Resources` (Materials, PYQs, Quizzes) complete with breadcrumb navigation.
3. **Interactive Quiz Engine:**
   - Supports **Learning Mode** (instant correct answer feedback, custom explanations, score tracking) and **Exam Mode** (scoring, countdown timer, question completion tracking).
4. **Community Library:**
   - File-sharing portal for students to contribute links or PDFs.
   - Includes unique view tracking, rating metrics, like counts, reporting, and moderation moderation-score filters.
5. **Modern Minimal SaaS Visual Redesign:**
   - Clean fonts (Inter), harmonized slate colors, interactive borders, horizontal header layout, and mobile-friendly bottom navigations.
6. **Timing-Aware In-App Notifications:**
   - Subject-wise and College-wide notifications.
   - Ensures students only see notifications created *after* their follow became active (`Notification.created_at >= Subscription.followed_at`).
   - Merged database query filters via logical `OR` for deduplicated lists and accurate unread badge counts.
7. **Production-Ready served assets:**
   - Dedicated served routing (`/files/...`) with permission checking and disk checks to block IDOR and directory traversal.
8. **PWA Mobile Support:**
   - Standard Service Worker and manifest configuration allowing students to add the study platform to their mobile home screens.

---

## Known Limitations
* **SQLite Write Concurrency:** Local SQLite database uses disk write locks, which is ideal for single-node hosting but does not scale to high-volume multi-node deployments.
* **On-Disk File Storage:** Course files and college logos are stored on the server's local file system rather than cloud object storage (like AWS S3).
* **Sync Alerts:** Notifications use REST pulls/polls. There is no real-time WebSocket communication.

---

## Deployment Status & Notes
* **Target Environment:** Tested and optimized for deployment on **PythonAnywhere Free Tier**.
* **Upload Limits:** Enforced 5MB maximum file upload limits on study materials/PYQs to manage disk quota consumption, displaying custom `413 Payload Too Large` error templates.

---

## Database & Storage Notes
* **Database Path:** `instance/studyhub.db`
* **Assets Upload Directory:** `uploads/`
* **Logos Directory:** `uploads/college_logos/`

---

## Rollback Reminder
Before initiating any React migrations, create a full backup of the database and upload folders, and tag the commit. If v2 encounters breaking regressions, roll back to the tagged v1 stable commit using:
```bash
git checkout tags/v1-stable
```
See [V1_BACKUP_AND_ROLLBACK.md](file:///d:/StudyHub/V1_BACKUP_AND_ROLLBACK.md) for step-by-step restoration instructions.
