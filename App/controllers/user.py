from App.models import User
from App.database import db


def create_user(username, firstname, lastname, password, email):
    newuser = User(username=username, firstname=firstname, lastname=lastname, password=password, email=email)
    db.session.add(newuser)
    try:
        db.session.commit()
        return newuser
    except Exception as e:
        print("[user.create_user] Error occurred while creating new user: ", str(e))
        db.session.rollback()
        return None

def get_user_by_username(username):
    try:
        user = User.query.filter_by(username=username).first()
        if user:
            return user
        else:
            return None
    except Exception as e:
        print("[user.get_user_by_username] Error occurred: ", str(e))
        return None

def get_user(id):
    try:
        user = User.query.get(id)
        if user:
            return user
        else:
            return None
    except Exception as e:
        print("[user.get_user] Error occurred: ", str(e))
        return None

def get_user_regular(regular):
    try:
        user = User.query.get(regular.ID)
        if user:
            return user
        else:
            return None
    except Exception as e:
        print("[user.get_user_regular] Error occurred: ", str(e))
        return None


def get_all_users():
    try:
        users = User.query.all()
        if users:
            return users
        else:
            return []
    except Exception as e:
        print("[user.get_all_users] Error occurred: ", str(e))
        return []

def get_all_users_json():
    try:
        users = User.query.all()
        if not users:
            return []
        users = [user.get_json() for user in users]
        return users
    except Exception as e:
        print("[user.get_all_users_json] Error occurred: ", str(e))
        return []

def update_user_username(id, username):
    try:
        user = get_user(id)
        if user:
            user.username = username
            db.session.commit()
            return True
        else:
            print("[user.update_user_username] Error: User not found.")
            return False
    except Exception as e:
        print("[user.update_user_username] Error occurred while updating username: ", str(e))
        db.session.rollback()
        return False
    

def update_name(userID, newFirstname, newLastName):
    try:
        user = get_user(userID)
        if user:
            user.firstname = newFirstname
            user.lastname = newLastName
            db.session.commit()
            return True
        else:
            print("[user.update_name] Error: User not found.")
            return False
    except Exception as e:
        print("[user.update_name] Error occurred while updating name: ", str(e))
        db.session.rollback()
        return False


def update_email(userID, newEmail):
    try:
        user = get_user(userID)
        if user:
            user.email = newEmail
            db.session.commit()
            return True
        else:
            print("[user.update_email] Error: User not found.")
            return False
    except Exception as e:
        print("[user.update_email] Error occurred while updating email: ", str(e))
        db.session.rollback()
        return False


def update_password(userID, newPassword):
    try:
        user = get_user(userID)
        if user:
            #Put a check to enter old password as well eventually
            user.set_password(newPassword)
            db.session.commit()
            return True
        else:
            print("[user.update_password] Error: User not found.")
            return False
    except Exception as e:
        print("[user.update_password] Error occurred while updating password: ", str(e))
        db.session.rollback()
        return False