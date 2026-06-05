# StudyHub College - Notification Feature QA Report

This document reports the QA validation status and testing results for the **Subject-Wise In-App Notifications** feature implemented in Phase 7.

---

## 1. What Works
All 17 core notification flows have been programmatically and manually tested and verified. The results are detailed below:

* **Subject Subscriptions (Flow 1 & 2)**: Students can successfully subscribe to and unsubscribe from subjects via the student subject details page. Button states update cleanly (`🔔 Subscribe` / `🔕 Unsubscribe`).
* **Subscription & College Isolation (Flow 3, 4, 5)**:
  * Students only see notifications for subjects they are actively subscribed to.
  * Students do not see notifications for unsubscribed subjects.
  * Cross-college isolation is strictly enforced. Students cannot access or receive notifications from subjects belonging to other colleges, even if they share the same name/code.
* **Notification Generation (Flow 6, 7, 8, 9)**:
  * Publishing **Study Materials** automatically dispatches a notification.
  * Publishing **PYQs** automatically dispatches a notification.
  * Publishing **Quizzes** automatically dispatches a notification.
  * **Draft / Unpublished** content remains silent and does *not* create any notifications.
* **Avoidance of Duplicates (Flow 10)**: Re-publishing already published items is safe. The backend check only fires dispatches when the content is transitioned from draft to published, avoiding duplicate notification spam.
* **Notification Bell & Unread Count (Flow 11 & 12)**: The bell icon badge count dynamically reflects the number of unread notifications matching the student's subscribed subjects.
* **Mark as Read Actions (Flow 13 & 14)**:
  * Students can mark individual notifications as read, creating a single `NotificationRead` row.
  * Students can click "Mark All as Read" to mark all active unread notifications in their subscribed subjects as read.
* **Target Redirect Links (Flow 15)**: View links lead to correct routes:
  * Material links open PDF directly via `/files/materials/<id>`.
  * PYQ links open PDF directly via `/files/pyqs/<id>`.
  * Quiz links open the quiz start view via `/student/quizzes/<id>/start`.
* **Access Control (Flow 16)**: Unauthorized/anonymous users are blocked from access and redirected to `/login` via blueprint checks.
* **Impersonation Auditing (Flow 17)**: Platform admins impersonating students load their exact notification counts. Actions taken on their behalf are tracked under standard session constraints, backed by the audit log system.

---

## 2. Bugs Found & Fixed
* **SQLAlchemy Subquery Coercion Warnings**:
  * *Bug*: In SQLAlchemy 1.4+, querying notifications using a subquery for matching subscribed subject IDs emitted a coercion warning: `SAWarning: Coercing Subquery object into a select() for use in IN()`.
  * *Fix*: Replaced the nested subquery queries in `app/routes/student.py` with standard list comprehensions over `current_user.subscriptions`, which is faster, cleaner, and avoids warnings.

---

## 3. Security Analysis
* **Indirect Object Reference (IDOR) Protection**: Notification read actions require checking ownership: `if notification.college_id != current_user.college_id: abort(403)`. This prevents students from marking other colleges' notifications as read.
* **Route Protection**: The entire student namespace uses blueprint before-request decorators enforcing `student` or `platform_admin` roles. Anonymous users are fully blocked.

---

## 4. UX Assessment
* **Clean Badge Styling**: The bell count badge is styled inside `base.html` and uses the "Classical Minimal Academic" layout theme. It remains responsive and behaves cleanly on mobile devices within the student bottom navigation bar.
* **Contextual Redirections**: "View Details" buttons inside notification cards correctly guide students directly to their content (PDF downloads/views for study resources, and start pages for quizzes), providing a seamless experience.

---

## 5. Duplicate Notification Behavior
* Notifications are only generated when an item is saved with `is_published=True` when it was previously `False`.
* Attempting to republish an already published item returns an information flash message (`"Material is already published."`) and bypasses notification creation.

---

## 6. Remaining Limitations
* Notifications are **in-app only** (stored in the database and queried in the UI). There are no email notifications or browser push notifications implemented, as requested.

---

## 7. Final Notification Readiness Status
* **Status**: **READY FOR PRODUCTION**
* All 17 verification flows successfully pass regression, security, and usability checks. The implementation is highly stable and conforms to the project rules.
