import psycopg2
from psycopg2 import sql
from config.config import load_config  # Importing the load_config function

# Create ENUM types in PostgreSQL
create_role_enum = """
CREATE TYPE user_role AS ENUM ('soldier', 'commander', 'manager');
"""

create_task_status_enum = """
CREATE TYPE task_status AS ENUM ('pending', 'in_progress', 'completed', 'cancelled');
"""

# Users table
create_users_table = """
CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    role user_role NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# Units table
create_units_table = """
CREATE TABLE Units (
    unit_id SERIAL PRIMARY KEY,
    unit_name VARCHAR(100) NOT NULL,
    parent_unit_id INTEGER REFERENCES Units(unit_id)
);
"""

# Soldiers table
create_soldiers_table = """
CREATE TABLE Soldiers (
    soldier_id SERIAL PRIMARY KEY,
    personal_number VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone_number VARCHAR(20),
    is_kosher BOOLEAN DEFAULT FALSE,
    receive_sms BOOLEAN DEFAULT TRUE,
    whatsapp_enabled BOOLEAN DEFAULT FALSE,
    unit_id INTEGER REFERENCES Units(unit_id)
);
"""

# Commanders table
create_commanders_table = """
CREATE TABLE Commanders (
    commander_id SERIAL PRIMARY KEY,
    rank VARCHAR(50) NOT NULL,
    unit_id INTEGER REFERENCES Units(unit_id)
);
"""

# Tasks table
create_tasks_table = """
CREATE TABLE Tasks (
    task_id SERIAL PRIMARY KEY,
    creator_id INTEGER REFERENCES Users(user_id),
    title VARCHAR(100) NOT NULL,
    description TEXT,
    status task_status NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    due_date DATE
);
"""

# Task Assignments table
create_task_assignments_table = """
CREATE TABLE Task_Assignments (
    assignment_id SERIAL PRIMARY KEY,
    task_id INTEGER REFERENCES Tasks(task_id),
    soldier_id INTEGER REFERENCES Soldiers(soldier_id),
    is_updated BOOLEAN DEFAULT FALSE,
    assigned_at TIMESTAMP
);
"""

# Locations table
create_locations_table = """
CREATE TABLE Locations (
    location_id SERIAL PRIMARY KEY,
    soldier_id INTEGER REFERENCES Soldiers(soldier_id),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    full_address VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# Addresses table
create_addresses_table = """
CREATE TABLE Addresses (
    address_id SERIAL PRIMARY KEY,
    soldier_id INTEGER REFERENCES Soldiers(soldier_id),
    city VARCHAR(100) NOT NULL,
    street VARCHAR(100) NOT NULL,
    house_number VARCHAR(10),
    postal_code VARCHAR(10)
);
"""

# Load configuration values from the .env file
config = load_config()

# Default database (for example, postgres) to create a new database
DEFAULT_DB = "postgres"

# Function to connect to the default database and create a new database if it doesn't exist
def create_database():
    try:
        conn = psycopg2.connect(
            dbname=DEFAULT_DB,
            user=config['DB_USER'],
            password=config['DB_PASSWORD'],
            host=config['DB_HOST'],
            port=config['DB_PORT']
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Check if the database exists
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname='{config['DB_NAME']}'")
        exists = cursor.fetchone()

        # Create the database if it doesn't exist
        if not exists:
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(config['DB_NAME'])))
            print(f"Database '{config['DB_NAME']}' created successfully.")
        else:
            print(f"Database '{config['DB_NAME']}' already exists.")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error creating database: {e}")

# Function to create tables in the database
def create_tables():
    try:
        conn = psycopg2.connect(
            dbname=config['DB_NAME'],
            user=config['DB_USER'],
            password=config['DB_PASSWORD'],
            host=config['DB_HOST'],
            port=config['DB_PORT']
        )
        cursor = conn.cursor()

        # Create tables based on the provided queries
        queries = [
            create_role_enum,
            create_task_status_enum,
            create_users_table,
            create_units_table,
            create_soldiers_table,
            create_commanders_table,
            create_tasks_table,
            create_task_assignments_table,
            create_locations_table,
            create_addresses_table,
        ]

        for query in queries:
            cursor.execute(query)
            print(f"Table created successfully: {query.split()[2]}")

        conn.commit()
        cursor.close()
        conn.close()
        print("All tables created successfully.")
    except Exception as e:
        print(f"Error creating tables: {e}")

# Function to insert the initial user into the Users table
def insert_initial_user():
    try:
        # Connect to the database
        conn = psycopg2.connect(
            dbname=config['DB_NAME'],
            user=config['DB_USER'],
            password=config['DB_PASSWORD'],
            host=config['DB_HOST'],
            port=config['DB_PORT']
        )
        cursor = conn.cursor()

        # Prepare the query to insert the initial user
        insert_query = """
        INSERT INTO Users (username, password, email, role)
        VALUES (%s, %s, %s, %s);
        """
        # Initial user details
        initial_user_data = ("admin", "password123", "admin@example.com", "manager")

        # Execute the insert query
        cursor.execute(insert_query, initial_user_data)
        conn.commit()
        print("Initial user created successfully.")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error inserting initial user: {e}")

# Main execution
if __name__ == '__main__':
    create_database()  # Create the database if it doesn't exist
    create_tables()    # Create all tables in the database
    insert_initial_user()  # Insert the initial user
