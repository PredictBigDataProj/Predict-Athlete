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
    load_models, get_user, get_user_by_username
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


#[
#     "height_cm", "weight_kg", "age", "crossing", "finishing", "heading_accuracy", 
#     "short_passing", "volleys", "dribbling", "curve", "fk_accuracy", 
#     "long_passing", "ball_control", "acceleration", "sprint_speed", "agility", 
#     "reactions", "balance", "shot_power", "jumping", "stamina", "strength", 
#     "long_shots", "aggression", "interceptions", "positioning", "vision", 
#     "penalties", "composure", "defensive_awareness", "standing_tackle", 
#     "sliding_tackle", "gk_diving", "gk_handling", "gk_kicking", 
#     "gk_positioning", "gk_reflexes"
# ]



models_dict, selected_features_dict, pca_dict, scaler = load_models()


league_views = Blueprint('league_views', __name__, template_folder='../templates')


@league_views.route('/league/<league_id>-<country>', methods=['GET'])
def get_league_page(league_id, country):

    print(f"League ID: {league_id}, Country: {country}")
    
    #PUT THE VISUALIZATIONS AND ANALYISIS IN THIS FUNCTION/ RENDERED TEMPLATE PAGE 

    return render_template('league.html', league_id=league_id, country=country)







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


