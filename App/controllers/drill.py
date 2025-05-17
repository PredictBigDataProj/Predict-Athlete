from App.models import Drill
from App.database import db
import ast
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError




def create_drill(regular, name, details, difficulty, category): #stats_Affected
    if difficulty is None:
        return False
        

    # stats_Affected = ast.literal_eval(review.liked_by_staff or '[]')

    newDrill = Drill(regular=regular, 
                        name=name,
                        details=details,
                        difficulty=difficulty,
                        category=category)

    #newReview.comments=[]
    db.session.add(newDrill)

    try:
        db.session.commit()
        return newDrill
        #return True
    except SQLAlchemyError as e:
        print(f"[DB ERROR] create_drill: {e}")
        db.session.rollback()
        return None


def get_all_drills():
  try:
    drills = Drill.query.order_by(Drill.dateCreated.desc()).all()
    return drills
  except SQLAlchemyError as e:
    print(f"[DB ERROR] get_all_drills: {e}")
    return []

def get_drill_by_name(name):
    try:
        drill = Drill.query.filter_by(name=name).first()
        if drill:
            return drill
        else:
            return None
    except Exception as e:
        print(f"[drill.get_staff_by_username] Error occurred while fetching drill by name {name}: ", str(e))
        return None


def get_drill(id):
  try:
    drill = Drill.query.filter_by(ID=id).first()
    return drill if drill else None
  except SQLAlchemyError as e:
    print(f"[DB ERROR] get_drill: {e}")
    return None

