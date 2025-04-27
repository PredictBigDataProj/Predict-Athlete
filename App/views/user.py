from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for, current_app
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import login_required, current_user
import numpy as np
import pandas as pd
import ast
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import euclidean_distances
from App.database import db


from.index import index_views

from App.controllers import (
    create_user,
    get_all_users,
    get_all_users_json,
    jwt_required,
    get_all_players,
    load_models, get_user, get_user_by_username,
    create_derived_features,
    get_physical_attribute_stats
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
    "age"
    # "speed_strength_ratio",
    # "agility_height_ratio",
    # "jumping_height_ratio",
    # "stamina_weight_ratio",
    # "offensive_skills",
    # "defensive_skills",
    # "playmaking_skills",
    # "physical_dominance",
    # "technical_ability",
    # "speed_composite",
    # "goalkeeper_skills",
    # "offensive_defensive_diff",
    # "offensive_defensive_ratio",
    # "technical_physical_ratio",
    # "pressure_handling"
]



df = pd.read_csv('App/data/Finished_final_proj_3.csv')  # index=False avoids saving row indices


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
    physical_stats = get_physical_attribute_stats()
    return render_template('data_entry.html', attributes=player_attributes, physical_stats=physical_stats)



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
    #models_dict, selected_features_dict, pca_dict, scaler = load_models()

    models_dict = current_app.config['MODELS_DICT']
    selected_features_dict = current_app.config['SELECTED_FEATURES_DICT']
    pca_dict = current_app.config['PCA_DICT']
    scaler = current_app.config['SCALER']

    players = get_all_players()
    physical_stats = get_physical_attribute_stats()

    try:
        # Get input data from form
        input_data = {}
        for attr in player_attributes:
            value = request.form.get(attr, type=int)
            input_data[attr] = value if value is not None else 50
        
        # Validate physical attributes total
        physical_attrs = [
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
            ]
        physical_total = sum(input_data.get(attr, 0) for attr in physical_attrs)
        
        if physical_total > physical_stats["reasonable_max"]:
            flash("Your physical attributes total exceeds realistic values. Please redistribute your points.", "error")
            return render_template('data_entry.html', players=players, attributes=player_attributes, 
                                  physical_stats=physical_stats, input_data=input_data)
        
        # Continue with existing processing
        test_player_df = pd.DataFrame([input_data])
        test_player_df = create_derived_features(test_player_df)
        
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

        # user = get_user(current_user.id)


        # # Update the user's attributes and prediction results
        # #Make this a controller once it works
        # if user:
        #     for key, value in input_data.items():
        #         setattr(user, key, value)  
        #     user.most_likely_position = most_likely_position
        #     user.top_probability = top_probability
        #     user.predictions = predictions

            
        #     db.session.commit()


        combined_dict = {}


        for pos in models_dict.keys():
            combined_dict[pos] = {
                'model': models_dict[pos],                    
                'selected_features': selected_features_dict[pos],  
                'pca': pca_dict.get(pos, None)                 
            }



        #Here and bellow calcualtes simialr players to the data entered in the form.
        selected_features = combined_dict[most_likely_position]['selected_features']
        pca = combined_dict[most_likely_position].get('pca')  
        


        numerical_cols = [
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

        df_input = df[numerical_cols]

        
        df_scaled = scaler.transform(df_input)  
        df_scaled_df = pd.DataFrame(df_scaled, columns=numerical_cols)  


        

        # test_player_df = pd.DataFrame([input_data])

        # test_player_df = create_derived_features(test_player_df)

        
        # test_player_scaled = scaler.transform(test_player_df)
        # test_player_scaled_df = pd.DataFrame(test_player_scaled, columns=test_player_df.columns)

        test_player_input = test_player_df[numerical_cols]  # Numeric data for test player
        test_player_scaled = scaler.transform(test_player_input)  # Transform test player data
        test_player_scaled_df = pd.DataFrame(test_player_scaled, columns=numerical_cols)



        
        if pca is not None:
            


            df_pca = pca.transform(df_scaled_df)
            df_pca_df = pd.DataFrame(df_pca, columns=[f'PCA_{i+1}' for i in range(df_pca.shape[1])])
            
            
            selected_features_pca = [f'PCA_{i+1}' for i in range(df_pca.shape[1])]
            df_for_similarity = df_pca_df[selected_features_pca]
            
            
            test_player_pca = pca.transform(test_player_scaled_df)  
            test_player_pca_df = pd.DataFrame(test_player_pca, columns=[f'PCA_{i+1}' for i in range(df_pca.shape[1])])
            
            
            test_vector = test_player_pca_df[selected_features_pca]
        else:
            
            df_for_similarity = df_scaled_df[selected_features]
            test_vector = test_player_scaled_df[selected_features]


        
       #Using euclidean distance for the similarity, the loewr the distance is the better it works. right now it shows the distance as well. take out after just for testin as of now.
        distances = euclidean_distances(df_for_similarity, test_vector)
        df['similarity_score'] = distances  

        
        similar_players = df.sort_values(by='similarity_score').head(5) #Change the head number to give how much ever players you want to display when doing it.



        return render_template('result.html', most_likely_position=most_likely_position, top_probability=top_probability, predictions=[(pos, round(prob * 100, 2)) for pos, prob in sorted_predictions], similar_players=similar_players[['full_name', 'similarity_score']].to_dict(orient='records'))

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


