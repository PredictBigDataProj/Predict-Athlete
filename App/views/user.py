from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from.index import index_views

from App.controllers import (
    create_user,
    get_all_users,
    get_all_users_json,
    jwt_required,
    get_all_players
)

player_attributes = [
    "height_cm", "weight_kg", "age", "crossing", "finishing", "heading_accuracy", 
    "short_passing", "volleys", "dribbling", "curve", "fk_accuracy", 
    "long_passing", "ball_control", "acceleration", "sprint_speed", "agility", 
    "reactions", "balance", "shot_power", "jumping", "stamina", "strength", 
    "long_shots", "aggression", "interceptions", "positioning", "vision", 
    "penalties", "composure", "defensive_awareness", "standing_tackle", 
    "sliding_tackle", "gk_diving", "gk_handling", "gk_kicking", 
    "gk_positioning", "gk_reflexes"
]

user_views = Blueprint('user_views', __name__, template_folder='../templates')

@user_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)


@user_views.route('/data_entry', methods=['GET'])
def get_data_entry_page():

    players = get_all_players()
    
    return render_template('data_entry.html', players=players, attributes=player_attributes)

@user_views.route('/data_entry', methods=['POST'])
def get_user_attr():

    players = get_all_players()

    for attr in player_attributes:
        
        attr = request.form.get(f'{attr}')
        User.attr = attr

    
    return redirect(url_for('user_views.get_data_entry_page'))




@user_views.route('/users', methods=['POST'])
def create_user_action():
    data = request.form
    flash(f"User {data['username']} created!")
    create_user(data['username'], data['password'])
    return redirect(url_for('user_views.get_user_page'))

@user_views.route('/api/users', methods=['GET'])
def get_users_action():
    users = get_all_users_json()
    return jsonify(users)

@user_views.route('/api/users', methods=['POST'])
def create_user_endpoint():
    data = request.json
    user = create_user(data['username'], data['password'])
    return jsonify({'message': f"user {user.username} created with id {user.id}"})

@user_views.route('/static/users', methods=['GET'])
def static_user_page():
  return send_from_directory('static', 'static-user.html')


