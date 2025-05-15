from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.controllers import create_user, initialize
import pandas as pd

from App.controllers import (
    create_user,
    get_all_users,
    get_all_users_json,
    jwt_required,
    get_all_players
)

drills_views = Blueprint('drills_views', __name__, template_folder='../templates')


@drills_views.route('/drills', methods=['GET'])
def drills_page():
    return render_template('Drills.html')