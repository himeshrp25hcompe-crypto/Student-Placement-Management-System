from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# =========================
# DATABASE
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "placement.db")


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


# =========================
# HOME
# =========================

@app.route("/")
def home():
    return render_template("index.html")


# =========================
# STUDENT DASHBOARD
# =========================

@app.route("/student")
def student():
    return render_template("student.html")


# =========================
# STUDENT - VIEW COMPANIES
# =========================

@app.route("/student/companies")
def student_companies():

    connection = get_db_connection()

    companies = connection.execute(
        "SELECT * FROM companies ORDER BY id"
    ).fetchall()

    connection.close()

    return render_template(
        "companies.html",
        companies=companies
    )


# =========================
# STUDENT - APPLY
# =========================

@app.route("/student/apply", methods=["POST"])
def apply_for_placement():

    student_id = request.form["student_id"]
    company_id = request.form["company_id"]

    connection = get_db_connection()

    student = connection.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    ).fetchone()

    if student is None:
        connection.close()

        return """
        <h2>Student Not Found</h2>
        <a href="/student/companies">Go Back</a>
        """

    company = connection.execute(
        "SELECT * FROM companies WHERE id = ?",
        (company_id,)
    ).fetchone()

    if company is None:
        connection.close()

        return """
        <h2>Company Not Found</h2>
        <a href="/student/companies">Go Back</a>
        """

    # CGPA eligibility
    if float(student["cgpa"]) < float(company["min_cgpa"]):

        connection.close()

        return f"""
        <h2>Not Eligible</h2>

        <p>Your CGPA: {student["cgpa"]}</p>
        <p>Required CGPA: {company["min_cgpa"]}</p>

        <p>You are not eligible for this company.</p>

        <br>

        <a href="/student/companies">Go Back</a>
        """

    # Duplicate application check
    existing = connection.execute(
        """
        SELECT id
        FROM applications
        WHERE student_id = ?
        AND company_id = ?
        """,
        (student_id, company_id)
    ).fetchone()

    if existing is not None:

        connection.close()

        return """
        <h2>Already Applied</h2>

        <p>You have already applied to this company.</p>

        <br>

        <a href="/student/companies">Go Back</a>
        """

    # Add application
    connection.execute(
        """
        INSERT INTO applications
        (student_id, company_id, status)
        VALUES (?, ?, ?)
        """,
        (student_id, company_id, "Applied")
    )

    connection.commit()
    connection.close()

    return """
    <h2>Application Submitted Successfully!</h2>

    <p>Your application has been submitted successfully.</p>

    <br>

    <a href="/student/companies">View Companies</a>

    <br><br>

    <a href="/student/applications">View Applications</a>
    """


# =========================
# STUDENT - VIEW APPLICATIONS
# =========================

@app.route("/student/applications")
def student_applications():

    connection = get_db_connection()

    applications = connection.execute(
        """
        SELECT
            applications.id,
            students.name,
            students.roll_no,
            companies.company_name,
            companies.job_role,
            companies.package,
            applications.status

        FROM applications

        JOIN students
        ON applications.student_id = students.id

        JOIN companies
        ON applications.company_id = companies.id

        ORDER BY applications.id
        """
    ).fetchall()

    connection.close()

    return render_template(
        "applications.html",
        applications=applications
    )


# =========================
# ADMIN DASHBOARD
# =========================

@app.route("/admin")
def admin():
    return render_template("admin.html")


# =========================
# ADMIN - MANAGE STUDENTS
# =========================

@app.route("/admin/students")
def admin_students():

    connection = get_db_connection()

    students = connection.execute(
        "SELECT * FROM students ORDER BY id"
    ).fetchall()

    connection.close()

    return render_template(
        "admin_students.html",
        students=students
    )


# =========================
# ADMIN - ADD STUDENT
# =========================

@app.route("/admin/students/add", methods=["POST"])
def add_student():

    name = request.form["name"]
    roll_no = request.form["roll_no"]
    branch = request.form["branch"]
    cgpa = request.form["cgpa"]
    email = request.form["email"]

    connection = get_db_connection()

    connection.execute(
        """
        INSERT INTO students
        (name, roll_no, branch, cgpa, email)
        VALUES (?, ?, ?, ?, ?)
        """,
        (name, roll_no, branch, cgpa, email)
    )

    connection.commit()
    connection.close()

    return redirect("/admin/students")


# =========================
# ADMIN - EDIT STUDENT
# =========================

@app.route("/admin/students/edit/<int:student_id>", methods=["POST"])
def edit_student(student_id):

    name = request.form["name"]
    roll_no = request.form["roll_no"]
    branch = request.form["branch"]
    cgpa = request.form["cgpa"]
    email = request.form["email"]

    connection = get_db_connection()

    connection.execute(
        """
        UPDATE students
        SET name = ?,
            roll_no = ?,
            branch = ?,
            cgpa = ?,
            email = ?
        WHERE id = ?
        """,
        (name, roll_no, branch, cgpa, email, student_id)
    )

    connection.commit()
    connection.close()

    return redirect("/admin/students")


# =========================
# ADMIN - DELETE STUDENT
# =========================

@app.route(
    "/admin/students/delete/<int:student_id>",
    methods=["POST"]
)
def delete_student(student_id):

    connection = get_db_connection()

    connection.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )

    connection.commit()
    connection.close()

    return redirect("/admin/students")


# =========================
# ADMIN - MANAGE COMPANIES
# =========================

@app.route("/admin/companies")
def admin_companies():

    connection = get_db_connection()

    companies = connection.execute(
        "SELECT * FROM companies ORDER BY id"
    ).fetchall()

    connection.close()

    return render_template(
        "admin_companies.html",
        companies=companies
    )


# =========================
# ADMIN - ADD COMPANY
# =========================

@app.route("/admin/companies/add", methods=["POST"])
def add_company():

    company_name = request.form["company_name"]
    job_role = request.form["job_role"]
    min_cgpa = request.form["min_cgpa"]
    package = request.form["package"]
    location = request.form["location"]

    connection = get_db_connection()

    connection.execute(
        """
        INSERT INTO companies
        (company_name, job_role, min_cgpa, package, location)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            company_name,
            job_role,
            min_cgpa,
            package,
            location
        )
    )

    connection.commit()
    connection.close()

    return redirect("/admin/companies")


# =========================
# ADMIN - EDIT COMPANY
# =========================

@app.route(
    "/admin/companies/edit/<int:company_id>",
    methods=["POST"]
)
def edit_company(company_id):

    company_name = request.form["company_name"]
    job_role = request.form["job_role"]
    min_cgpa = request.form["min_cgpa"]
    package = request.form["package"]
    location = request.form["location"]

    connection = get_db_connection()

    connection.execute(
        """
        UPDATE companies
        SET company_name = ?,
            job_role = ?,
            min_cgpa = ?,
            package = ?,
            location = ?
        WHERE id = ?
        """,
        (
            company_name,
            job_role,
            min_cgpa,
            package,
            location,
            company_id
        )
    )

    connection.commit()
    connection.close()

    return redirect("/admin/companies")


# =========================
# ADMIN - DELETE COMPANY
# =========================

@app.route(
    "/admin/companies/delete/<int:company_id>",
    methods=["POST"]
)
def delete_company(company_id):

    connection = get_db_connection()

    connection.execute(
        "DELETE FROM companies WHERE id = ?",
        (company_id,)
    )

    connection.commit()
    connection.close()

    return redirect("/admin/companies")


# =========================
# ADMIN - VIEW APPLICATIONS
# =========================

@app.route("/admin/applications")
def admin_applications():

    connection = get_db_connection()

    applications = connection.execute(
        """
        SELECT
            applications.id,
            students.name,
            students.roll_no,
            companies.company_name,
            companies.job_role,
            companies.package,
            applications.status

        FROM applications

        JOIN students
        ON applications.student_id = students.id

        JOIN companies
        ON applications.company_id = companies.id

        ORDER BY applications.id
        """
    ).fetchall()

    connection.close()

    return render_template(
        "admin_applications.html",
        applications=applications
    )


# =========================
# ADMIN - UPDATE APPLICATION STATUS
# =========================

@app.route(
    "/admin/applications/update/<int:application_id>",
    methods=["POST"]
)
def update_application_status(application_id):

    status = request.form["status"]

    connection = get_db_connection()

    connection.execute(
        """
        UPDATE applications
        SET status = ?
        WHERE id = ?
        """,
        (status, application_id)
    )

    connection.commit()
    connection.close()

    return redirect("/admin/applications")


# =========================
# RUN FLASK
# =========================

if __name__ == "__main__":
    app.run(debug=True)