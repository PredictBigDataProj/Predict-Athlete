from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.controllers import create_user, initialize
from flask_login import login_required, login_user, current_user, logout_user
import textwrap
import pandas as pd

from App.controllers import (
    create_user,
    get_all_users,
    get_all_users_json,
    jwt_required,
    get_all_players, 
    create_drill, get_all_drills, get_drill_by_name,
    get_regular_by_username, get_regular_by_id
)

drills_views = Blueprint('drills_views', __name__, template_folder='../templates')


@drills_views.route('/drills', methods=['GET'])
def drills_page():
    drills = get_all_drills()
    return render_template('Drills.html', drills=drills)



@drills_views.route('/createDrillPage', methods=['GET'])
#Eventually put the login required here
def create_drill_page():
    return render_template('CreateDrill.html')

@drills_views.route('/createDrill', methods=['POST'])
def createDrill():



    data = request.form

    name = data['drill-name']
    difficulty = data['drill-difficulty']
    category = data['drill-category']
    raw_details = data['drill-details']

    details = "\n".join(textwrap.wrap(raw_details, width=80))  # Wrap text at 80 characters
    # details += f"{wrapped_review}"

    temp_drill = get_drill_by_name(name)

    if temp_drill:
        return render_template('CreateDrill.html', message="This Name is already in use!")



    regular = get_regular_by_id(current_user.ID)
    # status = 
    create_drill(regular, name, details, difficulty, category)
    # print(f'This is the status: {status}')
    print("Made it past the dupe name")
    return redirect("/drills")

    #return redirect(request.referrer)
    return render_template('Drills.html')