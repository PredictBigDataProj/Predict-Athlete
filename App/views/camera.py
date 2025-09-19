
from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for, Response
# from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import login_required, login_user, current_user, logout_user

from .index import index_views
from App.models import User

# from App.controllers import (
#   create_user, jwt_authenticate, login,
#   get_regular_by_username, create_regular, generate_frames

# )


#READ ME IM IMPROTANT

#Look at the notebook to understnad the logic im improtant, trust me.

camera_views = Blueprint('camera_views', __name__, template_folder='../templates')


@camera_views.route('/camera', methods=['GET'])
def camera_page():
    return render_template('Camera.html')

@camera_views.route('/video', methods=['GET'])
def video_page():
    return render_template('Video.html')

@camera_views.route('/video_feed')
def video_feed():
    # Video streaming route
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')