


from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
# from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import login_required, login_user, current_user, logout_user

from .index import index_views
from App.models import User
from App.controllers import (
  create_user, jwt_authenticate, login,
  get_regular_by_username, create_regular

)

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=1, max=50)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=50)])
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=30)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('SignUp')

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')
'''
Page/Action Routes
'''


# @auth_views.route('/users', methods=['GET'])
# def get_user_page():
#   users = get_all_users()
#   return render_template('users.html', users=users)


@auth_views.route('/identify', methods=['GET'])
@login_required
def identify_page():
  return jsonify({
      'message':
      f"username: {current_user.username}, id : {current_user.ID}"
  })


# @auth_views.route('/login', methods=['POST'])
# def login_action():
#   data = request.form
#   message="Bad username or password"
#   user = login(data['username'], data['password'])
#   if user:
#     login_user(user)
#     return redirect("/Home")
    
#   return render_template('login.html', message=message)


# @auth_views.route('/logout', methods=['GET'])
# def logout_action():
#   logout_user()
#   return redirect("/")

# @auth_views.route('/login', methods=['GET'])
# def login_page():
#   return render_template('login.html')

# @auth_views.route('/login', methods=['POST'])
# def login_action():
#   data = request.form
#   message="Bad username or password"
  
#   user = login(data['username'], data['password'])
#   if user:
#     user_type = type(user)
#     print("User type:", user_type)
#     login_user(user)
#     if (user.user_type == "regular"):
#       return redirect("/Home")  # Redirect to student dashboard
#     # elif (user.user_type == "student"):
#     #   return redirect("/StudentHome")  # Redirect to staff dashboard
#     # elif (user.user_type == "admin"):
#     #   return redirect("/admin")
#   return render_template('login.html', message=message)



@auth_views.route('/login', methods=['GET', 'POST'])
def login_action():
    form = LoginForm()
    message = None
    if form.validate_on_submit():
        user = login(form.username.data, form.password.data)
        if user:
            login_user(user)
            if user.user_type == "regular":
                return redirect("/Home")
            # elif (user.user_type == "student"):
            #   return redirect("/StudentHome")  # Redirect to staff dashboard
            # elif (user.user_type == "admin"):
            #   return redirect("/admin")
        else:
            message = "Bad username or password"
    return render_template('login.html', form=form, message=message)

@auth_views.route('/logout', methods=['GET'])
@login_required
def logout_action():
  logout_user()
  return redirect("/Home")


@auth_views.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignupForm()

  if form.validate_on_submit():
    temp_user = get_regular_by_username(form.username.data)

    if temp_user:
      flash("Username is already taken!", "error")
      return render_template('SignUp.html', form=form, message="Username is already taken! message")

    # Save user to the database
    create_regular(
        firstname=form.firstname.data,
        lastname=form.lastname.data,
        username=form.username.data,
        email=form.email.data,
        password=form.password.data
    )

    regular = get_regular_by_username(form.username.data)
    login_user(regular)

    return redirect("/Home")

  return render_template('SignUp.html', form=form)


# @auth_views.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         firstname = request.form['firstname']
#         lastname = request.form['lastname']
#         username = request.form['username']
#         email = request.form['email']
#         password = request.form['password']
#         confirm_password = request.form['confirm_password']

#         temp_user = get_regular_by_username(username)

#         if temp_user:
#           return render_template('SignUp.html', message="Username is already taken!")

#         if password != confirm_password:
#             return render_template('SignUp.html', message="Passwords do not match!")

#         # Save user to the database
#         create_regular(
#             firstname=firstname, lastname=lastname, username=username,
#             email=email, password=password
#         )

#         regular = get_regular_by_username(username)
 
#         login_user(regular)

#         return redirect("/Home") # Redirect to login after signup

#     return render_template('SignUp.html')

#Just here to check the multiple user sessions
@auth_views.route('/whoami')
def whoami():
    if current_user.is_authenticated:
        return f"Logged in as {current_user.username}"
    else:
        return "Not logged in"

'''
API Routes
'''


# @auth_views.route('/api/users', methods=['GET'])
# def get_users_action():
#   users = get_all_users_json()
#   return jsonify(users)


# @auth_views.route('/api/users', methods=['POST'])
# def create_user_endpoint():
#   data = request.json
#   create_user(data['username'], data['password'])
#   return jsonify({'message': f"user {data['username']} created"})


# @auth_views.route('/api/login', methods=['POST'])
# def user_login_api():
#   data = request.json
#   token = jwt_authenticate(data['username'], data['password'])
#   if not token:
#     return jsonify(message='bad username or password given'), 401
#   return jsonify(access_token=token)


@auth_views.route('/api/identify', methods=['GET'])
def identify_user_action():
  return jsonify({
      'message':
      f"username: {jwt_current_user.username}, id : {jwt_current_user.ID}"
  })