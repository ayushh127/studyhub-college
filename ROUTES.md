# Routes Guide

This document lists all the proposed routes for the StudyHub College MVP.

## Public Routes
- `GET /` - Landing page
- `GET /about` - About page
- `GET /college/register` - College registration form
- `POST /college/register` - Submit college registration
- `GET /college/request-success` - Success page

## Auth Routes
- `GET /login` - Login page
- `POST /login` - Process login
- `GET /register` - Student registration page
- `POST /register` - Process student registration
- `GET /logout` - Logout
- `GET /forgot-password` - (Placeholder)
- `POST /forgot-password` - (Placeholder)

## Platform Admin Routes
- `GET /admin/dashboard`
- `GET /admin/college-requests`
- `GET /admin/college-requests/<id>`
- `POST /admin/college-requests/<id>/approve`
- `POST /admin/college-requests/<id>/reject`
- `GET /admin/colleges`
- `GET /admin/colleges/create`
- `POST /admin/colleges/create`
- `GET /admin/colleges/<id>`
- `GET /admin/colleges/<id>/edit` - Edit college details page
- `POST /admin/colleges/<id>/edit` - Submit edited college details
- `POST /admin/colleges/<id>/logo` - Upload/update college logo
- `POST /admin/colleges/<id>/logo/remove` - Remove college logo
- `GET /admin/colleges/<id>/admins/create`
- `POST /admin/colleges/<id>/admins/create`
- `POST /admin/colleges/<id>/activate`
- `POST /admin/colleges/<id>/deactivate`
- `GET /admin/community` - View all community materials (admin)
- `GET /admin/community/queue` - Moderation queue for flagged materials
- `GET /admin/community/reports/<id>` - View reports for a specific material
- `POST /admin/community/materials/<id>/hide` - Hide a community material
- `POST /admin/community/materials/<id>/restore` - Restore a community material
- `POST /admin/community/materials/<id>/remove` - Permanently remove a community material
- `GET /admin/users`
- `GET /admin/users/create-platform-admin`
- `POST /admin/users/create-platform-admin`
- `GET /admin/users/<id>`
- `POST /admin/users/<id>/activate`
- `POST /admin/users/<id>/deactivate`
- `GET /admin/audit-logs`
- `GET /admin/settings`

## Impersonation Routes
- `POST /admin/users/<id>/impersonate`
- `POST /admin/impersonation/exit`

## College Admin Routes
- `GET /college-admin/dashboard`
- `GET /college-admin/profile`
- `POST /college-admin/profile`

### Subjects & Units
- `GET /college-admin/subjects`
- `GET /college-admin/subjects/create`
- `POST /college-admin/subjects/create`
- `GET /college-admin/subjects/<id>`
- `GET /college-admin/subjects/<id>/edit`
- `POST /college-admin/subjects/<id>/edit`
- `POST /college-admin/subjects/<id>/delete`
- `GET /college-admin/subjects/<subject_id>/units/create`
- `POST /college-admin/subjects/<subject_id>/units/create`
- `GET /college-admin/units/<id>`
- `GET /college-admin/units/<id>/edit`
- `POST /college-admin/units/<id>/edit`
- `POST /college-admin/units/<id>/delete`

### Materials & PYQs
- `GET /college-admin/materials`
- `GET /college-admin/materials/upload`
- `POST /college-admin/materials/upload`
- `GET /college-admin/materials/<id>`
- `GET /college-admin/materials/<id>/edit`
- `POST /college-admin/materials/<id>/edit`
- `POST /college-admin/materials/<id>/delete`
- `POST /college-admin/materials/<id>/publish`
- `POST /college-admin/materials/<id>/unpublish`
- `GET /college-admin/pyqs`
- `GET /college-admin/pyqs/upload`
- `POST /college-admin/pyqs/upload`
- `GET /college-admin/pyqs/<id>`
- `GET /college-admin/pyqs/<id>/edit`
- `POST /college-admin/pyqs/<id>/edit`
- `POST /college-admin/pyqs/<id>/delete`
- `POST /college-admin/pyqs/<id>/publish`
- `POST /college-admin/pyqs/<id>/unpublish`

### Quizzes
- `GET /college-admin/quizzes`
- `GET /college-admin/quizzes/create`
- `POST /college-admin/quizzes/create`
- `GET /college-admin/quizzes/<id>`
- `GET /college-admin/quizzes/<id>/edit`
- `POST /college-admin/quizzes/<id>/edit`
- `POST /college-admin/quizzes/<id>/delete`
- `POST /college-admin/quizzes/<id>/publish`
- `POST /college-admin/quizzes/<id>/unpublish`
- `GET /college-admin/quizzes/<quiz_id>/questions/create`
- `POST /college-admin/quizzes/<quiz_id>/questions/create`
- `GET /college-admin/questions/<id>/edit`
- `POST /college-admin/questions/<id>/edit`
- `POST /college-admin/questions/<id>/delete`

### Reports
- `GET /college-admin/students`
- `GET /college-admin/students/<id>`
- `GET /college-admin/reports`

## Student Routes
- `GET /student/dashboard`
- `GET /student/dashboard-v2` - React-based student dashboard v2
- `GET /api/student/dashboard` - API route serving JSON data for the student dashboard v2
- `GET /student/onboarding` - First-time onboarding page
- `POST /student/onboarding/college` - Submit college selection during onboarding
- `POST /student/onboarding/complete` - Mark onboarding as complete
- `GET /student/select-college`
- `POST /student/select-college`
- `POST /student/colleges/<college_id>/toggle-follow` - Toggle follow status for the selected college (subscribing to all college updates)
- `POST /student/subjects/<subject_id>/toggle-follow` - Toggle follow status for a subject (subscribing to subject updates)
- `GET /student/subjects`
- `GET /student/subjects/<id>`
- `GET /student/units/<id>`
- `GET /student/materials/<id>`
- `GET /student/pyqs`
- `GET /student/pyqs/<id>`
- `GET /student/subjects/<id>/pyqs`
- `GET /student/quizzes`
- `GET /student/quizzes/<id>/start`
- `POST /student/quizzes/<id>/start`
- `GET /student/attempts/<attempt_id>`
- `POST /student/attempts/<attempt_id>/answer`
- `POST /student/attempts/<attempt_id>/submit`
- `GET /student/attempts/<attempt_id>/result`
- `GET /student/attempts/<attempt_id>/review`
- `GET /student/progress`
- `GET /student/profile`
- `POST /student/profile`
- `GET /student/notifications` - View all notifications
- `POST /student/notifications/<id>/read` - Mark a notification as read
- `POST /student/notifications/read-all` - Mark all notifications as read
- `GET /student/notifications/<id>/open` - Auto-mark read and redirect to notification target page
- `GET /student/community` - Community library material explorer (browsing, searching, filtering)
- `GET /student/community/upload` - Page to share community resources
- `POST /student/community/upload` - Submit community resource
- `GET /student/community/my-uploads` - List student's own shared resources
- `GET /student/community/users/<user_id>` - View public uploader profile and all materials uploaded by a student
- `GET /student/community/materials/<id>` - View details of a community material
- `POST /student/community/materials/<id>/like` - Toggle like status for a community material (supports AJAX JSON responses)
- `POST /student/community/materials/<id>/rate` - Submit or update rating for a community material
- `POST /student/community/materials/<id>/report` - Submit a report for a community material
- `GET /student/community/materials/<id>/edit` - Page to edit uploader's own community resource
- `POST /student/community/materials/<id>/edit` - Submit edited community resource
- `POST /student/community/materials/<id>/delete` - Soft-delete uploader's own community resource

## Secure File Routes
- `GET /files/materials/<id>`
- `GET /files/pyqs/<id>`
- `GET /files/community/<id>` - Secure access to community PDF downloads
- `GET /files/college-logos/<id>` - Serve college logo
