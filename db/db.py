import psycopg2
from psycopg2 import pool
from flask_sqlalchemy import SQLAlchemy
from config.config import load_config
from create_db import check_if_db_initialized, create_database, create_tables, insert_initial_user

# Load the configuration
config = load_config()

# Only create the database and tables if they do not exist (first run)
if not check_if_db_initialized():
    create_database()
    create_tables()
    insert_initial_user()

# Create a connection pool with minimum and maximum connections
connection_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=config['DB_MIN_CONNECT'],
    maxconn=config['DB_MAX_CONNECT'],
    dbname=config['DB_NAME'],
    user=config['DB_USER'],
    password=config['DB_PASSWORD'],
    host=config['DB_HOST'],
    port=config['DB_PORT']
)

def get_db_connection():
    try:
        # Get a connection from the pool
        conn = connection_pool.getconn()
        if conn:
            print("Successfully received connection from pool.")
            return conn
    except Exception as e:
        print(f"Error getting connection from pool: {e}")
        return None

def close_db_connection(conn):
    try:
        # Return the connection to the pool
        connection_pool.putconn(conn)
        print("Connection returned to pool.")
    except Exception as e:
        print(f"Error returning connection to pool: {e}")

def close_all_connections():
    try:
        # Close all connections in the pool
        connection_pool.closeall()
        print("All pool connections closed.")
    except Exception as e:
        print(f"Error closing all pool connections: {e}")

db_alchemy = SQLAlchemy()
