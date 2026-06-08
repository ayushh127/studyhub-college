# Student Onboarding & Subscription Flow Plan

> Student onboarding/subscription database, routes, and UI template foundations added. Notification logic and AJAX subscription toggles not implemented yet.

This document outlines the design, architecture, routes, database schema, and notification logic to provide a clean, modern, and user-friendly onboarding experience for students on **StudyHub College**.

---

## 1. Database & Model Changes

### A. User Profile Fields
To track the student's onboarding and registration state, we add the following fields to the `User` model in `app/models.py`:
* **`onboarding_completed`** (`db.Boolean`, default=`False`, nullable=False): Tracks whether a student has completed their first-time college selection, followed subjects, and notification preferences. If `False`, they will be redirected to the onboarding wizard.
* **`profile_completed`** (`db.Boolean`, default=`False`, nullable=False): Tracks whether the student's profile setup is finalized.

### B. College Subscription Model
To allow students to subscribe to all updates from their selected college, we will introduce a new model **`CollegeSubscription`** in `app/models.py` (which includes a `followed_at` timestamp to support subscription timing controls).
```python
class CollegeSubscription(db.Model):
    __tablename__ = 'college_subscriptions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    college_id = db.Column(db.Integer, db.ForeignKey('colleges.id'), nullable=False)
    is_enabled = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    followed_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (db.UniqueConstraint('user_id', 'college_id', name='_user_college_uc'),)

    user = db.relationship('User', backref=db.backref('college_subscriptions', cascade='all, delete-orphan'))
    college = db.relationship('College', backref=db.backref('college_subscriptions', cascade='all, delete-orphan'))
```

### C. Subject Subscription Model Updates
The existing `SubjectSubscription` model in `app/models.py` has been updated with a `followed_at` column as well.
```python
class SubjectSubscription(db.Model):
    __tablename__ = 'subject_subscriptions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    is_enabled = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    followed_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
```

---

## 2. Route Plan
The onboarding and subscription flows will be managed by the following endpoints in `app/routes/student.py`:

* **`GET /student/onboarding`**
  * Renders the unified multi-step onboarding page.
  * Displays a progress bar and three distinct steps:
    1. **College Selection:** Searchable grid of active college cards.
    2. **Subject Selection:** Checkbox list of subjects belonging to the chosen college.
    3. **Preferences:** Checkbox option to follow all updates from the selected college.
* **`POST /student/onboarding`**
  * Processes the submitted onboarding form.
  * Steps:
    1. Sets `current_user.college_id` to the selected college.
    2. Registers `SubjectSubscription` records for all checked subjects.
    3. Creates a `CollegeSubscription` record if the college notifications checkbox is checked.
    4. Sets `current_user.onboarding_completed = True`.
    5. Redirects to `/student/dashboard`.
* **`POST /student/colleges/<int:id>/follow`**
  * Toggles (subscribes/unsubscribes) the `CollegeSubscription` for the student's linked college.
  * Supports AJAX JSON response for real-time UI updates.
* **`POST /student/subjects/<int:id>/follow`**
  * Toggles (subscribes/unsubscribes) the `SubjectSubscription` for a specific subject.
  * Supports AJAX JSON response for real-time UI updates.
* **`POST /student/onboarding/skip`**
  * Allows students to bypass the wizard. Sets default preferences (college assigned to their profile, no subject subscriptions, no college updates) and marks `onboarding_completed = True`.

---

## 3. Onboarding Flow Design
```mermaid
sequenceDiagram
    autonumber
    actor Student
    participant Middleware as student_bp.before_request
    participant OnboardingPage as /student/onboarding
    participant DB as SQLite DB
    participant Dashboard as /student/dashboard

    Student->>Middleware: Requests dashboard
    Middleware->>DB: Checks if user.onboarding_completed is True
    DB-->>Middleware: Returns False
    Middleware-->>Student: Redirect to /student/onboarding

    Note over Student, OnboardingPage: Step 1: Select College Tiles (Search/Filter)
    Note over Student, OnboardingPage: Step 2: Select Subjects to Follow
    Note over Student, OnboardingPage: Step 3: Toggle College-Wide Notifications

    Student->>OnboardingPage: Submits onboarding form (POST)
    OnboardingPage->>DB: Saves college_id, subscriptions, and sets onboarding_completed=True
    DB-->>OnboardingPage: Commits transaction
    OnboardingPage-->>Student: Redirect to /student/dashboard
```

---

## 4. UI/UX Interface Guidelines

We will adhere strictly to the "Modern Minimal SaaS" theme.

### A. Onboarding Steps
* **Progress Bar:** A clean top tracker indicating `Step 1: College Selection`, `Step 2: Choose Subjects`, and `Step 3: Preferences`.
* **College Selection:** A grid of cards with college logos (and initials fallback). Real-time searching uses client-side JavaScript to filter tiles instantly by name, code, city, or state. Selecting a card highlights it with an Indigo border and checks a hidden input.
* **Subject Selection:** Renders subject cards grouped by semester. Each card features a checkbox and summary details (Subject Code, Semester).
* **College Updates:** A toggle switch styled with CSS to follow/unfollow the college.

### B. Dashboard Changes
* **College Card:** Displayed at the top of the student dashboard, featuring the selected college's logo, details, and a quick "Follow College Updates" toggle button.
* **Followed Subjects:** The dashboard will display **only** followed subjects to keep it focused.
* **Empty State:** If a student does not follow any subjects, a clean placeholder card will be displayed, guiding them with a "Find & Follow Subjects" button that links to the Subjects Directory.
* **Onboarding Banner:** A small dismissible notification alert reminding them they can reconfigure their preferences in `/student/profile` at any time.

---

## 5. Notification Logic
To prevent duplicate notifications when a student is subscribed to both the college and individual subjects within it, we will query notifications using a unified SQL query.

### A. Notification Dispatching
* When a college admin publishes content (material, PYQ, or quiz), a single `Notification` row is inserted:
  ```python
  notification = Notification(
      college_id=college_id,
      subject_id=subject_id,
      ...
  )
  ```

### B. Fetching Notifications (Timing-Aware and Deduplicated)
* We retrieve notifications for a student matching their college id where:
  - If a student is subscribed to the college, notifications are shown if `Notification.created_at >= CollegeSubscription.followed_at`.
  - If they are subscribed to subjects, notifications are shown for those subjects if `Notification.created_at >= SubjectSubscription.followed_at`.
  - If they are subscribed to both, the timing window filters are combined using a logical `OR` so that notifications are returned without duplication if they qualify through *either* path.
* **SQL Query Structure:**
  ```python
  college_sub = CollegeSubscription.query.filter_by(
      user_id=current_user.id,
      college_id=current_user.college_id,
      is_enabled=True
  ).first()
  
  subject_subs = SubjectSubscription.query.filter_by(
      user_id=current_user.id,
      is_enabled=True
  ).all()
  
  from sqlalchemy import or_, and_
  filters = []
  if college_sub:
      filters.append(Notification.created_at >= college_sub.followed_at)
  for sub in subject_subs:
      filters.append(and_(
          Notification.subject_id == sub.subject_id,
          Notification.created_at >= sub.followed_at
      ))
      
  if not filters:
      notifications_list = []
  else:
      notifications_list = Notification.query.filter(
          Notification.college_id == current_user.college_id,
          or_(*filters)
      ).order_by(Notification.created_at.desc()).all()
  ```
* Since the filter resolves to a single query on the `Notification` table, it naturally deduplicates alerts!

---

## 6. Implementation Stages & Tokens

To manage scope safely and keep the project compile-ready at all times, we will implement this feature in the following order:

* **Step 1: Database Models & Migrations**
  * Update `User` and create `CollegeSubscription` in `app/models.py`.
  * Write and run the SQLite schema migration script `migrate_student_onboarding.py`.
* **Step 2: Onboarding Controller & Redirects (Completed)**
  * [x] Add the global onboarding check in `student_bp.before_request`.
  * [x] Implement the `/student/onboarding` GET and POST routes in `app/routes/student.py`.
* **Step 3: Onboarding UI Templates (Completed)**
  * [x] Create `app/templates/student/onboarding.html` using a multi-step layout.
* **Step 4: AJAX Subscription Toggles (Completed)**
  * [x] Implement `/student/colleges/<id>/toggle-follow` and `/student/subjects/<id>/toggle-subscription` routes.
  * [x] Add frontend JS click triggers and JSON support.
* **Step 5: Notifications Logic Refactoring (Completed)**
  * [x] Update `User.get_unread_notification_count()` in `app/models.py`.
  * [x] Update `notifications()` and `read_all_notifications()` endpoints in `app/routes/student.py`.
* **Step 6: Dashboard Customizations & QA (Completed)**
  * [x] Clean up `dashboard.html` to show followed subjects, selected college subscription card, setup banners, and quick access actions.
  * [x] Verify the full onboarding experience and toggles using automated and manual QA tests.
