from flask import Blueprint, request, jsonify
from services.login_service import authenticate_user
from services.token_service import create_token
from utils.utils import is_valid_email

bp_login = Blueprint('login', __name__)



@bp_login.route('', methods=['POST'])
def login():
    data = request.get_json()

    if data is None:
        return jsonify({'message': 'No JSON data provided'}), 400

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Missing email or password'}), 400
    if not is_valid_email(email):
        return jsonify({'message': 'Invalid email format'}), 400

    # קריאה לפונקציה שמבצעת את האימות
    user = authenticate_user(email, password)

    if user:
        user_role = user.role_value  # השגת רמת המשתמש מתוך מאגר הנתונים

        # יצירת טוקן JWT
        token = create_token(user.user_id, user_role)

        return jsonify({'message': 'Login successful', 'user_id': user.user_id, 'token': token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401
