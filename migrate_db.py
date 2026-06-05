import sqlite3
import os

db_path = os.path.join('instance', 'studyhub.db')

def migrate():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE college_requests ADD COLUMN admin_password_hash VARCHAR(256);")
        print("Migration successful: Added admin_password_hash to college_requests")
    except sqlite3.OperationalError as e:
        print(f"Migration error (column might already exist): {e}")
    conn.commit()
    conn.close()

if __name__ == '__main__':
    migrate()
