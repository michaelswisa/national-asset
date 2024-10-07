from flask import Flask
from blueprints.bp_users import bp_users
from blueprints.bp_login import bp_login
from db.db import db_alchemy as db
from config.config import load_config
from flask_cors import CORS

# Load the configuration
config = load_config()

app = Flask(__name__)

# Set up SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{config["DB_USER"]}:{config["DB_PASSWORD"]}@{config["DB_HOST"]}:{config["DB_PORT"]}/{config["DB_NAME"]}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable tracking modifications
app.config['SQLALCHEMY_POOL_SIZE'] = config["DB_MAX_CONNECT"]  # Connection pool size
app.config['SQLALCHEMY_POOL_TIMEOUT'] = config["POOL_TIMEOUT"]  # Maximum wait time for a free connection

db.init_app(app)
CORS(app)
# Register blueprints
app.register_blueprint(bp_users, url_prefix='/users')
app.register_blueprint(bp_login, url_prefix='/login')

# Define a simple route to test the application
@app.route('/')
def index():
    return "Welcome to the Flask application!"

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
