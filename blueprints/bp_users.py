from flask import Flask, Blueprint, jsonify, request
from db.db import db
from models.users import User
from services import users_service

bp_users = Blueprint('users', __name__)


@bp_users.route('', methods=['POST'])
def create_user():
    try:
        data = request.get_json()

        # קריאה לשירות יצירת משתמש
        user = users_service.create_user(data)

        # במידה והכל תקין, מחזירים תגובה חיובית
        return jsonify({"message": "User created successfully", 'user': user.to_dict()}), 201

    except ValueError as e:
        # טיפול בשגיאות שמגיעות מהשירות, כמו שם משתמש שכבר קיים או נתונים חסרים
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        print("Error", str(e))
        # טיפול בשגיאות לא צפויות אחרות
        return jsonify({"error": "An unexpected error occurred"}), 500
