from app import create_app
from app.extensions import db

def migrate():
    app = create_app()
    with app.app_context():
        db.create_all()
        print("Migration successful: Created any missing database tables.")

if __name__ == '__main__':
    migrate()
