import pytest
from app import app
from flask import json


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


# נתוני המשתמש הקיים בבסיס הנתונים
existing_user_data = {
    'email': 'admin@example.com',
    'password': 'password123'  # הסיסמה המקורית שנשמרה כ-hashed
}


def test_login_success(client):
    # בדיקה להצלחה בהתחברות עם המשתמש הקיים
    response = client.post('/login', json=existing_user_data)
    assert response.status_code == 200
    assert 'Login successful' in response.json['message']
    assert 'token' in response.json
    assert 'user_id' in response.json


def test_login_missing_email(client):
    data = {
        'password': 'password123'
    }

    response = client.post('/login', json=data)
    assert response.status_code == 400
    assert 'Missing email or password' in response.json['message']


def test_login_missing_password(client):
    data = {
        'email': 'admin@example.com'
    }

    response = client.post('/login', json=data)
    assert response.status_code == 400
    assert 'Missing email or password' in response.json['message']


def test_login_invalid_credentials(client):
    data = {
        'email': 'admin@example.com',
        'password': 'wrongpassword'
    }

    response = client.post('/login', json=data)
    assert response.status_code == 401
    assert 'Invalid credentials' in response.json['message']


def test_login_invalid_email_format(client):
    data = {
        'email': 'invalid-email-format',
        'password': 'password123'
    }

    response = client.post('/login', json=data)
    assert response.status_code == 400
    assert 'Invalid email format' in response.json['message']
