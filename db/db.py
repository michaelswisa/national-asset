import psycopg2
from psycopg2 import pool
from flask_sqlalchemy import SQLAlchemy
from config.config import load_config

# טען את הקונפיגורציה
config = load_config()

# יצירת pool עם מינימום ומקסימום חיבורים
connection_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=config['DB_MIN_CONNECT'],   # מינימום חיבורים במאגר
    maxconn=config['DB_MAX_CONNECT'],   # מקסימום חיבורים במאגר
    dbname=config['DB_NAME'],
    user=config['DB_USER'],
    password=config['DB_PASSWORD'],
    host=config['DB_HOST'],
    port=config['DB_PORT']
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
