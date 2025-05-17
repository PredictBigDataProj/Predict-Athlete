from App.models import Regular, Drill
from App.database import db 
import os
from werkzeug.utils import secure_filename
from sqlalchemy.exc import SQLAlchemyError


from .drill import (
    create_drill,
    get_drill, get_drill_by_name
)


def create_regular(username, firstname, lastname, email, password):
    newRegular = Regular(username, firstname, lastname, email, password)
    db.session.add(newRegular)
    
    try:
        db.session.commit()
        return True
    except Exception as e:
        print("[regular.create_regular] Error occurred while creating new regular: ", str(e))
        db.session.rollback()
        return False

def get_regular_by_id(id):
    try:
        regular = Regular.query.filter_by(ID=id).first()
        if regular:
            return regular
        else:
            return None
    except Exception as e:
        print(f"[regular.get_regular_by_id] Error occurred while fetching regular by ID {id}: ", str(e))
        return None


def get_regular_by_name(firstname, lastname):
    try:
        regular = Regular.query.filter_by(firstname=firstname, lastname=lastname).first()
        if regular:
            return regular
        else:
            return None
    except Exception as e:
        print(f"[regular.get_regular_by_name] Error occurred while fetching regular by name {firstname} {lastname}: ", str(e))
        return None


def get_regular_by_username(username):
    try:
        regular = Regular.query.filter_by(username=username).first()
        if regular:
            return regular
        else:
            return None
    except Exception as e:
        print(f"[regular.get_regular_by_username] Error occurred while fetching regular by username {username}: ", str(e))
        return None


def update_regular_profile(regular_id, firstname, lastname, email, profile_pic=None):
    try:
        regular = Regular.query.get(regular_id)

        if not regular:
            raise ValueError("Regular not found")

        regular.firstname = firstname
        regular.lastname = lastname
        regular.email = email

        if profile_pic and profile_pic.filename:
            filename = secure_filename(profile_pic.filename)
            upload_dir = os.path.join('App', 'static', 'uploads')
            os.makedirs(upload_dir, exist_ok=True)

            upload_path = os.path.join(upload_dir, filename)
            profile_pic.save(upload_path)

            regular.profile_pic = f'/static/uploads/{filename}'

        db.session.commit()
    except Exception as e:
        print(f"[regular.update_regular_profile] Error occurred while updating regular profile: {str(e)}")
        db.session.rollback()
        raise


def regular_create_drill(regular, name, details, difficulty, category):
    try:
        if create_drill(regular, name, details, difficulty, category):
            return True
        else:
            return False
    except Exception as e:
        print("[regular.regular_create_drill] Error occurred while creating drill:", str(e))
        return False



def add_favourite_drill(regular_id, drill_id,):
    try:

        regular = get_regular_by_id(regular_id)
        drill = get_drill(drill_id)

        

        if regular:
            if drill:
                if drill in regular.favouriteDrills:
                    regular.favouriteDrills.remove(drill)
                    drill.favouriteStatus = False
                    db.session.commit()
                    return drill
                else:
                    regular.favouriteDrills.append(drill)
                    drill.favouriteStatus = True
                    db.session.commit()
                    return drill
            else:
                return None
        else:
            return None


        # if new_comment:
        #     existing_review = Review.query.get(reviewID)

        #     if existing_review:
        #         existing_review.comments.append(new_comment)
        #         db.session.add(new_comment)
        #         db.session.commit()
        #         return new_comment
        #     else:
        #         return None
        # else:
        #     return None
    except SQLAlchemyError as e:
        print(f"[DB ERROR] add_favourite_drill: {e}")
        db.session.rollback()
        return None


def get_favourite_drills(regularID):
  try:
    regular = Regular.query.filter_by(ID=regularID).first()
    if regular:
        return regular.favouriteDrills
    else:
        None
  except SQLAlchemyError as e:
    print(f"[DB ERROR] get_favourite_drills: {e}")
    return []