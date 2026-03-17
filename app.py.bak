from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "hospital123"

# DATABASE CONNECTION
def db():
    return sqlite3.connect("hospital.db", check_same_thread=False)


# ---------------------- SEARCH ----------------------
@app.route("/search")
def search():
    name = request.args.get("name", "")

    con = db()
    cur = con.cursor()

    cur.execute(
        "SELECT * FROM patients WHERE name LIKE ?",
        ('%' + name + '%',)
    )

    data = cur.fetchall()
    con.close()

    return render_template("patients.html", patients=data)


# ---------------------- DASHBOARD ----------------------
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

    return render_template(
        "dashboard.html",
        patients=patients,
        doctors=doctors,
        appointments=appointments
    )


# ---------------------- LOGIN ----------------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        con = db()
        cur = con.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = cur.fetchone()
        con.close()

        if user:
            session["username"] = user[1]
            session["role"] = user[3]
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid Username or Password")

    return render_template("login.html")


# ---------------------- LOGOUT ----------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ---------------------- ADD USER ----------------------
@app.route("/add_user", methods=["GET", "POST"])
def add_user():

    if session.get("role") != "admin":
        return "Access Denied"

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        con = db()
        cur = con.cursor()

        cur.execute(
            "INSERT INTO users(username,password,role) VALUES (?,?,?)",
            (username, password, role)
        )

        con.commit()
        con.close()

        return redirect("/dashboard")

    return render_template("add_user.html")


# ---------------------- ADD PATIENT ----------------------
@app.route("/add_patient", methods=["GET", "POST"])
def add_patient():
    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        gender = request.form["gender"]
        mobile = request.form["mobile"]

        con = db()
        cur = con.cursor()

        cur.execute(
            "INSERT INTO patients(name,age,gender,mobile) VALUES (?,?,?,?)",
            (name, age, gender, mobile)
        )

        con.commit()
        con.close()

        return redirect("/patients")

    return render_template("add_patient.html")


# ---------------------- VIEW PATIENTS ----------------------
@app.route("/patients")
def patients():
    con = db()
    cur = con.cursor()

    cur.execute("SELECT * FROM patients")
    data = cur.fetchall()

    con.close()

    return render_template("patients.html", patients=data)


# ---------------------- ADD DOCTOR ----------------------
@app.route("/add_doctor", methods=["GET", "POST"])
def add_doctor():
    if request.method == "POST":

        name = request.form["name"]
        dept = request.form["dept"]

        con = db()
        cur = con.cursor()

        cur.execute(
            "INSERT INTO doctors(name,department) VALUES (?,?)",
            (name, dept)
        )

        con.commit()
        con.close()

        return redirect("/dashboard")

    return render_template("add_doctor.html")


# ---------------------- APPOINTMENT ----------------------
@app.route("/appointment", methods=["GET", "POST"])
def appointment():
    con = db()
    cur = con.cursor()

    cur.execute("SELECT * FROM patients")
    patients = cur.fetchall()

    cur.execute("SELECT * FROM doctors")
    doctors = cur.fetchall()

    if request.method == "POST":

        pid = request.form["patient"]
        did = request.form["doctor"]
        date = request.form["date"]
        time = request.form["time"]

        cur.execute(
            "INSERT INTO appointments(patient_id,doctor_id,date,time) VALUES (?,?,?,?)",
            (pid, did, date, time)
        )

        con.commit()
        con.close()

        return redirect("/dashboard")

    con.close()
    return render_template("appointment.html", patients=patients, doctors=doctors)


# ---------------------- ADMISSION ----------------------
@app.route("/admission", methods=["GET", "POST"])
def admission():
    con = db()
    cur = con.cursor()

    cur.execute("SELECT * FROM patients")
    patients = cur.fetchall()

    if request.method == "POST":

        pid = request.form["patient"]
        room = request.form["room"]
        date = request.form["date"]

        cur.execute(
            "INSERT INTO admissions(patient_id,room,admission_date) VALUES (?,?,?)",
            (pid, room, date)
        )

        con.commit()
        con.close()

        return redirect("/dashboard")

    con.close()
    return render_template("admission.html", patients=patients)


# ---------------------- BILLING ----------------------
@app.route("/billing", methods=["GET", "POST"])
def billing():
    con = db()
    cur = con.cursor()

    cur.execute("SELECT * FROM patients")
    patients = cur.fetchall()

    if request.method == "POST":

        pid = request.form["patient"]
        service = request.form["service"]
        amount = request.form["amount"]

        cur.execute(
            "INSERT INTO billing(patient_id,service,amount) VALUES (?,?,?)",
            (pid, service, amount)
        )

        con.commit()
        con.close()

        return redirect("/dashboard")

    con.close()
    return render_template("billing.html", patients=patients)


# ---------------------- EDIT PATIENT ----------------------
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_patient(id):
    con = db()
    cur = con.cursor()

    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        gender = request.form["gender"]
        mobile = request.form["mobile"]

        cur.execute(
            "UPDATE patients SET name=?,age=?,gender=?,mobile=? WHERE id=?",
            (name, age, gender, mobile, id)
        )

        con.commit()
        con.close()

        return redirect("/patients")

    cur.execute("SELECT * FROM patients WHERE id=?", (id,))
    patient = cur.fetchone()

    con.close()

    return render_template("edit_patient.html", patient=patient)


# ---------------------- DELETE PATIENT ----------------------
@app.route("/delete/<int:id>")
def delete(id):
    con = db()
    cur = con.cursor()

    cur.execute("DELETE FROM patients WHERE id=?", (id,))
    con.commit()
    con.close()

    return redirect("/patients")


# ---------------------- DISCHARGE ----------------------
@app.route("/discharge", methods=["GET", "POST"])
def discharge():
    con = db()
    cur = con.cursor()

    cur.execute("SELECT * FROM patients")
    patients = cur.fetchall()

    if request.method == "POST":

        pid = request.form["patient"]
        date = request.form["date"]
        summary = request.form["summary"]

        cur.execute(
            "INSERT INTO discharge(patient_id,discharge_date,summary) VALUES (?,?,?)",
            (pid, date, summary)
        )

        con.commit()
        con.close()

        return redirect("/dashboard")

    con.close()
    return render_template("discharge.html", patients=patients)


# ---------------------- RUN APP ----------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))