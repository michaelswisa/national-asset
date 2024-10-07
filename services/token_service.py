import jwt
from datetime import datetime, timedelta
from config.config import get_secret_key

SECRET_KEY = get_secret_key()

def create_token(user_id, user_role):
    """יוצר טוקן JWT עבור המשתמש."""
    # שימוש ב- datetime.now() בשילוב עם timezone
    expiration_time = datetime.now() + timedelta(hours=1)  # טוקן בתוקף לשעה
    token = jwt.encode({
        'user_id': user_id,
        'role': user_role,  # רמת המשתמש
        'exp': expiration_time.timestamp()  # המרת זמן לתקופת UNIX
    }, SECRET_KEY, algorithm='HS256')
    return token

def decode_token(token):
    """מפרק טוקן JWT ומחזיר את פרטי המשתמש."""
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return data
    except jwt.ExpiredSignatureError:
        return None  # הטוקן פג תוקף
    except jwt.InvalidTokenError:
        return None  # טוקן לא חוקי
