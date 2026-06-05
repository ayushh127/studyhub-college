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
- `GET /admin/colleges/<id>/admins/create`
- `POST /admin/colleges/<id>/admins/create`
- `POST /admin/colleges/<id>/activate`
- `POST /admin/colleges/<id>/deactivate`
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
- `GET /student/select-college`
- `POST /student/select-college`
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

## Secure File Routes
- `GET /files/materials/<id>`
- `GET /files/pyqs/<id>`
