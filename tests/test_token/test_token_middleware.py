import pytest
import jwt
from datetime import datetime, timedelta
from flask import Flask, jsonify
from middleware.token_middleware import token_required, role_required
from config.config import get_secret_key

SECRET_KEY = get_secret_key()

@pytest.fixture
def client():
    app = Flask(__name__)

    # הגדרת נתיבים רק לצורכי בדיקה
    @app.route('/commander-only', methods=['GET'])
    @token_required
    @role_required(['commander', 'manager'])
    def commander_only_route(user_id, user_role):
        return jsonify({'message': f'Welcome commander or manager {user_id}'}), 200

    @app.route('/manager-only', methods=['GET'])
    @token_required
    @role_required(['manager'])
    def manager_only_route(user_id, user_role):
        return jsonify({'message': f'Welcome manager {user_id}'}), 200

    with app.test_client() as client:
        yield client


def generate_token(user_id, role, exp_hours=1):
    """פונקציה ליצירת טוקן לצורכי בדיקה"""
    expiration_time = datetime.now() + timedelta(hours=exp_hours)
    token = jwt.encode({
        'user_id': user_id,
        'role': role,
        'exp': expiration_time.timestamp()
    }, SECRET_KEY, algorithm='HS256')
    return token


def test_token_missing(client):
    response = client.get('/commander-only')
    assert response.status_code == 401
    assert 'Token is missing!' in response.json['message']


def test_token_invalid(client):
    headers = {'Authorization': 'Bearer invalidtoken123'}
    response = client.get('/commander-only', headers=headers)
    assert response.status_code == 401
    assert 'Invalid token' in response.json['message']



def test_token_expired(client):
    expired_token = generate_token(user_id=1, role='commander', exp_hours=-1)
    headers = {'Authorization': f'Bearer {expired_token}'}
    response = client.get('/commander-only', headers=headers)
    assert response.status_code == 401
    assert 'Token expired' in response.json['message']


def test_commander_access_granted(client):
    valid_token = generate_token(user_id=1, role='commander')
    headers = {'Authorization': f'Bearer {valid_token}'}
    response = client.get('/commander-only', headers=headers)
    assert response.status_code == 200
    assert 'Welcome commander or manager' in response.json['message']


def test_commander_access_denied(client):
    valid_token = generate_token(user_id=2, role='soldier')
    headers = {'Authorization': f'Bearer {valid_token}'}
    response = client.get('/commander-only', headers=headers)
    assert response.status_code == 403
    assert 'Access forbidden: insufficient permissions' in response.json['message']


def test_manager_access_granted(client):
    valid_token = generate_token(user_id=1, role='manager')
    headers = {'Authorization': f'Bearer {valid_token}'}
    response = client.get('/manager-only', headers=headers)
    assert response.status_code == 200
    assert 'Welcome manager' in response.json['message']


def test_manager_access_denied(client):
    valid_token = generate_token(user_id=2, role='commander')
    headers = {'Authorization': f'Bearer {valid_token}'}
    response = client.get('/manager-only', headers=headers)
    assert response.status_code == 403
    assert 'Access forbidden: insufficient permissions' in response.json['message']
