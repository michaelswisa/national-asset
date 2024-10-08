import pytest
from app import app, db
from services.token_service import create_token
from models.users import User  # מוודא שייבאת את מודל המשתמש


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def clean_up():
    yield
    with app.app_context():
        # מחיקת המשתמש testuser מהדאטאבייס
        user = User.query.filter_by(username='testuser').first()
        if user:
            db.session.delete(user)
            db.session.commit()


# יצירת טוקן עבור מנהל (ID 1) עם הרשאות 'manager'
admin_token = create_token(1, 'manager')


def test_create_user_success(client):
    data = {
        'username': 'testuser',
        'password': 'testpass',
        'email': 'test@example.com',
        'role': 'soldier'
    }

    # הוספת הטוקן לכותרת הבקשה
    headers = {
        'Authorization': f'Bearer {admin_token}'
    }

    response = client.post('/users', json=data, headers=headers)

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

    headers = {
        'Authorization': f'Bearer {admin_token}'
    }

    response = client.post('/users', json=data, headers=headers)

    assert response.status_code == 400
    assert 'Missing required fields' in response.json['error']


def test_create_user_duplicate_username(client):
    data = {
        'username': 'testuser',
        'password': 'testpass',
        'email': 'test@example.com',
        'role': 'soldier'
    }

    headers = {
        'Authorization': f'Bearer {admin_token}'
    }

    client.post('/users', json=data, headers=headers)
    response = client.post('/users', json=data, headers=headers)
    assert response.status_code == 400
    assert 'Username or email must be unique' in response.json['error']


def test_create_user_invalid_role(client):
    data = {
        'username': 'testuser',
        'password': 'testpass',
        'email': 'test@example.com',
        'role': 'invalid_role'
    }

    headers = {
        'Authorization': f'Bearer {admin_token}'
    }

    response = client.post('/users', json=data, headers=headers)
    assert response.status_code == 400
    assert 'Invalid value for the role' in response.json['error']


def test_create_user_invalid_email(client):
    data = {
        'username': 'testuser',
        'password': 'testpass',
        'email': 'invalid_email_format',
        'role': 'soldier'
    }

    headers = {
        'Authorization': f'Bearer {admin_token}'
    }

    response = client.post('/users', json=data, headers=headers)
    assert response.status_code == 400
    assert 'Invalid email format' in response.json['error']


def test_create_user_invalid_data_type(client):
    data = {
        'username': 'testuser',
        'password': 123456,  # מספר במקום מחרוזת
        'email': 'test@example.com',
        'role': 'soldier'
    }

    headers = {
        'Authorization': f'Bearer {admin_token}'
    }

    response = client.post('/users', json=data, headers=headers)
    assert response.status_code == 400
    assert 'Invalid data type for password' in response.json['error']
