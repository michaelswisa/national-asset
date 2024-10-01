import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

# יצירת סוגי ENUM ב-PostgreSQL
create_role_enum = """
CREATE TYPE user_role AS ENUM ('soldier', 'commander', 'manager');
"""

create_task_status_enum = """
CREATE TYPE task_status AS ENUM ('pending', 'in_progress', 'completed', 'cancelled');
"""

# טבלת Users
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

# טבלת Units
create_units_table = """
CREATE TABLE Units (
    unit_id SERIAL PRIMARY KEY,
    unit_name VARCHAR(100) NOT NULL,
    parent_unit_id INTEGER REFERENCES Units(unit_id)
);
"""

# טבלת Soldiers
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

# טבלת Commanders
create_commanders_table = """
CREATE TABLE Commanders (
    commander_id SERIAL PRIMARY KEY,
    rank VARCHAR(50) NOT NULL,
    unit_id INTEGER REFERENCES Units(unit_id)
);
"""

# טבלת Tasks
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

# טבלת Task_Assignments
create_task_assignments_table = """
CREATE TABLE Task_Assignments (
    assignment_id SERIAL PRIMARY KEY,
    task_id INTEGER REFERENCES Tasks(task_id),
    soldier_id INTEGER REFERENCES Soldiers(soldier_id),
    is_updated BOOLEAN DEFAULT FALSE,
    assigned_at TIMESTAMP
);
"""

# טבלת Locations
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

#טבלת Addresses
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

# טוענים את משתני הסביבה מקובץ .env
load_dotenv(dotenv_path='../config/.env')

# מקבלים את ערכי החיבור ממערכת הסביבה
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

# מסד נתונים ברירת מחדל (למשל postgres) ליצירת מסד חדש
DEFAULT_DB = "postgres"


# חיבור למסד ברירת מחדל כדי ליצור את מסד הנתונים אם הוא לא קיים
def create_database():
    try:
        conn = psycopg2.connect(
            dbname=DEFAULT_DB,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # בדיקה אם מסד הנתונים קיים
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname='{DB_NAME}'")
        exists = cursor.fetchone()

        # יצירת מסד הנתונים אם הוא לא קיים
        if not exists:
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
            print(f"Database '{DB_NAME}' created successfully.")
        else:
            print(f"Database '{DB_NAME}' already exists.")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error creating database: {e}")


# פונקציה ליצירת טבלאות במסד הנתונים
def create_tables():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = conn.cursor()

        # יצירת הטבלאות לפי השאילתות שסיפקת
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


if __name__ == '__main__':
    create_database()  # יצירת מסד הנתונים אם הוא לא קיים
    create_tables()  # יצירת כל הטבלאות במסד הנתונים
