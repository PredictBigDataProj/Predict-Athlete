from .user import create_user
import joblib 
import os
from App.database import db
import csv
from datetime import datetime
from App.models import Player
from App.default_config import DATA_PATH



# import numpy as np
# import pandas as pd
# from sklearn.preprocessing import StandardScaler
# from sklearn.decomposition import PCA
# from sklearn.feature_selection import RFE
# from sklearn.linear_model import LogisticRegression, Lasso
# from sklearn.ensemble import RandomForestClassifier
# from xgboost import XGBClassifier
# from sklearn.model_selection import train_test_split, GridSearchCV
# from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
# from imblearn.over_sampling import SMOTE



def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')
    import_csv_player('App/data/Finished_final_proj_3.csv')
    load_models()


def load_models():
    
    #DATA_PATH = current_app.config['DATA_PATH']

    
    positions = ["ST", "RWB", "RW", "RM", "RB", "LWB", "LW", "LM", "LB", "GK", "CM", "CF", "CDM", "CB", "CAM"]

    models_dict = {}
    selected_features_dict = {}
    pca_dict = {}

    for pos in positions:
        models_dict[pos] = joblib.load(os.path.join(DATA_PATH, f"{pos}_model_RF_XGB.pkl"))
        selected_features_dict[pos] = joblib.load(os.path.join(DATA_PATH, f"{pos}_features_RF_XGB.pkl"))
        

        pca_path = os.path.join(DATA_PATH, f"{pos}_pca_RF_XGB.pkl")
        if os.path.exists(pca_path):
            pca_dict[pos] = joblib.load(pca_path)
        else:
            pca_dict[pos] = None

        print (f'{pos} was loaded successfully!')


    scaler = joblib.load(os.path.join(DATA_PATH, "scaler_RF_XGB.pkl"))
    return models_dict, selected_features_dict, pca_dict, scaler

def import_csv_player(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:

            player = Player(
                player_id=int(row['player_id']),
                name=row['name'],
                full_name=row['full_name'],
                height_cm=int(row['height_cm']),
                weight_kg=int(row['weight_kg']),
                dob=datetime.strptime(row['dob'], '%Y-%m-%d'),  # Convert DOB to date object
                preferred_foot=row['preferred_foot'],
                body_type=row['body_type'],
                club_id=int(row['club_id']),
                club_name=row['club_name'],
                club_league_id=int(row['club_league_id']),
                club_league_name=row['club_league_name'],
                crossing=int(row['crossing']),
                finishing=int(row['finishing']),
                heading_accuracy=int(row['heading_accuracy']),
                short_passing=int(row['short_passing']),
                volleys=int(row['volleys']),
                dribbling=int(row['dribbling']),
                curve=int(row['curve']),
                fk_accuracy=int(row['fk_accuracy']),
                long_passing=int(row['long_passing']),
                ball_control=int(row['ball_control']),
                acceleration=int(row['acceleration']),
                sprint_speed=int(row['sprint_speed']),
                agility=int(row['agility']),
                reactions=int(row['reactions']),
                balance=int(row['balance']),
                shot_power=int(row['shot_power']),
                jumping=int(row['jumping']),
                stamina=int(row['stamina']),
                strength=int(row['strength']),
                long_shots=int(row['long_shots']),
                aggression=int(row['aggression']),
                interceptions=int(row['interceptions']),
                positioning=int(row['positioning']),
                vision=int(row['vision']),
                penalties=int(row['penalties']),
                composure=int(row['composure']),
                defensive_awareness=int(row['defensive_awareness']),
                standing_tackle=int(row['standing_tackle']),
                sliding_tackle=int(row['sliding_tackle']),
                gk_diving=int(row['gk_diving']),
                gk_handling=int(row['gk_handling']),
                gk_kicking=int(row['gk_kicking']),
                gk_positioning=int(row['gk_positioning']),
                gk_reflexes=int(row['gk_reflexes']),
                # season=row['Season'], #These ones i have to figure out how to use them and which ones to take when i finish get nations of players.
                # club_nation=row['Club/Nation'],
                # career_length=int(row['Career_length']),
                # start_year_final=int(row['Start_year_final']),
                # end_recent_year_final=int(row['End/Recent_year_final']),
                cam=int(row['CAM']),
                cb=int(row['CB']),
                cdm=int(row['CDM']),
                cf=int(row['CF']),
                cm=int(row['CM']),
                gk=int(row['GK']),
                lb=int(row['LB']),
                lm=int(row['LM']),
                lw=int(row['LW']),
                lwb=int(row['LWB']),
                rb=int(row['RB']),
                rm=int(row['RM']),
                rw=int(row['RW']),
                rwb=int(row['RWB']),
                st=int(row['ST']),
                age=int(row['age']),
                position_groups=row['position_groups'],
                nation=row['nation_Nation'],
                league=row['league_name'],
                preferred_foot_left=int(row['preferred_foot_Left']),
                preferred_foot_right=int(row['preferred_foot_Right']),

                speed_strength_ratio=float(row['speed_strength_ratio']),
                agility_height_ratio=float(row['agility_height_ratio']),
                jumping_height_ratio=float(row['jumping_height_ratio']),
                stamina_weight_ratio=float(row['stamina_weight_ratio']),
                offensive_skills=float(row['offensive_skills']),
                defensive_skills=float(row['defensive_skills']),
                playmaking_skills=float(row['playmaking_skills']),
                physical_dominance=float(row['physical_dominance']),
                technical_ability=float(row['technical_ability']),
                speed_composite=float(row['speed_composite']),
                goalkeeper_skills=float(row['goalkeeper_skills']),
                offensive_defensive_diff=float(row['offensive_defensive_diff']),
                offensive_defensive_ratio=float(row['offensive_defensive_ratio']),
                technical_physical_ratio=float(row['technical_physical_ratio']),
                pressure_handling =float(row['pressure_handling'])
            )
            db.session.add(player)  
        db.session.commit() 
    print("CSV data imported successfully!")