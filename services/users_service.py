from db.db import db
from models.users import User


from sqlalchemy.exc import IntegrityError, DataError

def create_user(data):
    user_name = data.get('username')
    password = data.get('password')
    email = data.get('email')
    role = data.get('role')

    if not user_name or not password or not email or not role:
        raise ValueError("Missing required fields")

    try:
        # יצירת אובייקט משתמש חדש
        new_user = User(username=user_name, password=password, email=email, role=role)
        db.session.add(new_user)
        db.session.commit()
        return new_user
    except IntegrityError as e:
        db.session.rollback()  # במידה ויש שגיאה מחזירים את השינויים אחורה
        if "unique constraint" in str(e.orig):
            raise ValueError("Username or email must be unique")
        else:
            raise e  # במידה ויש שגיאה אחרת, מחזירים את השגיאה המקורית
    except DataError as e:
        db.session.rollback()
        raise ValueError("Invalid value for the role. Please select a valid option.")
