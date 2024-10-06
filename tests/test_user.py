import pytest
from app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_create_user_success(client):
    data = {
        'username': 'testuser',
        'password': 'testpass',
        'email': 'test@example.com',
        'role': 'soldier'
    }
    response = client.post('/users', json=data)
    assert response.status_code == 201
    assert 'User created successfully' in response.json['message']
    assert 'user' in response.json
    assert response.json['user']['username'] == 'testuser'
    assert response.json['user']['email'] == 'test@example.com'
    assert response.json['user']['role'] == 'soldier'

def test_create_user_missing_fields(client):
    data = {
        'username': 'testuser',
        'password': 'testpass'
    }
    response = client.post('/users', json=data)
    assert response.status_code == 400
    assert 'Missing required fields' in response.json['error']

def test_create_user_duplicate_username(client):
    data = {
        'username': 'testuser',
        'password': 'testpass',
        'email': 'test@example.com',
        'role': 'soldier'
    }
    client.post('/users', json=data)
    response = client.post('/users', json=data)
    assert response.status_code == 400
    assert 'Username or email must be unique' in response.json['error']

def test_create_user_invalid_role(client):
    data = {
        'username': 'testuser',
        'password': 'testpass',
        'email': 'test@example.com',
        'role': 'invalid_role'
    }
    response = client.post('/users', json=data)
    assert response.status_code == 400
    assert 'Invalid value for the role' in response.json['error']