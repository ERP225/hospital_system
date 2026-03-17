import sqlite3

con = sqlite3.connect("hospital.db")
cur = con.cursor()

cur.execute("""
INSERT INTO users(username,password,role)
VALUES('admin','admin123','admin')
""")

con.commit()

print("Admin created")