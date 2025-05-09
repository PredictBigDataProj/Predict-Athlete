from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from App.database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)

    crossing = db.Column(db.Integer)
    finishing = db.Column(db.Integer)
    heading_accuracy = db.Column(db.Integer)
    short_passing = db.Column(db.Integer)
    volleys = db.Column(db.Integer)
    dribbling = db.Column(db.Integer)
    curve = db.Column(db.Integer)
    fk_accuracy = db.Column(db.Integer)
    long_passing = db.Column(db.Integer)
    ball_control = db.Column(db.Integer)
    acceleration = db.Column(db.Integer)
    sprint_speed = db.Column(db.Integer)
    agility = db.Column(db.Integer)
    reactions = db.Column(db.Integer)
    balance = db.Column(db.Integer)
    shot_power = db.Column(db.Integer)
    jumping = db.Column(db.Integer)
    stamina = db.Column(db.Integer)
    strength = db.Column(db.Integer)
    long_shots = db.Column(db.Integer)
    aggression = db.Column(db.Integer)
    interceptions = db.Column(db.Integer)
    positioning = db.Column(db.Integer)
    vision = db.Column(db.Integer)
    penalties = db.Column(db.Integer)
    composure = db.Column(db.Integer)
    defensive_awareness = db.Column(db.Integer)
    standing_tackle = db.Column(db.Integer)
    sliding_tackle = db.Column(db.Integer)
    gk_diving = db.Column(db.Integer)
    gk_handling = db.Column(db.Integer)
    gk_kicking = db.Column(db.Integer)
    gk_positioning = db.Column(db.Integer)
    gk_reflexes = db.Column(db.Integer)


    height_cm = db.Column(db.Integer)
    weight_kg = db.Column(db.Integer)
    age = db.Column(db.Integer)

    most_likely_position = db.Column(db.String(50))
    top_probability = db.Column(db.Float)
    predictions = db.Column(db.JSON)


    

    def __init__(self, username, password, input_data=None, most_likely_position=None, top_probability=None, predictions=None):
        self.username = username
        self.set_password(password)

        if input_data:
            for key, value in input_data.items():
                setattr(self, key, value)
        
        self.most_likely_position = most_likely_position
        self.top_probability = top_probability
        self.predictions = predictions

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username,
            'most_likely_position': self.most_likely_position,
            'top_probability': self.top_probability,
            'predictions': self.predictions
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

