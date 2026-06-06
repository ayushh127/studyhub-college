# Community Library QA Verification Report

This document reports the final QA verification results for the **Community Library** feature implementation in StudyHub College. All 33 target verification flows have been tested and verified successfully.

---

## 1. Overall Status
* **QA Status**: 🟢 **PASSED** (100% of test cases passed)
* **Local Testing Readiness**: **Ready**
* **Production Deployment Readiness**: **Safe to deploy**

---

## 2. Tested & Verified Flows

### Student Library Explorer & Navigation
1. **Student Library Explorer (Flows 1 & 5)**: Renders explorer interface cleanly. Sort parameters (`sort=latest`, `sort=views`, `sort=likes`, `sort=rating`) function successfully.
2. **Text Filtering (Flow 2)**: Standard subject, title, and description search matches materials dynamically.
3. **Type Filtering (Flow 3)**: Filters materials by type (`Notes`, `Assignment`, `PYQ`, `Other`).
4. **College Tag Filtering (Flow 4)**: Filters by optional college association tags.

### Sharing & Upload Validation
5. **PDF Uploads (Flow 6)**: Uploading PDF files works seamlessly.
6. **External URLs (Flow 7)**: Uploading materials with external URLs works.
7. **Empty Resource Blocking (Flow 8)**: Submitting the share form without both PDF and link displays a validation warning and blocks saving.
8. **Invalid Extensions Blocking (Flow 9)**: Blocked uploading files other than `.pdf`.
9. **File Size Limit (Flow 10)**: Custom `413 Payload Too Large` page prevents files larger than 5MB from consuming database/disk space.

### Details & View Counting
10. **My Uploads (Flow 11)**: Student can view their own uploaded materials with statuses, views, likes, and ratings counts. Title text is a clickable link.
11. **Details Access (Flows 12 & 13)**: Clickable title links open the material detail view cleanly. Uploader can view own active and non-active uploads. Other students can only view active ones.
12. **Unique View Tracking (Flow 14)**: Added `CommunityMaterialView` model with a unique constraint on `(user_id, material_id)`. Incrementing `views_count` triggers only once per student per material. Refreshing or repeat views are ignored.

### Student Interactions & Moderation
13. **Instagram-Style Like Button (Flow 15)**: Integrated instant AJAX toggle behavior. Heart icon toggles between `♥ Liked` (filled, primary color) and `♡ Like` (outline, gray color). Dynamic counts update instantly without page reloads. Fallback form post operates normally.
14. **Ratings Submission (Flow 16)**: Standard dropdown submission allows rating updates, updating the material's `ratings_count` and `average_rating`.
15. **Reporting Control (Flows 17 & 18)**: Allows a student to report a material once. Duplicate reports by the same user are blocked.
16. **Moderation Score & Escalation (Flows 19, 20 & 21)**: Score updates programmatically on report. Materials with high risk are moved to status `under_review`. Non-active materials are excluded from normal student library views.

### Platform Admin Moderation Dashboard
17. **Admin Explorer & Queue (Flows 22, 23 & 24)**: Platform admins can view all materials, moderation queues, and detailed lists of report reasons.
18. **Admin Actions (Flows 25, 26, 27 & 28)**: Platform admins can hide materials (status `hidden`), restore materials (status `active`), or remove materials (status `removed`). Student visibility immediately updates.

### File Security & Smoke Testing
19. **Secure File Streaming (Flows 29 & 30)**: PDF files are stored outside the public static directory and streamed securely via `/files/community/<id>`. IDOR and role visibility checks prevent students from accessing files of hidden materials. Raw file paths are never exposed in templates.
20. **Link Safety (Flow 31)**: Links open in a separate window securely (`target="_blank"` with `rel="noopener noreferrer"`).
21. **Mobile UX (Flow 32)**: Interface layout scales cleanly to mobile viewports.
22. **Smoke Test Existing MVP (Flow 33)**: Verification confirmed login, student dashboard, official subjects, quiz pages, and subscription notifications operate normally.

---

## 3. Bugs Fixed During QA
* **SQLite Session Cache Divergence**: During test client requests, SQLAlchemy cached old instances in the test script's identity map. Added `db.session.expire_all()` to the test script context blocks to guarantee fresh SQLite database retrieval.
* **Orphaned Row Contamination**: Re-running QA scripts previously left rows in the view/like/rating/report tables because SQLite foreign keys were not auto-cascading. Added a database cleaning routine to completely purge test data associated with `s1@qa.com`, `s2@qa.com`, and `pa@qa.com` at the start of every test run.
* **Remove Action Alignment**: Patched the script assertions to match the soft-delete behavior of the Platform Admin remove action (setting status to `removed` instead of hard deleting).

---

## 4. Security & UX Checklist
* **Access Control**: Logged-in sessions are checked on every route. Impersonating platform admins can view pages correctly.
* **Path Obfuscation**: File download URLs are served as `/files/community/<id>`. No local folders or absolute paths are exposed to the browser.
* **AJAX Responsiveness**: Like toggle buttons trigger immediate UI optimistic updates and fetch updates asynchronously, providing a premium feel.

---

## 5. PythonAnywhere Deployment Notes
1. **Source Code**: Push updated files (`app/models.py`, `app/routes/student.py`, etc.).
2. **Database Schema Update**: Run the database migration script in your PythonAnywhere bash console:
   ```bash
   python migrate_db.py
   ```
   *Note: This is non-destructive and will only add the `community_material_views` table.*
3. **Reload App**: Reload your web application via the PythonAnywhere web dashboard tab.
