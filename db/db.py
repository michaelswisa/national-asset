import psycopg2
from psycopg2 import pool
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv(dotenv_path='./config/.env')

# Get database connection details from environment variables
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_MIN_CONNECT = os.getenv('DB_MIN_CONNECT')
DB_MAX_CONNECT = os.getenv('DB_MAX_CONNECT')

# יצירת pool עם מינימום ומקסימום חיבורים
connection_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=DB_MIN_CONNECT,   # מינימום חיבורים במאגר
    maxconn=DB_MAX_CONNECT,   # מקסימום חיבורים במאגר
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)

def get_db_connection():
    try:
        # לוקחים חיבור מה-pool
        conn = connection_pool.getconn()
        if conn:
            print("Successfully received connection from pool.")
            return conn
    except Exception as e:
        print(f"Error getting connection from pool: {e}")
        return None

def close_db_connection(conn):
    try:
        # מחזירים את החיבור ל-pool
        connection_pool.putconn(conn)
        print("Connection returned to pool.")
    except Exception as e:
        print(f"Error returning connection to pool: {e}")

def close_all_connections():
    try:
        # סוגרים את כל החיבורים שבמאגר
        connection_pool.closeall()
        print("All pool connections closed.")
    except Exception as e:
        print(f"Error closing all pool connections: {e}")



db = SQLAlchemy()