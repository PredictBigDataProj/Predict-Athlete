from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.controllers import create_user, initialize
import textwrap
import pandas as pd

from App.controllers import (
    create_user,
    get_all_users,
    get_all_users_json,
    jwt_required,
    get_all_players, 
    create_drill, get_all_drills, get_drill_by_name,
    get_regular_by_username,
    add_favourite_drill, get_favourite_drills
)

favourites_views = Blueprint('favourites_views', __name__, template_folder='../templates')


@favourites_views.route('/favourites', methods=['GET'])
def favourites_page():
    regular = get_regular_by_username('bob')

    favourites = get_favourite_drills(regular.ID)
    return render_template('Favourites.html', favourites=favourites)


@favourites_views.route('/addFavourites/<int:drill_id>', methods=['GET'])
def add_Favourites_action(drill_id):
    regular = get_regular_by_username('bob')

    add_favourite_drill(regular.ID, drill_id)
    return redirect(request.referrer)