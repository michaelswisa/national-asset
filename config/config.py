import os
from dotenv import load_dotenv


def get_path_env():
    # Get the current file directory
    current_dir = os.path.dirname(__file__)
    # Construct the path to the .env file
    dotenv_path = os.path.join(current_dir, '..', 'config', '.env')
    # Load the .env file
    load_dotenv(dotenv_path=dotenv_path)


def load_config():
    get_path_env()

    # Get database connection details from environment variables
    config = {
        'DB_NAME': os.getenv('DB_NAME'),
        'DB_USER': os.getenv('DB_USER'),
        'DB_PASSWORD': os.getenv('DB_PASSWORD'),
        'DB_HOST': os.getenv('DB_HOST'),
        'DB_PORT': os.getenv('DB_PORT'),
        'DB_MIN_CONNECT': os.getenv('DB_MIN_CONNECT'),
        'DB_MAX_CONNECT': os.getenv('DB_MAX_CONNECT'),
        'POOL_TIMEOUT': os.getenv('POOL_TIMEOUT'),
    }

    return config


def get_secret_key():
    get_path_env()
    # Get the secret key from environment variable
    return os.getenv('SECRET_KEY')
