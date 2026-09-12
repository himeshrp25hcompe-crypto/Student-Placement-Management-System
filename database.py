import sqlite3

connection = sqlite3.connect("placement.db")

cursor = connection.cursor()

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

print("Database created successfully!")