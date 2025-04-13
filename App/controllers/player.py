from App.models import Player
from App.database import db

def get_player_by_name(name):
    return Player.query.filter_by(name=name).first()


def get_all_players():
    return Player.query.all()

def get_player_by_position(position):

    players = get_all_players()
    matching_players = []
    
    for player in players:
        try:
            # Convert the 'position_groups' string to a list
            positions = ast.literal_eval(player.position_groups)
            
            # Check if the position exists in the player's positions
            if position in positions:
                matching_players.append(player)
        except (ValueError, SyntaxError):
            # If there's an error with literal_eval (invalid format), continue with next player
            continue
    
    return matching_players