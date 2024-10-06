import os
from flask import Flask
from dotenv import load_dotenv
from blueprints.bp_users import bp_users
from blueprints.bp_login import bp_login
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

# הגדר את SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # בטל מעקב אחר שינויים

db.init_app(app)

# רשום blueprints
app.register_blueprint(bp_users, url_prefix='/users')
app.register_blueprint(bp_login, url_prefix='/login')

# הגדר נתיב פשוט לבדיקת האפליקציה
@app.route('/')
def index():
    return "ברוכים הבאים לאפליקציית Flask!"

# הפעל את אפליקציית Flask
if __name__ == '__main__':
    app.run(debug=True)