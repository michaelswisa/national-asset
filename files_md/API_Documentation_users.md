# API Documentation users

## Endpoint

### Create User

- **URL**: `http://127.0.0.1:5000/users`
- **Method**: `POST`

### Request Body

The request should contain a JSON object with the following fields:

| Field     | Type     | Description                                     |
|-----------|----------|-------------------------------------------------|
| username  | string   | The username of the user.                       |
| password  | string   | The password of the user.                       |
| email     | string   | The email address of the user.                  |
| role      | string   | The role of the user. Must be one of the following: `soldier`, `commander`, `manager`. |

### Example Request

```json
{
    "username": "exampleUser",
    "password": "examplePass",
    "email": "example@example.com",
    "role": "soldier"
}
