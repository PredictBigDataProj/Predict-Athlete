# from flask import Blueprint, render_template, jsonify, request, flash, send_from_directory, flash, redirect, url_for
# from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies


# from.index import index_views

# from App.controllers import (
#     login
# )

# auth_views = Blueprint('auth_views', __name__, template_folder='../templates')




# '''
# Page/Action Routes
# '''    
# @auth_views.route('/users', methods=['GET'])
# def get_user_page():
#     users = get_all_users()
#     return render_template('users.html', users=users)

# @auth_views.route('/identify', methods=['GET'])
# @jwt_required()
# def identify_page():
#     return render_template('message.html', title="Identify", message=f"You are logged in as {current_user.id} - {current_user.username}")
    

# @auth_views.route('/login', methods=['POST'])
# def login_action():
#     data = request.form
#     token = login(data['username'], data['password'])
#     response = redirect(request.referrer)
#     if not token:
#         flash('Bad username or password given'), 401
#     else:
#         flash('Login Successful')
#         set_access_cookies(response, token) 
#     return response

# @auth_views.route('/logout', methods=['GET'])
# def logout_action():
#     response = redirect(request.referrer) 
#     flash("Logged Out!")
#     unset_jwt_cookies(response)
#     return response

# '''
# API Routes
# '''

# @auth_views.route('/api/login', methods=['POST'])
# def user_login_api():
#   data = request.json
#   token = login(data['username'], data['password'])
#   if not token:
#     return jsonify(message='bad username or password given'), 401
#   response = jsonify(access_token=token) 
#   set_access_cookies(response, token)
#   return response

# @auth_views.route('/api/identify', methods=['GET'])
# @jwt_required()
# def identify_user():
#     return jsonify({'message': f"username: {current_user.username}, id : {current_user.id}"})

# @auth_views.route('/api/logout', methods=['GET'])
# def logout_api():
#     response = jsonify(message="Logged Out!")
#     unset_jwt_cookies(response)
#     return response



from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import login_required, login_user, current_user, logout_user

from .index import index_views
from App.models import User
from App.controllers import (create_user, jwt_authenticate, login)

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')
'''
Page/Action Routes
'''


@auth_views.route('/users', methods=['GET'])
def get_user_page():
  users = get_all_users()
  return render_template('users.html', users=users)


@auth_views.route('/identify', methods=['GET'])
@login_required
def identify_page():
  return jsonify({
      'message':
      f"username: {current_user.username}, id : {current_user.ID}"
  })


@auth_views.route('/login', methods=['POST'])
def login_action():
  data = request.form
  message="Bad username or password"
  user = login(data['username'], data['password'])
  if user:
    # user_type = type(user)
    # print("User type:", user_type)
    login_user(user)
    #flash ("mesggae", "success")
    return redirect("/Home")  # Redirect to student dashboard
    
    # if (user.user_type == "staff"):
    #   return redirect("/getMainPage")  # Redirect to student dashboard
    # elif (user.user_type == "student"):
    #   return redirect("/StudentHome")  # Redirect to staff dashboard
    # elif (user.user_type == "admin"):
    #   return redirect("/admin")
  return render_template('login.html', message=message)


@auth_views.route('/logout', methods=['GET'])
def logout_action():
  logout_user()
  # data = request.form
  # user = login(data['username'], data['password'])
  #return 'logged out!'
  return redirect("/")


'''
API Routes
'''


@auth_views.route('/api/users', methods=['GET'])
def get_users_action():
  users = get_all_users_json()
  return jsonify(users)


@auth_views.route('/api/users', methods=['POST'])
def create_user_endpoint():
  data = request.json
  create_user(data['username'], data['password'])
  return jsonify({'message': f"user {data['username']} created"})


@auth_views.route('/api/login', methods=['POST'])
def user_login_api():
  data = request.json
  token = jwt_authenticate(data['username'], data['password'])
  if not token:
    return jsonify(message='bad username or password given'), 401
  return jsonify(access_token=token)


@auth_views.route('/api/identify', methods=['GET'])
@jwt_required()
def identify_user_action():
  return jsonify({
      'message':
      f"username: {jwt_current_user.username}, id : {jwt_current_user.ID}"
  })