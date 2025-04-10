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

index_views = Blueprint('index_views', __name__, template_folder='../templates')

df = pd.read_csv('App/data/Single_Record_test.csv')

@index_views.route('/', methods=['GET'])
def index_page():

    df = pd.read_csv('App/data/Single_Record_test.csv')

    data = df['Name Alternative'].tolist()

    #This should go to log in, but for right now it does to this index page.

    players = get_all_players()

    return render_template('index.html', data=data, players=players)

@index_views.route('/init', methods=['GET'])
def init():
    initialize()
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})