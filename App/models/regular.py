from App.database import db
from .user import User



class Regular(User):
  __tablename__ = 'regular'
  ID = db.Column(db.Integer, db.ForeignKey('user.ID', name='fk_regular_user'), primary_key=True)
  favouriteDrills = db.relationship('Drill', backref='regularFavouriteDrills', lazy='joined')
  profile_pic = db.Column(db.Text, nullable=True)

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


  __mapper_args__ = {"polymorphic_identity": "regular"}

  def __init__(self, username, firstname, lastname, email, password):
    super().__init__(username=username,
                     firstname=firstname,
                     lastname=lastname,
                     email=email,
                     password=password)
    self.favouriteDrills = []
    self.profile_pic = "https://st3.depositphotos.com/4111759/13425/v/600/depositphotos_134255634-stock-illustration-avatar-icon-male-profile-gray.jpg"

  



  def to_json(self):
    return {
        "staffID":self.ID,
        "username":self.username,
        "firstname":self.firstname,
        "lastname":self.lastname,
        "email":self.email,
        "favouriteDrills": [drill.to_json() for drill in self.favouriteDrills]
    }

  def __repr__(self):
    return f'<Regular User {self.ID} :{self.email}>'