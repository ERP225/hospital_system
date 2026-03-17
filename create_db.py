import sqlite3

con = sqlite3.connect("hospital.db")
cur = con.cursor()

cur.execute("""
CREATE TABLE patients(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
age INTEGER,
gender TEXT,
mobile TEXT
)
""")

cur.execute("""
CREATE TABLE doctors(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
department TEXT
)
""")

cur.execute("""
CREATE TABLE appointments(
id INTEGER PRIMARY KEY AUTOINCREMENT,
patient_id INTEGER,
doctor_id INTEGER,
date TEXT,
time TEXT
)
""")

cur.execute("""
CREATE TABLE admissions(
id INTEGER PRIMARY KEY AUTOINCREMENT,
patient_id INTEGER,
room TEXT,
admission_date TEXT
)
""")

cur.execute("""
CREATE TABLE billing(
id INTEGER PRIMARY KEY AUTOINCREMENT,
patient_id INTEGER,
service TEXT,
amount INTEGER
)
""")

cur.execute("""
CREATE TABLE discharge(
id INTEGER PRIMARY KEY AUTOINCREMENT,
patient_id INTEGER,
discharge_date TEXT,
summary TEXT
)
""")

con.commit()

cur.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
password TEXT,
role TEXT
)
""")

con.commit()
con.close()

