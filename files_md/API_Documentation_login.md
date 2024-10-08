# API Documentation

## Endpoint

### User Login

- **URL**: `http://127.0.0.1:5000/login`
- **Method**: `POST`

### Request Body

The request should contain a JSON object with the following fields:

| Field    | Type     | Description                           |
|----------|----------|---------------------------------------|
| email    | string   | The email address of the user.       |
| password | string   | The password of the user.            |

### Example Request

```json
{
    "email": "example@example.com",
    "password": "examplePass"
}
```

### Response

On successful login, the response will contain:

| Field     | Type     | Description                                        |
|-----------|----------|----------------------------------------------------|
| message   | string   | A message indicating the login status.            |
| user_id   | string   | The ID of the logged-in user.                      |
| token     | string   | The JWT token generated for the user session.     |

### Example Response

#### Success (200)

```json
{
    "message": "Login successful",
    "user_id": "12345",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### Error (400)

```json
{
    "message": "Missing email or password"
}
```

#### Invalid Credentials (401)

```json
{
    "message": "Invalid credentials"
}
```
