import os
import sqlite3
from app import create_app
from app.extensions import db

def migrate():
    app = create_app()
    with app.app_context():
        # First ensure all tables are created
        db.create_all()
        print("Standard tables initialized (db.create_all).")
        
        # Safe alteration of columns for SQLite
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
        if db_uri.startswith('sqlite:///'):
            # Extract database file path
            db_path = db_uri.replace('sqlite:///', '')
            # If relative path, resolve it relative to parent folder
            if not os.path.isabs(db_path):
                # app.root_path is d:\StudyHub\app, so d:\StudyHub\app\..\instance\studyhub.db is correct
                db_path = os.path.join(app.root_path, '..', db_path)
            db_path = os.path.abspath(db_path)
            
            if os.path.exists(db_path):
                print(f"Running custom SQLite schema upgrades on database: {db_path}")
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                # Check and add colleges.logo_path
                cursor.execute("PRAGMA table_info(colleges);")
                columns = cursor.fetchall()
                col_names = [col[1] for col in columns]
                if 'logo_path' not in col_names:
                    print("Adding 'logo_path' column to 'colleges' table...")
                    cursor.execute("ALTER TABLE colleges ADD COLUMN logo_path VARCHAR(256) DEFAULT NULL;")
                    conn.commit()
                else:
                    print("Column 'logo_path' already exists in 'colleges' table.")

                # Check and add college_requests.logo_path
                cursor.execute("PRAGMA table_info(college_requests);")
                columns = cursor.fetchall()
                col_names = [col[1] for col in columns]
                if 'logo_path' not in col_names:
                    print("Adding 'logo_path' column to 'college_requests' table...")
                    cursor.execute("ALTER TABLE college_requests ADD COLUMN logo_path VARCHAR(256) DEFAULT NULL;")
                    conn.commit()
                else:
                    print("Column 'logo_path' already exists in 'college_requests' table.")
                
                # Check and add users.onboarding_completed and profile_completed
                cursor.execute("PRAGMA table_info(users);")
                columns = cursor.fetchall()
                col_names = [col[1] for col in columns]
                if 'onboarding_completed' not in col_names:
                    print("Adding 'onboarding_completed' column to 'users' table...")
                    cursor.execute("ALTER TABLE users ADD COLUMN onboarding_completed BOOLEAN NOT NULL DEFAULT 0;")
                    conn.commit()
                else:
                    print("Column 'onboarding_completed' already exists in 'users' table.")
                    
                if 'profile_completed' not in col_names:
                    print("Adding 'profile_completed' column to 'users' table...")
                    cursor.execute("ALTER TABLE users ADD COLUMN profile_completed BOOLEAN NOT NULL DEFAULT 0;")
                    conn.commit()
                else:
                    print("Column 'profile_completed' already exists in 'users' table.")

                # Check and add subject_subscriptions.is_enabled
                cursor.execute("PRAGMA table_info(subject_subscriptions);")
                columns = cursor.fetchall()
                col_names = [col[1] for col in columns]
                if 'is_enabled' not in col_names:
                    print("Adding 'is_enabled' column to 'subject_subscriptions' table...")
                    cursor.execute("ALTER TABLE subject_subscriptions ADD COLUMN is_enabled BOOLEAN NOT NULL DEFAULT 1;")
                    conn.commit()
                else:
                    print("Column 'is_enabled' already exists in 'subject_subscriptions' table.")

                # Check and add subject_subscriptions.followed_at
                cursor.execute("PRAGMA table_info(subject_subscriptions);")
                columns = cursor.fetchall()
                col_names = [col[1] for col in columns]
                if 'followed_at' not in col_names:
                    print("Adding 'followed_at' column to 'subject_subscriptions' table...")
                    cursor.execute("ALTER TABLE subject_subscriptions ADD COLUMN followed_at DATETIME;")
                    cursor.execute("UPDATE subject_subscriptions SET followed_at = created_at;")
                    conn.commit()
                else:
                    print("Column 'followed_at' already exists in 'subject_subscriptions' table.")

                # Check and add college_subscriptions.followed_at
                cursor.execute("PRAGMA table_info(college_subscriptions);")
                columns = cursor.fetchall()
                col_names = [col[1] for col in columns]
                if 'followed_at' not in col_names:
                    print("Adding 'followed_at' column to 'college_subscriptions' table...")
                    cursor.execute("ALTER TABLE college_subscriptions ADD COLUMN followed_at DATETIME;")
                    cursor.execute("UPDATE college_subscriptions SET followed_at = created_at;")
                    conn.commit()
                else:
                    print("Column 'followed_at' already exists in 'college_subscriptions' table.")
                    
                conn.close()
            else:
                print(f"SQLite database file not found at: {db_path}")
        else:
            print("Non-SQLite database configured. Skipping custom SQLite alteration.")
            
    print("Database migration complete.")

if __name__ == '__main__':
    migrate()
