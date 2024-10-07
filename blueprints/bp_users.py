from flask import Blueprint, jsonify, request
from services import users_service

bp_users = Blueprint('users', __name__)

@bp_users.route('', methods=['POST'])
def create_user():
    try:
        data = request.get_json()

        # Call the service to create a user
        user = users_service.create_user(data)

        # If everything is fine, return a positive response
        return jsonify({"message": "User created successfully", 'user': user.to_dict()}), 201

    except ValueError as e:
        # Handle errors coming from the service, such as existing username or missing data
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        print("Error:", str(e))
        # Handle any unexpected errors
        return jsonify({"error": "An unexpected error occurred"}), 500
