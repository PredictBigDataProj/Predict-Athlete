from App.models import Player
from App.database import db

def get_player_by_name(name):
    return Player.query.filter_by(name=name).first()


def get_all_players():
    return Player.query.all()

