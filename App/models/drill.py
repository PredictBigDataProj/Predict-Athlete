from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from datetime import datetime
from sqlalchemy import func

class Drill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), nullable=False, unique=True)
    category = db.Column(db.String(1000), nullable=False)
    difficulty = db.Column(db.String(1000), nullable=False)
    details = db.Column(db.String(1000), nullable=False)
    stats_Affected = db.Column(db.String, default='')
    dateCreated = db.Column(db.DateTime, server_default=func.now())




    def __init__(self, name, category, difficulty, details):
        self.name = name
        self.category = category
        self.difficulty = difficulty
        self.details = details
        # self.stats_Affected = stats_Affected


    def get_json(self):
        return{
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'difficulty': self.difficulty,
            'details': self.details,
            "dateCreated": self.dateCreated.strftime("%d-%m-%Y %H:%M"),  # Format the date/time
            'stats_Affected': self.stats_Affected,
        }