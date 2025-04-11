from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import login_required, current_user
import numpy as np
import pandas as pd
import ast
from sklearn.preprocessing import StandardScaler


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
    "height_cm", "weight_kg", "age", "crossing", "finishing", "heading_accuracy", 
    "short_passing", "volleys", "dribbling", "curve", "fk_accuracy", 
    "long_passing", "ball_control", "acceleration", "sprint_speed", "agility", 
    "reactions", "balance", "shot_power", "jumping", "stamina", "strength", 
    "long_shots", "aggression", "interceptions", "positioning", "vision", 
    "penalties", "composure", "defensive_awareness", "standing_tackle", 
    "sliding_tackle", "gk_diving", "gk_handling", "gk_kicking", 
    "gk_positioning", "gk_reflexes"
]

models_dict, selected_features_dict, pca_dict, scaler = load_models()


user_views = Blueprint('user_views', __name__, template_folder='../templates')

@user_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)


@user_views.route('/Home', methods=['GET'])
def index_page():

    #df = pd.read_csv('App/data/Single_Record_test.csv')

    #data = df['Name Alternative'].tolist()

    #This should go to log in, but for right now it does to this index page.

    players = get_all_players()

    return render_template('index.html', players=players)


@user_views.route('/data_entry', methods=['GET'])
def get_data_entry_page():

    players = get_all_players()
    
    return render_template('data_entry.html', players=players, attributes=player_attributes)



@user_views.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # firstname = request.form['firstname']
        # lastname = request.form['lastname']
        # faculty = request.form['faculty']
        username = request.form['username']
        # email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        temp_user = get_user_by_username(username)

        if temp_user:
          return render_template('SignUp.html', message="Username is already taken!")

        if password != confirm_password:
            return render_template('SignUp.html', message="Passwords do not match!")

        # Save user to the database
        create_user(username=username, password=password)

        #flash(f"Home", "success")

        return redirect("/Home") # Redirect to login after signup

    return render_template('SignUp.html')

@user_views.route('/data_entry', methods=['POST'])
def get_user_attr():

    players = get_all_players()

    try:
        
        input_data = {}
        for attr in player_attributes:
            value = request.form.get(attr, type=int)
            input_data[attr] = value if value is not None else 50

        
        test_player_df = pd.DataFrame([input_data])

        
        test_player_scaled = scaler.transform(test_player_df)
        test_player_scaled_df = pd.DataFrame(test_player_scaled, columns=test_player_df.columns)

        
        predictions = {}

        for pos in models_dict:
            model = models_dict[pos]
            selected_features = selected_features_dict[pos]
            pca = pca_dict.get(pos)

            
            if pca is not None:
                test_player_pca = pca.transform(test_player_scaled)
                pca_features = [f'PCA_{i+1}' for i in range(test_player_pca.shape[1])]
                test_player_data_input = pd.DataFrame(test_player_pca, columns=pca_features)[selected_features]
            else:
                test_player_data_input = test_player_scaled_df[selected_features]

            
            prob = model.predict_proba(test_player_data_input)[0][1]
            predictions[pos] = prob

        
        sorted_predictions = sorted(predictions.items(), key=lambda x: x[1], reverse=True)
        most_likely_position = sorted_predictions[0][0]
        top_probability = round(sorted_predictions[0][1] * 100, 2)

        user = get_user(current_user.id)


        # Update the user's attributes and prediction results
        #Make this a controller once it works
        if user:
            for key, value in input_data.items():
                setattr(user, key, value)  # Update player attributes
            user.most_likely_position = most_likely_position
            user.top_probability = top_probability
            user.predictions = predictions

            # Commit the changes to the database
            db.session.commit()

        return render_template('result.html', most_likely_position=most_likely_position, top_probability=top_probability, predictions=[(pos, round(prob * 100, 2)) for pos, prob in sorted_predictions])

    except Exception as e:
        return f"An error occurred: {e}", 500






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


