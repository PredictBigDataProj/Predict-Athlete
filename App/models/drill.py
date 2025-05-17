from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from datetime import datetime
from sqlalchemy import func

class Drill(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), nullable=False, unique=True)
    category = db.Column(db.String(1000), nullable=False)
    difficulty = db.Column(db.String(1000), nullable=False)
    details = db.Column(db.String(1000), nullable=False)
    stats_Affected = db.Column(db.String, default='')
    dateCreated = db.Column(db.DateTime, server_default=func.now())
    createdByRegularID = db.Column(db.Integer, db.ForeignKey('regular.ID', name='fk_drill_regular'))




    def __init__(self, regular, name, category, difficulty, details):
        self.createdByRegularID = regular.ID
        self.name = name
        self.category = category
        self.difficulty = difficulty
        self.details = details
        # self.stats_Affected = stats_Affected

    def get_id(self):
        return self.ID

    def get_json(self):
        return{
            'drill_id': self.id,
            'name': self.name,
            "createdByRegularID": self.createdByRegularID,
            'category': self.category,
            'difficulty': self.difficulty,
            'details': self.details,
            "dateCreated": self.dateCreated.strftime("%d-%m-%Y %H:%M"),  # Format the date/time
            'stats_Affected': self.stats_Affected,
        }