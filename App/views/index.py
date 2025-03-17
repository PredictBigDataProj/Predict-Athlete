from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.controllers import create_user, initialize
import pandas as pd

index_views = Blueprint('index_views', __name__, template_folder='../templates')

df = pd.read_csv('/workspace/Predict-Athlete/App/data/Single_Record_test.csv')

@index_views.route('/', methods=['GET'])
def index_page():

    df = pd.read_csv('/workspace/Predict-Athlete/App/data/Single_Record_test.csv')

    data = df['Name Alternative'].tolist()
    return render_template('index.html', data=data)

@index_views.route('/init', methods=['GET'])
def init():
    initialize()
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})