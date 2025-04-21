from App.models import Player
from App.database import db
import numpy as np
import pandas as pd

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



def create_derived_features(df):
    
    
    df_new = df.copy()
    
    
    df_new['speed_strength_ratio'] = df_new['sprint_speed'] / (df_new['strength'] + 0.1)  
    df_new['agility_height_ratio'] = df_new['agility'] / (df_new['height_cm'] + 0.1)
    df_new['jumping_height_ratio'] = df_new['jumping'] / (df_new['height_cm'] + 0.1)
    df_new['stamina_weight_ratio'] = df_new['stamina'] / (df_new['weight_kg'] + 0.1)
    
    
    df_new['offensive_skills'] = (df_new['finishing'] + df_new['shot_power'] + 
                                  df_new['long_shots'] + df_new['positioning'] + 
                                  df_new['volleys']) / 5
    
    df_new['defensive_skills'] = (df_new['defensive_awareness'] + df_new['standing_tackle'] + 
                                 df_new['sliding_tackle'] + df_new['interceptions']) / 4
    
    df_new['playmaking_skills'] = (df_new['short_passing'] + df_new['long_passing'] + 
                                   df_new['vision'] + df_new['ball_control']) / 4
    
    df_new['physical_dominance'] = (df_new['strength'] + df_new['aggression'] + 
                                    df_new['jumping']) / 3
    
    df_new['technical_ability'] = (df_new['dribbling'] + df_new['ball_control'] + 
                                  df_new['curve'] + df_new['fk_accuracy']) / 4
    
    df_new['speed_composite'] = (df_new['acceleration'] + df_new['sprint_speed'] + 
                                df_new['agility']) / 3
    
    
    df_new['goalkeeper_skills'] = (df_new['gk_diving'] + df_new['gk_handling'] + 
                                  df_new['gk_kicking'] + df_new['gk_positioning'] + 
                                  df_new['gk_reflexes']) / 5
    
    
    df_new['offensive_defensive_diff'] = df_new['offensive_skills'] - df_new['defensive_skills']
    df_new['offensive_defensive_ratio'] = df_new['offensive_skills'] / (df_new['defensive_skills'] + 0.1)
    df_new['technical_physical_ratio'] = df_new['technical_ability'] / (df_new['physical_dominance'] + 0.1)
    
    
    df_new['pressure_handling'] = (df_new['composure'] + df_new['reactions'] + df_new['balance']) / 3
    
    return df_new

