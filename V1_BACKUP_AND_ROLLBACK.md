# V1 Backup and Rollback Procedures

This guide details how to backup the database and assets, create a Git tag for v1 Stable, and roll back if issues occur during the React page-by-page migration.

---

## 1. How to Backup the SQLite Database

SQLite database file is located at `instance/studyhub.db`.

### Locally (Windows/PowerShell):
Copy the database to a safe location outside the Git directory or to a dedicated backups folder:
```powershell
# Create backups folder
mkdir backups -Force

# Copy database with date stamp
Copy-Item "instance/studyhub.db" "backups/studyhub_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss').db"
```

### On PythonAnywhere:
Copy the database file in your console or File manager:
```bash
cp instance/studyhub.db backups/studyhub_backup_$(date +%Y%m%d_%H%M%S).db
```

---

## 2. How to Backup the Uploads Folder

All user study materials, PYQs, and college logos are stored in the `uploads/` directory.

### Locally (Windows/PowerShell):
Create a zip archive of the uploads folder:
```powershell
Compress-Archive -Path "uploads" -DestinationPath "backups/uploads_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss').zip" -Force
```

### On PythonAnywhere:
Create a compressed tarball:
```bash
tar -czvf backups/uploads_backup_$(date +%Y%m%d_%H%M%S).tar.gz uploads/
```

---

## 3. How to Create a Git Tag
To mark the current stable commit as version 1:
```bash
# Create local tag
git tag -a v1-stable -m "StudyHub College v1 Jinja/Flask Stable Release"

# Push tag to GitHub
git push origin v1-stable
```

---

## 4. How to Rollback to the V1 Tag
If a migration step fails and you need to restore the codebase to the stable Flask version:
```bash
# Fetch latest tags
git fetch --tags

# Revert local workspace to v1-stable tag
git checkout v1-stable

# Optional: Reset current branch to the tag (Warning: Discards local changes)
git reset --hard v1-stable
```

---

## 5. How to Restore Database Backup

If the SQLite schema becomes corrupt or data is lost during migrations:
1. Stop the web server or application process.
2. Delete the current database file:
   ```bash
   rm instance/studyhub.db
   ```
3. Copy your latest backup to the instance directory:
   ```bash
   cp backups/studyhub_backup_YYYYMMDD_HHMMSS.db instance/studyhub.db
   ```
4. Verify files permissions and start the server.

---

## 6. How to Restore Uploads Folder

1. Remove the current uploads directory:
   ```bash
   rm -rf uploads
   ```
2. Unpack the backup:
   * **Windows:**
     ```powershell
     Expand-Archive -Path "backups/uploads_backup_YYYYMMDD_HHMMSS.zip" -DestinationPath "."
     ```
   * **Linux/PythonAnywhere:**
     ```bash
     tar -xzvf backups/uploads_backup_YYYYMMDD_HHMMSS.tar.gz
     ```

---

## 7. Security Warning
> [!CAUTION]
> **DO NOT PUSH DATABASE OR UPLOAD FILES TO GITHUB.**
> The `instance/` folder and `uploads/` folder are listed in `.gitignore`. Ensure they are never committed to your public repository to prevent exposing user data, uploaded PDFs, or admin database credentials.
