import sqlite3
import os

# Get the folder where this file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Create the database in the project folder
DATABASE = os.path.join(BASE_DIR, "placement.db")

connection = sqlite3.connect(DATABASE)

cursor = connection.cursor()

# Students table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    roll_no TEXT,
    branch TEXT,
    cgpa REAL,
    email TEXT
)
""")

# Companies table
cursor.execute("""
CREATE TABLE IF NOT EXISTS companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT,
    job_role TEXT,
    min_cgpa REAL,
    package TEXT,
    location TEXT
)
""")

# Applications table
cursor.execute("""
CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    company_id INTEGER,
    status TEXT
)
""")

connection.commit()
connection.close()

print("Database tables created successfully!")