from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "hospital123"

# DATABASE CONNECTION
def db():
    con = sqlite3.connect("hospital.db")
    con.row_factory = sqlite3.Row   # ✅ THIS LINE IS MUST
    return con

# CREATE TABLES (IMPORTANT FOR RENDER)
def init_db():
    con = db()
    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, role TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS patients (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age TEXT, gender TEXT, mobile TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS doctors (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, department TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS appointments (id INTEGER PRIMARY KEY AUTOINCREMENT, patient_id INTEGER, doctor_id INTEGER, date TEXT, time TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS admissions (id INTEGER PRIMARY KEY AUTOINCREMENT, patient_id INTEGER, room TEXT, admission_date TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS billing (id INTEGER PRIMARY KEY AUTOINCREMENT, patient_id INTEGER, service TEXT, amount TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS discharge (id INTEGER PRIMARY KEY AUTOINCREMENT, patient_id INTEGER, discharge_date TEXT, summary TEXT)")

    # DEFAULT ADMIN USER
    cur.execute("SELECT * FROM users WHERE username='admin'")
    if not cur.fetchone():
        cur.execute("INSERT INTO users(username,password,role) VALUES ('admin','admin','admin')")

    con.commit()
    con.close()

init_db()

# LOGIN
@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return render_template("login.html", error="Enter username & password")

        con = db()
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username,password))
        user = cur.fetchone()
        con.close()

        if user:
            session["username"] = user[1]
            session["role"] = user[3]
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid Username or Password")

    return render_template("login.html")

# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# DASHBOARD
@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect("/")

    con = db()
    cur = con.cursor()

    cur.execute("SELECT COUNT(*) FROM patients")
    patients = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM doctors")
    doctors = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM appointments")
    appointments = cur.fetchone()[0]

    con.close()

    return render_template("dashboard.html", patients=patients, doctors=doctors, appointments=appointments)

# ADD PATIENT
@app.route("/add_patient", methods=["GET","POST"])
def add_patient():
    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        gender = request.form.get("gender")
        mobile = request.form.get("mobile")

        if not name:
            return "Name required"

        con = db()
        cur = con.cursor()
        cur.execute("INSERT INTO patients(name,age,gender,mobile) VALUES (?,?,?,?)",(name,age,gender,mobile))
        con.commit()
        con.close()

        return redirect("/patients")

    return render_template("add_patient.html")

# VIEW PATIENTS
@app.route("/patients")
def patients():
    con = db()
    cur = con.cursor()
    cur.execute("SELECT * FROM patients")
    data = cur.fetchall()
    con.close()
    return render_template("patients.html", patients=data)

# SEARCH
@app.route("/search")
def search():
    name = request.args.get("name")

    if not name:
        return redirect("/patients")

    con = db()
    cur = con.cursor()
    cur.execute("SELECT * FROM patients WHERE name LIKE ?", ('%'+name+'%',))
    data = cur.fetchall()
    con.close()

    return render_template("patients.html", patients=data)

# ADD DOCTOR
@app.route("/add_doctor", methods=["GET","POST"])
def add_doctor():
    if request.method == "POST":
        name = request.form.get("name")
        dept = request.form.get("dept")

        con = db()
        cur = con.cursor()
        cur.execute("INSERT INTO doctors(name,department) VALUES (?,?)",(name,dept))
        con.commit()
        con.close()

        return redirect("/dashboard")

    return render_template("add_doctor.html")

# APPOINTMENT
@app.route("/appointment", methods=["GET","POST"])
def appointment():
    con = db()
    cur = con.cursor()

    cur.execute("SELECT * FROM patients")
    patients = cur.fetchall()

    cur.execute("SELECT * FROM doctors")
    doctors = cur.fetchall()

    if request.method == "POST":
        pid = request.form.get("patient")
        did = request.form.get("doctor")
        date = request.form.get("date")
        time = request.form.get("time")

        cur.execute("INSERT INTO appointments(patient_id,doctor_id,date,time) VALUES (?,?,?,?)",(pid,did,date,time))
        con.commit()
        con.close()

        return redirect("/dashboard")

    return render_template("appointment.html", patients=patients, doctors=doctors)
#EDIT PATIENT 
@app.route("/edit/<int:id>", methods=["GET","POST"])
def edit_patient(id):

    con = db()
    cur = con.cursor()

    if request.method == "POST":
        cur.execute(
            "UPDATE patients SET name=?,age=?,gender=?,mobile=? WHERE id=?",
            (
                request.form.get("name"),
                request.form.get("age"),
                request.form.get("gender"),
                request.form.get("mobile"),
                id
            )
        )
        con.commit()
        con.close()
        return redirect("/patients")

    cur.execute("SELECT * FROM patients WHERE id=?", (id,))
    patient = cur.fetchone()
    con.close()

    if not patient:
        return "Patient not found"

    return render_template("edit_patient.html", patient=patient)
# RUN APP
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))