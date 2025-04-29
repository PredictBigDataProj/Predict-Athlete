from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import login_required, current_user
import numpy as np
import pandas as pd
import ast
from sklearn.preprocessing import StandardScaler
from App.database import db


from.index import index_views

from App.controllers import (
    create_user,
    get_all_users,
    get_all_users_json,
    jwt_required,
    get_all_players,
    load_models, get_user, get_user_by_username, get_league_name_id
)


player_attributes = [
    "height_cm",
    "weight_kg",
    "crossing",
    "finishing",
    "heading_accuracy",
    "short_passing",
    "volleys",
    "dribbling",
    "curve",
    "fk_accuracy",
    "long_passing",
    "ball_control",
    "acceleration",
    "sprint_speed",
    "agility",
    "reactions",
    "balance",
    "shot_power",
    "jumping",
    "stamina",
    "strength",
    "long_shots",
    "aggression",
    "interceptions",
    "positioning",
    "vision",
    "penalties",
    "composure",
    "defensive_awareness",
    "standing_tackle",
    "sliding_tackle",
    "gk_diving",
    "gk_handling",
    "gk_kicking",
    "gk_positioning",
    "gk_reflexes",
    "age",
    "speed_strength_ratio",
    "agility_height_ratio",
    "jumping_height_ratio",
    "stamina_weight_ratio",
    "offensive_skills",
    "defensive_skills",
    "playmaking_skills",
    "physical_dominance",
    "technical_ability",
    "speed_composite",
    "goalkeeper_skills",
    "offensive_defensive_diff",
    "offensive_defensive_ratio",
    "technical_physical_ratio",
    "pressure_handling"
]

positions = ["ST", "RWB", "RW", "RM", "RB", "LWB", "LW", "LM", "LB", "GK", "CM", "CF", "CDM", "CB", "CAM"]




#models_dict, selected_features_dict, pca_dict, scaler = load_models()

df = pd.read_csv('App/data/Final_project_finished_4.csv')  # index=False avoids saving row indices


league_views = Blueprint('league_views', __name__, template_folder='../templates')


@league_views.route('/league/<league_id>-<country>', methods=['GET'])
def get_league_page(league_id, country):

    #print(f"League ID: {league_id}, Country: {country}")

    # bins = [15, 20, 25, 30, 35, 40, 45, 50] #These are the borders for the age groupings, can change depending.
    # labels = ['15-20', '21-25', '26-30', '31-35', '36-40', '41-45', '46-50'] #These are the age ranges, we can make this broader or more specfici depending.
    # df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=True)

    df['league_name_id'] = df['league_name'].apply(get_league_name_id)


    league_info = df[df['league_name_id'] == league_id]
    league_df = df[df['league_name_id'] == league_id]
    
    group_counts = league_df['age_group'].value_counts(normalize=True) * 100  # as percentage

    avg_age = league_df['age'].mean()
    min_age = league_df['age'].min()
    max_age = league_df['age'].max()
    max_career = league_df['league_Career_length'].max()
    min_career = league_df['league_Career_length'].min()
    avg_career = league_df['league_Career_length'].mean()
    age_counts = league_df['age'].value_counts()


    position_stats = []

    for pos in positions:
        pos_df = league_df[league_df[pos] == 1]
        group_counts_pos = pos_df['age_group'].value_counts(normalize=True) * 100  # as percentage

        if pos_df.empty:
            print(f'No players in this position: {pos}')
            print("\n")
        else:
            # avg_age_pos = pos_df['age'].mean()
            # min_age_pos = pos_df['age'].min()
            # max_age_pos = pos_df['age'].max()
            # max_career_pos = pos_df['league_Career_length'].max()
            # min_career_pos = pos_df['league_Career_length'].min()
            # avg_career_pos = pos_df['league_Career_length'].mean()


            pos_data = {
            'position': pos,
            'avg_age': pos_df['age'].mean(),
            'min_age': pos_df['age'].min(),
            'max_age': pos_df['age'].max(),
            'avg_career': pos_df['league_Career_length'].mean(),
            'min_career': pos_df['league_Career_length'].min(),
            'max_career': pos_df['league_Career_length'].max(),
            'pos_age_groups': group_counts_pos.to_dict()
            }
            position_stats.append(pos_data)


    print("\n")
    print(f"Overall for the {league_id} League")
    print(f'Average age is : {avg_age:.2f} years old')
    print(f'Youngest age is : {min_age:.2f} years old')
    print(f'Oldest age is : {max_age:.2f} years old')
    print(f'Max Career length is : {max_career:.2f} years')
    print(f'Min Career length is : {min_career:.2f} years')
    print(f'Average Career length is : {avg_career:.2f} years')
    print(f"Age Group Distribution for League: {league_id}")
    print(group_counts)
    print("\n")
    print("=======================================================================")


    avg_age = df[df['league_name_id'] == league_id]['age'].mean() #This is the same analysis as what is in the notebook, just use the df transformations in here and send the data as information tot he template.



    league_names = df[df['league_name_id'] == league_id]['league_name'].unique()
    nav_name = league_names[0] if len(league_names) > 0 else "League"
    #league_info = df
    #print(df[['league_name', 'league_name_id']])
    
    #PUT THE VISUALIZATIONS AND ANALYISIS IN THIS FUNCTION/ RENDERED TEMPLATE PAGE 

    return render_template('league.html', league_id=league_id, country=country, league_info=league_info.to_dict(orient='records'),
                            avg_age = avg_age, min_age = min_age, max_age = max_age,
                            avg_career = avg_career, min_career = min_career, max_career = max_career,
                            position_stats=position_stats,
                            age_groups=group_counts.to_dict(),
                            age_counts = age_counts.to_dict(),
                             nav_name=nav_name)







# @user_views.route('/users', methods=['POST'])
# def create_user_action():
#     data = request.form
#     flash(f"User {data['username']} created!")
#     create_user(data['username'], data['password'])
#     return redirect(url_for('user_views.get_user_page'))

# @user_views.route('/api/users', methods=['GET'])
# def get_users_action():
#     users = get_all_users_json()
#     return jsonify(users)

# @user_views.route('/api/users', methods=['POST'])
# def create_user_endpoint():
#     data = request.json
#     user = create_user(data['username'], data['password'])
#     return jsonify({'message': f"user {user.username} created with id {user.id}"})

# @user_views.route('/static/users', methods=['GET'])
# def static_user_page():
#   return send_from_directory('static', 'static-user.html')


