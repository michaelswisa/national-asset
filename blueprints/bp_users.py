from flask import Flask, Blueprint, jsonify, request
from db.db import db
from models.users import User

bp_users  = Blueprint('users',__name__)

@bp_users.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(username=data['username'], password=data['password'], email=data['email'], role=data['role'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully", 'user': new_user.to_dict()}), 201