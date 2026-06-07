import sqlite3
import os

def migrate():
    db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'studyhub.db')
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}. Skipping alteration.")
        return
        
    print(f"Opening database at {db_path}...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if logo_path column already exists in college_requests table
    cursor.execute("PRAGMA table_info(college_requests);")
    columns = cursor.fetchall()
    column_names = [col[1] for col in columns]
    
    if 'logo_path' in column_names:
        print("Column 'logo_path' already exists in 'college_requests' table. No migration needed.")
    else:
        print("Adding column 'logo_path' to 'college_requests' table...")
        cursor.execute("ALTER TABLE college_requests ADD COLUMN logo_path VARCHAR(256) DEFAULT NULL;")
        conn.commit()
        print("Column 'logo_path' added successfully!")
        
    conn.close()

if __name__ == '__main__':
    migrate()
