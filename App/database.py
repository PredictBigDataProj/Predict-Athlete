from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()

def get_migrate(app):
    return Migrate(app, db)

# def create_db():
#     db.create_all()
    
def create_db():
    try:
        db.create_all()
    except Exception as e:
        print(f"Error creating tables: {e}")

# def init_db(app):
#     db.init_app(app)


def init_db(app):
    db.init_app(app)
    with app.app_context():
        try:
            db.create_all()
            
        except Exception as e:
            print(f"Error creating tables: {e}")