from flask import Flask
from blueprints.bp_users import bp_users
from blueprints.bp_login import bp_login
from db.db import db
from config.config import load_config

# טען את הקונפיגורציה
config = load_config()

app = Flask(__name__)

# הגדר את SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{config["DB_USER"]}:{config["DB_PASSWORD"]}@{config["DB_HOST"]}:{config["DB_PORT"]}/{config["DB_NAME"]}'
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
