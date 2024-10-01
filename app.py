import os
from flask import Flask
from dotenv import load_dotenv
from blueprints.bp_users import bp_users
from db.db import db

# Load environment variables from .env file
load_dotenv(dotenv_path='./config/.env')

# Get database connection details from environment variables
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
app = Flask(__name__)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking


db.init_app(app)

# Register blueprints
app.register_blueprint(bp_users, url_prefix='/users')

# Define a simple route to test the application
@app.route('/')
def index():
    return "Welcome to the Flask App!"

# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)
