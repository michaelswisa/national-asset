from models.users import User
from services.hashing_pessword import check_password_hash


def authenticate_user(email, password):
    try:
        # חיפוש המשתמש בבסיס הנתונים לפי אימייל
        user = User.query.filter_by(email=email).first()
    except Exception as e:
        print(f"Database error: {e}")
        return None

    # בדיקה אם המשתמש קיים
    if user is None:
        return None

    check_password = check_password_hash(password, user.password)

    # בדיקה אם הסיסמה נכונה
    if check_password:
        return user
    return None

