# Setup & Development Guide

## Environment Setup

1. **Python Setup**
   Ensure Python 3.10+ is installed.
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   *Note: requirements.txt is generated as development progresses.*

3. **Database Initialization**
   The application uses SQLite for the MVP. To initialize the database, a seed script will be provided.
   ```bash
   python seed.py
   ```

4. **Run the Server**
   ```bash
   flask --app run run --debug
   ```

## Seed Credentials & Admin Creation

**WARNING: These demo credentials are for local development only. Change/remove them before deployment.**

For local development and testing, `seed.py` will generate the following default accounts:

- **Platform Admin:**
  - Email: admin@studyhub.local
  - Password: admin123

- **College Admin:**
  - Email: collegeadmin@studyhub.local
  - Password: admin123
  - *Note: You can log in as Platform Admin to create additional College Admins securely via the College Details page.*

- **Student:**
  - Email: student@studyhub.local
  - Password: student123

### Creating a Production-Safe Platform Admin

Before deployment or to set up your real administrator account without using the weak seed credentials, use the provided CLI script:

```bash
python create_admin.py
# Or use non-interactive arguments:
python create_admin.py --name "Admin Name" --email "admin@example.com" --password "securepassword"
```
This script will prompt you for a Full Name, Email, and secure Password, or accept them directly as command-line arguments. It will then safely hash the password and create the Platform Admin account without exposing it. You can also create additional platform admins from the Admin Dashboard > Users section once logged in as a platform admin.

## Authentication & Role Redirect Flow

The application provides a single login interface at `/login`. After entering credentials:
- **Platform Admin** is redirected to `/admin/dashboard`.
- **College Admin** is redirected to `/college-admin/dashboard`.
- **Student** is redirected to `/student/dashboard`.

If a user tries to access a dashboard outside their permissions, they will be shown a themed **403 Forbidden** page. Custom themed pages are also served for **404 Not Found** and **500 Internal Server Error** status codes.

## Deployment & Mobile Usage

* **PythonAnywhere Free Tier Deployment**: Refer to [DEPLOYMENT_PYTHONANYWHERE_FREE.md](file:///d:/StudyHub/DEPLOYMENT_PYTHONANYWHERE_FREE.md) for step-by-step production hosting instructions.
* **PWA Mobile Installation**: Learn how to add the portal directly to Android/iOS home screens using the PWA capabilities in [PWA_MOBILE_INSTALL_GUIDE.md](file:///d:/StudyHub/PWA_MOBILE_INSTALL_GUIDE.md).
