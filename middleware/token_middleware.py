from functools import wraps
from flask import request, jsonify, g
from services.token_service import decode_token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # בדיקה אם הטוקן נשלח בכותרת הבקשה
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        decoded_data, error = decode_token(token)
        if error:
            return jsonify({'message': error}), 401

        user_id = decoded_data['user_id']
        user_role = decoded_data['role']

        # שמירת המידע ב-g
        g.user_id = decoded_data['user_id']
        g.user_role = decoded_data['role']

        # המשך לפונקציה המקורית עם פרטי המשתמש
        return f(*args, **kwargs)

    return decorated


def role_required(allowed_roles):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            user_role = g.get('user_role')

            if user_role not in allowed_roles:
                return jsonify({'message': 'Access forbidden: insufficient permissions'}), 403

            return f(*args, **kwargs)
        return decorated
    return wrapper
