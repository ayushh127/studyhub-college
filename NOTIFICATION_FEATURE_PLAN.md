# In-App Notification Feature Plan

This document outlines the proposed implementation plan for the **Subject-Wise In-App Notification** feature. 

---

## 1. Database Schema Design

To minimize database bloat, notifications are stored globally per event, and read status is tracked on a per-user basis.

### `SubjectSubscription` (Model)
Tracks which students are subscribed to which subjects.
* `id` (Integer, Primary Key)
* `user_id` (Integer, ForeignKey('user.id'), nullable=False)
* `subject_id` (Integer, ForeignKey('subject.id'), nullable=False)
* `created_at` (DateTime, default=datetime.utcnow)
* *Constraint*: UniqueConstraint('user_id', 'subject_id')

### `Notification` (Model)
Stores the notification event itself.
* `id` (Integer, Primary Key)
* `college_id` (Integer, ForeignKey('college.id'), nullable=False)
* `subject_id` (Integer, ForeignKey('subject.id'), nullable=False)
* `title` (String(150), nullable=False)
* `message` (Text, nullable=False)
* `link` (String(255), nullable=True) -- e.g. `/student/materials/12`
* `created_at` (DateTime, default=datetime.utcnow)

### `NotificationRead` (Model)
Tracks which notifications have been read by which students.
* `id` (Integer, Primary Key)
* `user_id` (Integer, ForeignKey('user.id'), nullable=False)
* `notification_id` (Integer, ForeignKey('notification.id'), nullable=False)
* `read_at` (DateTime, default=datetime.utcnow)
* *Constraint*: UniqueConstraint('user_id', 'notification_id')

---

## 2. Routes Required

### Student Routes (`app/routes/student.py`)
* `GET /student/notifications`: Renders the notification list page.
* `POST /student/notifications/<int:id>/read`: Marks a single notification as read.
* `POST /student/notifications/read-all`: Marks all notifications in the user's subscribed subjects list as read.
* `POST /student/subjects/<int:id>/toggle-subscription`: Endpoint to subscribe/unsubscribe to a subject.

---

## 3. UI Requirements (Classical Minimal Academic Theme)

### Navigation / Global Header (`base.html`)
* **Bell Icon**: Shown in the student navbar with a dynamic unread count pill (e.g. `(3)` or a red dot badge).
* **Responsive Styling**: Matches the clean theme colors, resizing cleanly on mobile viewports.

### Notifications Page (`app/templates/student/notifications.html`)
* A dedicated dashboard sub-page with a chronological list of notifications.
* **Mark as Read** button on individual cards.
* **Mark all as Read** action button at the top.
* Parchment/minimalist style layout with empty states when there are no notifications.

### Subject Page Toggle (`app/templates/student/subject_details.html`)
* A toggle action button in the subject header (e.g., "🔔 Subscribe" or "🔕 Unsubscribe") showing the student's current subscription state for the active subject.

---

## 4. Trigger Points

Notifications are programmatically generated and committed to the database when a resource changes from unpublished to **published** (or is created as published) in the following College Admin routes:
* **Study Material**: `app/routes/college_admin.py` -> during publish/upload materials actions.
* **PYQ Paper**: `app/routes/college_admin.py` -> during publish/upload PYQ actions.
* **Quiz**: `app/routes/college_admin.py` -> during publish/upload Quiz actions.

*Example code block to trigger a notification:*
```python
def trigger_notification(college_id, subject_id, title, message, link):
    notification = Notification(
        college_id=college_id,
        subject_id=subject_id,
        title=title,
        message=message,
        link=link
    )
    db.session.add(notification)
```

---

## 5. Security & Isolation Rules

* **College Level Isolation**: Students can only retrieve notifications where `Notification.college_id == current_user.college_id`.
* **Subscription Isolation**: Query notifications by joining on `SubjectSubscription` where `SubjectSubscription.user_id == current_user.id` and `SubjectSubscription.subject_id == Notification.subject_id`.
* **Read-Status Integrity**: Reading a notification creates a record in `NotificationRead` bound only to `current_user.id`.
* **Impersonation Safety**: Platform admins impersonating a student should not persist read records or subscriptions unless desired, but standard role checks will handle session authentication cleanly.

---

## 6. Implementation Steps

### Step 1: Database Models
1. Add `SubjectSubscription`, `Notification`, and `NotificationRead` to `app/models.py`.
2. Run database migration script `migrate_db.py` to add new tables.

### Step 2: Backend Routes (Student)
1. Add the notification endpoints to `app/routes/student.py`.
2. Implement querying logic that fetches notifications for subscribed subjects and determines read status via exclusion joins on `NotificationRead`.

### Step 3: Frontend Templates & Styles
1. Update `app/templates/student/subject_details.html` with subscription toggle.
2. Add the Bell Icon/unread count badge to the student navbar (`base.html`).
3. Create `app/templates/student/notifications.html` with read actions.

### Step 4: Admin Triggers
1. Add helper function to create notifications.
2. Hook helper function into College Admin publish routes for Quizzes, Materials, and PYQs.

### Step 5: Verification & QA
1. Validate notification dispatch on new uploads.
2. Verify students receive only their college's/subscriptions' notifications.

---

## 7. Testing Checklist

### Setup Stage
* [ ] Create two test Student accounts: Student A and Student B (both under College X).
* [ ] Create a third Student account: Student C (under College Y).
* [ ] Create a College Admin account for College X.

### Test Case 1: Subscription Toggles
1. Log in as Student A.
2. Go to Subject CS101. Click **🔔 Subscribe**. Verify button text changes to **🔕 Unsubscribe**.
3. Verify database has a subscription record for Student A and CS101.

### Test Case 2: Notification Generation & Cross-College Isolation
1. Log in as College X Admin.
2. Upload a new study material to CS101 and click **Publish**.
3. Log in as Student A. Verify the unread notification badge is visible and lists the new CS101 material.
4. Log in as Student B (not subscribed to CS101). Verify they see **0** notifications.
5. Log in as Student C (College Y). Verify they see **0** notifications (even if subscribed to a subject with the same name).

### Test Case 3: Read State
1. Log in as Student A. Go to notifications page.
2. Click **Mark as Read** on the CS101 notification.
3. Verify it is marked visually as read and the badge count decreases.
4. Verify Student B's notification state remains completely unaffected.
