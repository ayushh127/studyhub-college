# Community Library Feature Plan

This document outlines the design and implementation plan for the **Community Library** feature in StudyHub College.

The Community Library is a student-to-student sharing hub. Unlike the official college content system managed by College Admins, the Community Library is open to all students across all colleges. Students can upload resources (PDFs and/or external URLs), search the library, rate, like, and report materials. Moderation is handled by Platform Admins using a risk-scoring system to prevent report abuse.

---

## 1. Database Schema Design

The new models will be added to `app/models.py`. We will preserve the SQLAlchemy database and SQLite setup.

### `CommunityMaterial`
Stores the material shared by a student.
* `id` (Integer, Primary Key)
* `title` (String(150), nullable=False)
* `description` (Text, nullable=True)
* `subject_name` (String(100), nullable=False) -- Free-text subject label
* `college_tag_id` (Integer, ForeignKey('colleges.id'), nullable=True) -- Optional college association
* `uploaded_by` (Integer, ForeignKey('users.id'), nullable=False)
* `material_type` (String(50), default='notes') -- e.g., 'notes', 'assignment', 'pyq', 'other'
* `file_path` (String(255), nullable=True) -- Local path to uploaded PDF (nullable if using external_url)
* `external_url` (String(255), nullable=True) -- Link to drive/website (nullable if uploading PDF)
* `status` (String(20), default='active') -- 'active', 'under_review', 'hidden', 'removed'
* `views_count` (Integer, default=0)
* `likes_count` (Integer, default=0)
* `reports_count` (Integer, default=0)
* `ratings_count` (Integer, default=0)
* `average_rating` (Float, default=0.0)
* `moderation_score` (Float, default=0.0) -- Calculated risk score
* `created_at` (DateTime, default=datetime.utcnow)
* `updated_at` (DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

### `CommunityMaterialLike`
Tracks likes to prevent duplicates.
* `id` (Integer, Primary Key)
* `user_id` (Integer, ForeignKey('users.id'), nullable=False)
* `material_id` (Integer, ForeignKey('community_materials.id'), nullable=False)
* `created_at` (DateTime, default=datetime.utcnow)
* *Constraint*: UniqueConstraint('user_id', 'material_id')

### `CommunityMaterialRating`
Tracks student ratings (1 to 5 stars) to calculate averages and prevent duplicates.
* `id` (Integer, Primary Key)
* `user_id` (Integer, ForeignKey('users.id'), nullable=False)
* `material_id` (Integer, ForeignKey('community_materials.id'), nullable=False)
* `rating` (Integer, nullable=False) -- Constrained to range [1, 5]
* `created_at` (DateTime, default=datetime.utcnow)
* *Constraint*: UniqueConstraint('user_id', 'material_id')

### `CommunityMaterialReport`
Tracks reports to prevent report-spam abuse.
* `id` (Integer, Primary Key)
* `user_id` (Integer, ForeignKey('users.id'), nullable=False)
* `material_id` (Integer, ForeignKey('community_materials.id'), nullable=False)
* `reason` (Text, nullable=False)
* `created_at` (DateTime, default=datetime.utcnow)
* *Constraint*: UniqueConstraint('user_id', 'material_id')

### `CommunityMaterialView`
Tracks unique student views per community material.
* `id` (Integer, Primary Key)
* `user_id` (Integer, ForeignKey('users.id'), nullable=False)
* `material_id` (Integer, ForeignKey('community_materials.id'), nullable=False)
* `viewed_at` (DateTime, default=datetime.utcnow)
* *Constraint*: UniqueConstraint('user_id', 'material_id')

---

## 2. Route Architecture

### Student Routes (`app/routes/student.py` / new blueprint)
* `GET /student/community`: Renders the Community Library landing page (lists, filters, sorts materials).
* `GET /student/community/upload`: Renders the material upload form.
* `POST /student/community/upload`: Receives and validates material uploads (PDF and/or URL).
* `GET /student/community/materials/<int:id>`: Renders the details page for a specific material.
* `GET /student/community/materials/<int:id>/download`: Serves the PDF securely (validates role and file state).
* `POST /student/community/materials/<int:id>/like`: Toggles a like (creates/deletes `CommunityMaterialLike`).
* `POST /student/community/materials/<int:id>/rate`: Submits a rating (creates/updates `CommunityMaterialRating`).
* `POST /student/community/materials/<int:id>/report`: Submits a report (creates `CommunityMaterialReport`).
* `GET /student/community/my-uploads`: Renders a list of the logged-in student's uploaded materials.
* `GET /student/community/materials/<int:id>/edit`: Renders the material edit form for the uploader's own active material.
* `POST /student/community/materials/<int:id>/edit`: Processes the material updates (validates, updates DB, saves new PDF).
* `POST /student/community/materials/<int:id>/delete`: Allows the uploader to soft-delete their own active material (changes status to `removed_by_uploader`).

### Platform Admin Routes (`app/routes/admin.py`)
* `GET /admin/community`: Lists all community materials.
* `GET /admin/community/queue`: Moderation queue (lists materials with `status='under_review'`).
* `GET /admin/community/reports/<int:id>`: Lists individual report reasons for a specific material.
* `POST /admin/community/materials/<int:id>/hide`: Sets `status='hidden'` (moderator override).
* `POST /admin/community/materials/<int:id>/restore`: Restores `status='active'` and resets moderation score.
* `POST /admin/community/materials/<int:id>/remove`: Hard deletes or marks `status='removed'`.

### College Admin Role
College Admins have no moderation powers in the first version to keep the hierarchy simple. They can view community materials normally, and a future phase can enable filters allowing them to view materials tagged to their specific college.

---

## 3. Moderation & Risk Escalation Formula

To protect against report abuse (e.g. students trying to tear down a competitor's notes or fake report spam), we use a weighted moderation risk formula:

### Metrics
1. $\text{report\_rate} = \frac{\text{reports\_count}}{\max(\text{views\_count}, 1)}$
2. $\text{like\_rate} = \frac{\text{likes\_count}}{\max(\text{views\_count}, 1)}$
3. $\text{rating\_score} = \frac{\text{average\_rating}}{5}$

### Risk Score Calculation
$$\text{risk\_score} = (\text{report\_rate} \times 100) + (\text{reports\_count} \times 3) - (\text{like\_rate} \times 40) - (\text{rating\_score} \times 20)$$

### Escalation Thresholds
A material's status is programmatically moved to `'under_review'` if it triggers any of the following rules:
1. **High Volume Reports**: $\text{reports\_count} \ge 5$ (Regardless of risk score).
2. **Suspicious Activity**: $\text{reports\_count} \ge 3$ and $\text{risk\_score} \ge 25$.
3. **High Ratio Reports**: $\text{report\_rate} \ge 0.25$ and $\text{views\_count} \ge 10$.
4. **Poor Quality + Flagged**: $\text{average\_rating} \le 2.0$ and $\text{ratings\_count} \ge 5$ and $\text{reports\_count} \ge 2$.

Materials flag for review but **are not auto-deleted**. They are queued in the Platform Admin Moderation Queue for final human review.

---

## 4. UI/UX Elements (Modern Minimal SaaS Theme)
* **Library Explorer**: A clean grid of material cards showing the title, free-text subject label, tags (if college associated), uploader, type icon (PDF or Link), likes, views, and star ratings.
* **Upload Interface**: Dual input form. Includes file select field (PDF only, max 5MB) and text input for external URL, validating that at least one is provided.
* **Moderation Board**: Platform admin queue showing flagged items sorted by $\text{risk\_score}$ descending, complete with quick action buttons (`Hide`, `Restore`, `View Reports`).

---

## 5. Security Constraints
* **Authentication**: All endpoints require logged-in sessions.
* **Authorization**: Only the uploader can edit/delete their own active material. Only Platform Admins can access moderation routes.
* **File Validation**: PDF extension check and strict 5MB file size limit. Files saved outside the public static directory and streamed via secure file transfer endpoints.
* **Unique Actions Constraints**: Unique constraints on database tables prevent students from writing duplicate likes, multiple ratings, or reporting the same item multiple times.

---

## 6. Implementation Sequence

* **Step 1: Database Setup** (COMPLETED)
  * Define `CommunityMaterial`, `CommunityMaterialLike`, `CommunityMaterialRating`, and `CommunityMaterialReport` in `app/models.py`.
  * Create a migration script to add the tables to SQLite without affecting existing data.
  * *Note: Community Library database models added. Routes/UI/interactions/moderation not implemented yet.*
* **Step 2: Student Interface - Browsing & Searching** (COMPLETED)
  * Create templates `student/community_list.html` and the student route `/student/community`.
  * Add filters (search input, type selector, college tag dropdown) and sorting logic (latest, views, likes).
* **Step 3: Student Interface - Uploads & File Handling** (COMPLETED)
  * Create `student/community_upload.html` template and forms validation.
  * Integrate secure file storage for uploads under `uploads/community/`.
  * *Note: Upload routes and templates created. Likes, ratings, details, and moderation are not implemented yet.*
* **Step 4: Student Interface - Material Detail & Interactions** (COMPLETED)
  * Create `student/community_details.html` template.
  * Implement backend routes for detail views, secure file streaming, external link redirection, and view tracking.
* **Step 5: Interactions (Likes & Ratings)** (COMPLETED)
  * Implemented `POST /student/community/materials/<id>/like` to toggle like status.
  * Implemented `POST /student/community/materials/<id>/rate` to add/update user ratings.
  * Updated detail templates to display interactable UI components.
* **Step 6: Reporting and Moderation Queue** (COMPLETED)
  * Implemented `POST /student/community/materials/<id>/report` route.
  * Added `update_community_material_moderation` to `app/utils/community.py` to calculate `risk_score`.
  * Configured escalation thresholds to automatically set highly flagged content to `under_review`.
* **Step 7: Admin Moderation Console** (COMPLETED)
  * Implemented platform admin routes for community moderation (`GET /admin/community`, `GET /admin/community/queue`, etc.).
  * Added ability for admins to view reports and hide/restore/remove materials.
  * Added `community_list`, `community_queue`, and `community_reports` admin templates.
* **Step 8: UX and Counting Refinements** (COMPLETED)
  * Implemented `CommunityMaterialView` for unique view counting (1 view per logged-in user per material).
  * Added AJAX JSON response support to `/student/community/materials/<id>/like`.
  * Redesigned Like button in lists and detail page to use heart icon states (♥/♡) and toggle via asynchronous `fetch` without page reload.
  * Added uploader preview notice and restricted student access for non-active materials (hidden/under review/removed).
  * Made titles clickable links on student My Uploads and Explorer list cards.
* **Step 9: Public Uploader Profile** (COMPLETED)
  * Implemented `GET /student/community/users/<user_id>` route to show a student's public community profile.
  * Created `community_user_profile.html` template showing user stats (total active uploads, views, likes, average rating) and a list of active materials uploaded by the student.
  * Added links to the uploader profile on the material details page, community list cards, and the My Uploads page.
  * Ensured privacy by hiding inactive/hidden materials and non-public user data.
