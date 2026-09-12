import sqlite3


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():
    return sqlite3.connect("placement.db")


# =========================================================
# INPUT VALIDATION
# =========================================================

def get_integer(message):
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Please enter a valid number.")


def get_float(message):
    while True:
        try:
            return float(input(message))
        except ValueError:
            print("Please enter a valid number.")


def get_cgpa(message):
    while True:
        cgpa = get_float(message)

        if 0 <= cgpa <= 10:
            return cgpa

        print("CGPA must be between 0 and 10.")


# =========================================================
# STUDENT FUNCTIONS
# =========================================================

def add_student():
    print("\n===== ADD STUDENT =====")

    name = input("Enter student name: ")
    roll_no = input("Enter roll number: ")
    branch = input("Enter branch: ")
    cgpa = get_cgpa("Enter CGPA: ")
    email = input("Enter email: ")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id FROM students WHERE roll_no = ?",
        (roll_no,)
    )

    if cursor.fetchone() is not None:
        print("\nStudent with this roll number already exists.")
        connection.close()
        return

    cursor.execute("""
        INSERT INTO students
        (name, roll_no, branch, cgpa, email)
        VALUES (?, ?, ?, ?, ?)
    """, (name, roll_no, branch, cgpa, email))

    connection.commit()
    connection.close()

    print("\nStudent added successfully!")


def view_students():
    print("\n===== STUDENT LIST =====")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, roll_no, branch, cgpa, email
        FROM students
        ORDER BY id
    """)

    students = cursor.fetchall()

    if not students:
        print("No students found.")
    else:
        print("-" * 90)
        print("{:<5} {:<20} {:<15} {:<15} {:<8} {:<25}".format(
            "ID", "Name", "Roll No", "Branch", "CGPA", "Email"
        ))
        print("-" * 90)

        for student in students:
            print("{:<5} {:<20} {:<15} {:<15} {:<8} {:<25}".format(
                student[0],
                student[1],
                student[2],
                student[3],
                student[4],
                student[5]
            ))

        print("-" * 90)

    connection.close()


def search_student():
    print("\n===== SEARCH STUDENT =====")

    roll_no = input("Enter roll number: ")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, roll_no, branch, cgpa, email
        FROM students
        WHERE roll_no = ?
    """, (roll_no,))

    student = cursor.fetchone()

    if student is None:
        print("\nStudent not found.")
    else:
        print("\n===== STUDENT FOUND =====")
        print("ID      :", student[0])
        print("Name    :", student[1])
        print("Roll No :", student[2])
        print("Branch  :", student[3])
        print("CGPA    :", student[4])
        print("Email   :", student[5])

    connection.close()


def update_student():
    print("\n===== UPDATE STUDENT =====")

    student_id = get_integer("Enter student ID: ")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    )

    student = cursor.fetchone()

    if student is None:
        print("\nStudent not found.")
        connection.close()
        return

    print("\nCurrent Details")
    print("Name    :", student[1])
    print("Roll No :", student[2])
    print("Branch  :", student[3])
    print("CGPA    :", student[4])
    print("Email   :", student[5])

    name = input("\nEnter new name: ")
    branch = input("Enter new branch: ")
    cgpa = get_cgpa("Enter new CGPA: ")
    email = input("Enter new email: ")

    cursor.execute("""
        UPDATE students
        SET name = ?, branch = ?, cgpa = ?, email = ?
        WHERE id = ?
    """, (name, branch, cgpa, email, student_id))

    connection.commit()
    connection.close()

    print("\nStudent updated successfully!")


def delete_student():
    print("\n===== DELETE STUDENT =====")

    student_id = get_integer("Enter student ID: ")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    )

    student = cursor.fetchone()

    if student is None:
        print("\nStudent not found.")
        connection.close()
        return

    print("\nStudent found:")
    print("Name    :", student[1])
    print("Roll No :", student[2])

    confirm = input(
        "\nAre you sure you want to delete this student? (yes/no): "
    )

    if confirm.lower() == "yes":

        cursor.execute(
            "DELETE FROM applications WHERE student_id = ?",
            (student_id,)
        )

        cursor.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,)
        )

        connection.commit()

        print("\nStudent deleted successfully!")

    else:
        print("\nDeletion cancelled.")

    connection.close()


# =========================================================
# COMPANY FUNCTIONS
# =========================================================

def add_company():
    print("\n===== ADD COMPANY =====")

    company_name = input("Enter company name: ")
    job_role = input("Enter job role: ")
    min_cgpa = get_cgpa("Enter minimum CGPA: ")
    package = input("Enter package (LPA): ")
    location = input("Enter location: ")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id
        FROM companies
        WHERE company_name = ? AND job_role = ?
    """, (company_name, job_role))

    if cursor.fetchone() is not None:
        print("\nThis company and job role already exists.")
        connection.close()
        return

    cursor.execute("""
        INSERT INTO companies
        (company_name, job_role, min_cgpa, package, location)
        VALUES (?, ?, ?, ?, ?)
    """, (
        company_name,
        job_role,
        min_cgpa,
        package,
        location
    ))

    connection.commit()
    connection.close()

    print("\nCompany added successfully!")


def view_companies():
    print("\n===== COMPANY LIST =====")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, company_name, job_role,
               min_cgpa, package, location
        FROM companies
        ORDER BY id
    """)

    companies = cursor.fetchall()

    if not companies:
        print("No companies found.")
    else:
        print("-" * 100)
        print("{:<5} {:<20} {:<20} {:<10} {:<12} {:<20}".format(
            "ID",
            "Company",
            "Job Role",
            "Min CGPA",
            "Package",
            "Location"
        ))
        print("-" * 100)

        for company in companies:
            print("{:<5} {:<20} {:<20} {:<10} {:<12} {:<20}".format(
                company[0],
                company[1],
                company[2],
                company[3],
                company[4],
                company[5]
            ))

        print("-" * 100)

    connection.close()


def update_company():
    print("\n===== UPDATE COMPANY =====")

    company_id = get_integer("Enter company ID: ")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM companies WHERE id = ?",
        (company_id,)
    )

    company = cursor.fetchone()

    if company is None:
        print("\nCompany not found.")
        connection.close()
        return

    print("\nCurrent Details:")
    print("Company Name :", company[1])
    print("Job Role     :", company[2])
    print("Minimum CGPA :", company[3])
    print("Package      :", company[4])
    print("Location     :", company[5])

    job_role = input("\nEnter new job role: ")
    min_cgpa = get_cgpa("Enter new minimum CGPA: ")
    package = input("Enter new package (LPA): ")
    location = input("Enter new location: ")

    cursor.execute("""
        UPDATE companies
        SET job_role = ?,
            min_cgpa = ?,
            package = ?,
            location = ?
        WHERE id = ?
    """, (
        job_role,
        min_cgpa,
        package,
        location,
        company_id
    ))

    connection.commit()
    connection.close()

    print("\nCompany updated successfully!")


def delete_company():
    print("\n===== DELETE COMPANY =====")

    company_id = get_integer("Enter company ID: ")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM companies WHERE id = ?",
        (company_id,)
    )

    company = cursor.fetchone()

    if company is None:
        print("\nCompany not found.")
        connection.close()
        return

    print("\nCompany found:")
    print("Company :", company[1])
    print("Job Role:", company[2])
    print("Package :", company[4])
    print("Location:", company[5])

    cursor.execute("""
        SELECT COUNT(*)
        FROM applications
        WHERE company_id = ?
    """, (company_id,))

    application_count = cursor.fetchone()[0]

    if application_count > 0:
        print(
            "\nThis company has",
            application_count,
            "existing application(s)."
        )
        print("Company cannot be deleted while applications exist.")

        connection.close()
        return

    confirm = input(
        "\nAre you sure you want to delete this company? (yes/no): "
    )

    if confirm.lower() == "yes":

        cursor.execute(
            "DELETE FROM companies WHERE id = ?",
            (company_id,)
        )

        connection.commit()

        print("\nCompany deleted successfully!")

    else:
        print("\nDeletion cancelled.")

    connection.close()


# =========================================================
# APPLICATION FUNCTIONS
# =========================================================

def apply_for_placement():
    print("\n===== APPLY FOR PLACEMENT =====")

    student_id = get_integer("Enter student ID: ")
    company_id = get_integer("Enter company ID: ")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT name, cgpa
        FROM students
        WHERE id = ?
    """, (student_id,))

    student = cursor.fetchone()

    if student is None:
        print("\nStudent not found.")
        connection.close()
        return

    cursor.execute("""
        SELECT company_name, job_role, min_cgpa
        FROM companies
        WHERE id = ?
    """, (company_id,))

    company = cursor.fetchone()

    if company is None:
        print("\nCompany not found.")
        connection.close()
        return

    student_name = student[0]
    student_cgpa = student[1]

    company_name = company[0]
    job_role = company[1]
    minimum_cgpa = company[2]

    print("\nStudent :", student_name)
    print("CGPA    :", student_cgpa)

    print("\nCompany :", company_name)
    print("Job Role:", job_role)
    print("Minimum CGPA:", minimum_cgpa)

    if student_cgpa < minimum_cgpa:
        print("\nNOT ELIGIBLE for this company.")
        connection.close()
        return

    cursor.execute("""
        SELECT id
        FROM applications
        WHERE student_id = ?
        AND company_id = ?
    """, (student_id, company_id))

    if cursor.fetchone() is not None:
        print("\nYou have already applied to this company.")
        connection.close()
        return

    cursor.execute("""
        INSERT INTO applications
        (student_id, company_id, status)
        VALUES (?, ?, ?)
    """, (
        student_id,
        company_id,
        "Applied"
    ))

    connection.commit()
    connection.close()

    print("\nEligible!")
    print("Application submitted successfully!")


def view_applications():
    print("\n===== PLACEMENT APPLICATIONS =====")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            applications.id,
            students.name,
            students.roll_no,
            companies.company_name,
            companies.job_role,
            applications.status
        FROM applications
        JOIN students
            ON applications.student_id = students.id
        JOIN companies
            ON applications.company_id = companies.id
        ORDER BY applications.id
    """)

    applications = cursor.fetchall()

    if not applications:
        print("No applications found.")
    else:

        print("-" * 100)
        print("{:<5} {:<20} {:<15} {:<20} {:<20} {:<15}".format(
            "ID",
            "Student",
            "Roll No",
            "Company",
            "Job Role",
            "Status"
        ))
        print("-" * 100)

        for application in applications:
            print("{:<5} {:<20} {:<15} {:<20} {:<20} {:<15}".format(
                application[0],
                application[1],
                application[2],
                application[3],
                application[4],
                application[5]
            ))

        print("-" * 100)

    connection.close()


def update_application_status():
    print("\n===== UPDATE APPLICATION STATUS =====")

    application_id = get_integer("Enter application ID: ")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id
        FROM applications
        WHERE id = ?
    """, (application_id,))

    if cursor.fetchone() is None:
        print("\nApplication not found.")
        connection.close()
        return

    print("\n1. Applied")
    print("2. Shortlisted")
    print("3. Selected")
    print("4. Rejected")

    choice = input("Enter new status: ")

    if choice == "1":
        status = "Applied"
    elif choice == "2":
        status = "Shortlisted"
    elif choice == "3":
        status = "Selected"
    elif choice == "4":
        status = "Rejected"
    else:
        print("\nInvalid choice.")
        connection.close()
        return

    cursor.execute("""
        UPDATE applications
        SET status = ?
        WHERE id = ?
    """, (status, application_id))

    connection.commit()
    connection.close()

    print("\nApplication status updated successfully!")


def delete_application():
    print("\n===== DELETE APPLICATION =====")

    application_id = get_integer("Enter application ID: ")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            applications.id,
            students.name,
            companies.company_name,
            applications.status
        FROM applications
        JOIN students
            ON applications.student_id = students.id
        JOIN companies
            ON applications.company_id = companies.id
        WHERE applications.id = ?
    """, (application_id,))

    application = cursor.fetchone()

    if application is None:
        print("\nApplication not found.")
        connection.close()
        return

    print("\nApplication found:")
    print("ID     :", application[0])
    print("Student:", application[1])
    print("Company:", application[2])
    print("Status :", application[3])

    confirm = input(
        "\nAre you sure you want to delete this application? (yes/no): "
    )

    if confirm.lower() == "yes":

        cursor.execute("""
            DELETE FROM applications
            WHERE id = ?
        """, (application_id,))

        connection.commit()

        print("\nApplication deleted successfully!")

    else:
        print("\nDeletion cancelled.")

    connection.close()


# =========================================================
# SEARCH & FILTER
# =========================================================

def search_filter_applications():
    print("\n===== SEARCH & FILTER APPLICATIONS =====")

    print("1. Search by Student")
    print("2. Search by Company")
    print("3. Filter by Status")

    choice = input("Enter your choice: ")

    connection = get_connection()
    cursor = connection.cursor()

    if choice == "1":

        name = input("Enter student name: ")

        cursor.execute("""
            SELECT
                applications.id,
                students.name,
                companies.company_name,
                companies.job_role,
                applications.status
            FROM applications
            JOIN students
                ON applications.student_id = students.id
            JOIN companies
                ON applications.company_id = companies.id
            WHERE students.name LIKE ?
        """, ('%' + name + '%',))

    elif choice == "2":

        company_name = input("Enter company name: ")

        cursor.execute("""
            SELECT
                applications.id,
                students.name,
                companies.company_name,
                companies.job_role,
                applications.status
            FROM applications
            JOIN students
                ON applications.student_id = students.id
            JOIN companies
                ON applications.company_id = companies.id
            WHERE companies.company_name LIKE ?
        """, ('%' + company_name + '%',))

    elif choice == "3":

        print("\n1. Applied")
        print("2. Shortlisted")
        print("3. Selected")
        print("4. Rejected")

        status_choice = input("Enter status: ")

        statuses = {
            "1": "Applied",
            "2": "Shortlisted",
            "3": "Selected",
            "4": "Rejected"
        }

        if status_choice not in statuses:
            print("\nInvalid status.")
            connection.close()
            return

        status = statuses[status_choice]

        cursor.execute("""
            SELECT
                applications.id,
                students.name,
                companies.company_name,
                companies.job_role,
                applications.status
            FROM applications
            JOIN students
                ON applications.student_id = students.id
            JOIN companies
                ON applications.company_id = companies.id
            WHERE applications.status = ?
        """, (status,))

    else:
        print("\nInvalid choice.")
        connection.close()
        return

    applications = cursor.fetchall()

    if not applications:
        print("\nNo applications found.")
    else:

        print("\nID | Student | Company | Job Role | Status")
        print("-" * 80)

        for application in applications:
            print(application)

    connection.close()


# =========================================================
# PLACEMENT DASHBOARD
# =========================================================

def placement_dashboard():
    print("\n===== PLACEMENT DASHBOARD =====")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM companies")
    companies = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM applications")
    applications = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM applications
        WHERE status = 'Applied'
    """)
    applied = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM applications
        WHERE status = 'Shortlisted'
    """)
    shortlisted = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM applications
        WHERE status = 'Selected'
    """)
    selected = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM applications
        WHERE status = 'Rejected'
    """)
    rejected = cursor.fetchone()[0]

    if students > 0:
        percentage = selected / students * 100
    else:
        percentage = 0

    print("\n-----------------------------")
    print("Total Students     :", students)
    print("Total Companies    :", companies)
    print("Total Applications :", applications)
    print("-----------------------------")
    print("Applied            :", applied)
    print("Shortlisted        :", shortlisted)
    print("Selected           :", selected)
    print("Rejected           :", rejected)
    print("-----------------------------")
    print("Placement Rate     : {:.2f}%".format(percentage))
    print("-----------------------------")

    connection.close()


# =========================================================
# STUDENT ELIGIBILITY
# =========================================================

def check_student_eligibility():
    print("\n===== CHECK STUDENT ELIGIBILITY =====")

    student_id = get_integer("Enter student ID: ")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT name, cgpa
        FROM students
        WHERE id = ?
    """, (student_id,))

    student = cursor.fetchone()

    if student is None:
        print("\nStudent not found.")
        connection.close()
        return

    print("\nStudent Name:", student[0])
    print("Student CGPA:", student[1])

    cursor.execute("""
        SELECT company_name,
               job_role,
               min_cgpa,
               package,
               location
        FROM companies
        WHERE min_cgpa <= ?
        ORDER BY min_cgpa
    """, (student[1],))

    companies = cursor.fetchall()

    print("\n===== ELIGIBLE COMPANIES =====")

    if not companies:
        print("No eligible companies found.")
    else:
        for company in companies:
            print("\nCompany       :", company[0])
            print("Job Role      :", company[1])
            print("Minimum CGPA  :", company[2])
            print("Package       :", company[3], "LPA")
            print("Location      :", company[4])

    connection.close()


# =========================================================
# COMPANY PLACEMENT REPORT
# =========================================================

def company_placement_report():
    print("\n===== COMPANY PLACEMENT REPORT =====")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            companies.company_name,
            COUNT(applications.id),
            SUM(
                CASE
                    WHEN applications.status = 'Selected'
                    THEN 1
                    ELSE 0
                END
            )
        FROM companies
        LEFT JOIN applications
            ON companies.id = applications.company_id
        GROUP BY companies.id
        ORDER BY companies.company_name
    """)

    data = cursor.fetchall()

    if not data:
        print("\nNo companies found.")
    else:

        print("\nCompany                  Applications     Selected")
        print("-" * 60)

        for row in data:
            selected = row[2]

            if selected is None:
                selected = 0

            print("{:<25} {:<17} {}".format(
                row[0],
                row[1],
                selected
            ))

    connection.close()


# =========================================================
# HIGHEST PACKAGE
# =========================================================

def highest_package_report():
    print("\n===== HIGHEST PACKAGE REPORT =====")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT company_name,
               job_role,
               package,
               location
        FROM companies
    """)

    companies = cursor.fetchall()

    highest = None

    for company in companies:

        try:
            package = float(
                str(company[2])
                .replace("LPA", "")
                .replace("lpa", "")
                .strip()
            )
        except ValueError:
            continue

        if highest is None or package > highest[0]:
            highest = (
                package,
                company[0],
                company[1],
                company[3]
            )

    if highest is None:
        print("\nNo valid package found.")
    else:
        print("\nHighest Package:", highest[0], "LPA")
        print("Company :", highest[1])
        print("Job Role:", highest[2])
        print("Location:", highest[3])

    connection.close()


# =========================================================
# STUDENT PLACEMENT HISTORY
# =========================================================

def student_placement_history():
    print("\n===== STUDENT PLACEMENT HISTORY =====")

    student_id = get_integer("Enter student ID: ")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT name, roll_no, branch, cgpa
        FROM students
        WHERE id = ?
    """, (student_id,))

    student = cursor.fetchone()

    if student is None:
        print("\nStudent not found.")
        connection.close()
        return

    print("\nName    :", student[0])
    print("Roll No :", student[1])
    print("Branch  :", student[2])
    print("CGPA    :", student[3])

    cursor.execute("""
        SELECT
            companies.company_name,
            companies.job_role,
            companies.package,
            companies.location,
            applications.status
        FROM applications
        JOIN companies
            ON applications.company_id = companies.id
        WHERE applications.student_id = ?
    """, (student_id,))

    applications = cursor.fetchall()

    if not applications:
        print("\nNo applications found.")
    else:

        print("\n===== APPLICATION HISTORY =====")

        for application in applications:
            print("\nCompany :", application[0])
            print("Job Role:", application[1])
            print("Package :", application[2], "LPA")
            print("Location:", application[3])
            print("Status  :", application[4])

    connection.close()


# =========================================================
# STUDENT PLACEMENT STATUS
# =========================================================

def student_placement_status():
    print("\n===== STUDENT PLACEMENT STATUS =====")

    student_id = get_integer("Enter student ID: ")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT name, roll_no, branch, cgpa
        FROM students
        WHERE id = ?
    """, (student_id,))

    student = cursor.fetchone()

    if student is None:
        print("\nStudent not found.")
        connection.close()
        return

    print("\nName    :", student[0])
    print("Roll No :", student[1])
    print("Branch  :", student[2])
    print("CGPA    :", student[3])

    cursor.execute("""
        SELECT
            companies.company_name,
            companies.job_role,
            companies.package,
            applications.status
        FROM applications
        JOIN companies
            ON applications.company_id = companies.id
        WHERE applications.student_id = ?
    """, (student_id,))

    applications = cursor.fetchall()

    if not applications:
        print("\nPlacement Status: NOT APPLIED")
        connection.close()
        return

    selected = 0
    shortlisted = 0
    applied = 0
    rejected = 0

    for application in applications:

        if application[3] == "Selected":
            selected += 1

        elif application[3] == "Shortlisted":
            shortlisted += 1

        elif application[3] == "Applied":
            applied += 1

        elif application[3] == "Rejected":
            rejected += 1

    if selected > 0:
        print("\nPlacement Status: SELECTED")
    elif shortlisted > 0:
        print("\nPlacement Status: SHORTLISTED")
    elif applied > 0:
        print("\nPlacement Status: APPLICATIONS IN PROGRESS")
    else:
        print("\nPlacement Status: REJECTED")

    print("\n===== APPLICATION SUMMARY =====")
    print("Total Applications :", len(applications))
    print("Selected           :", selected)
    print("Shortlisted        :", shortlisted)
    print("Applied            :", applied)
    print("Rejected           :", rejected)

    connection.close()


# =========================================================
# PLACEMENT STATISTICS
# =========================================================

def placement_statistics():
    print("\n===== PLACEMENT STATISTICS =====")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM companies")
    total_companies = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM applications")
    total_applications = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM applications
        WHERE status = 'Applied'
    """)
    applied = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM applications
        WHERE status = 'Shortlisted'
    """)
    shortlisted = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM applications
        WHERE status = 'Selected'
    """)
    selected = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM applications
        WHERE status = 'Rejected'
    """)
    rejected = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(cgpa) FROM students")
    average_cgpa = cursor.fetchone()[0]

    cursor.execute("SELECT MAX(cgpa) FROM students")
    highest_cgpa = cursor.fetchone()[0]

    cursor.execute("SELECT MIN(cgpa) FROM students")
    lowest_cgpa = cursor.fetchone()[0]

    if total_students > 0:
        placement_rate = selected / total_students * 100
    else:
        placement_rate = 0

    print("\n====================================")
    print("       PLACEMENT STATISTICS")
    print("====================================")

    print("\nStudents       :", total_students)
    print("Companies      :", total_companies)
    print("Applications   :", total_applications)

    print("\nApplied        :", applied)
    print("Shortlisted    :", shortlisted)
    print("Selected       :", selected)
    print("Rejected       :", rejected)

    if average_cgpa is not None:
        print("\nAverage CGPA   :", round(average_cgpa, 2))
        print("Highest CGPA   :", highest_cgpa)
        print("Lowest CGPA    :", lowest_cgpa)
    else:
        print("\nNo CGPA data available.")

    print("\nPlacement Rate : {:.2f}%".format(placement_rate))

    print("====================================")

    connection.close()


# =========================================================
# TOP PLACEMENT STUDENTS
# =========================================================

def top_placement_students():
    print("\n===== TOP PLACEMENT STUDENTS =====")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            students.name,
            students.roll_no,
            students.branch,
            students.cgpa,
            companies.company_name,
            companies.job_role,
            companies.package,
            companies.location
        FROM applications
        JOIN students
            ON applications.student_id = students.id
        JOIN companies
            ON applications.company_id = companies.id
        WHERE applications.status = 'Selected'
    """)

    students = cursor.fetchall()

    if not students:
        print("\nNo selected students found.")
        connection.close()
        return

    data = []

    for student in students:

        try:
            package = float(
                str(student[6])
                .replace("LPA", "")
                .replace("lpa", "")
                .strip()
            )
        except ValueError:
            package = 0

        data.append((package, student))

    data.sort(
        key=lambda x: x[0],
        reverse=True
    )

    rank = 1

    for package, student in data:

        print("\n----------------------------------------")
        print("Rank     :", rank)
        print("Name     :", student[0])
        print("Roll No  :", student[1])
        print("Branch   :", student[2])
        print("CGPA     :", student[3])
        print("Company  :", student[4])
        print("Job Role :", student[5])
        print("Package  :", student[6], "LPA")
        print("Location :", student[7])

        rank += 1

    print("----------------------------------------")

    connection.close()


# =========================================================
# MAIN MENU
# =========================================================

while True:

    print("\n")
    print("=" * 55)
    print("     STUDENT PLACEMENT MANAGEMENT SYSTEM")
    print("=" * 55)

    print("\n----- STUDENT MANAGEMENT -----")
    print("1.  Add Student")
    print("2.  View Students")
    print("3.  Search Student")
    print("4.  Update Student")
    print("5.  Delete Student")

    print("\n----- COMPANY MANAGEMENT -----")
    print("6.  Add Company")
    print("7.  View Companies")
    print("8.  Update Company")
    print("9.  Delete Company")

    print("\n----- PLACEMENT MANAGEMENT -----")
    print("10. Apply for Placement")
    print("11. View Applications")
    print("12. Update Application Status")
    print("13. Delete Application")
    print("14. Search & Filter Applications")

    print("\n----- REPORTS & ANALYSIS -----")
    print("15. Placement Dashboard")
    print("16. Check Student Eligibility")
    print("17. Company Placement Report")
    print("18. Highest Package Report")
    print("19. Student Placement History")
    print("20. Student Placement Status")
    print("21. Placement Statistics")
    print("22. Top Placement Students")

    print("\n23. Exit")

    print("=" * 55)

    choice = input("Enter your choice: ")

    if choice == "1":
        add_student()

    elif choice == "2":
        view_students()

    elif choice == "3":
        search_student()

    elif choice == "4":
        update_student()

    elif choice == "5":
        delete_student()

    elif choice == "6":
        add_company()

    elif choice == "7":
        view_companies()

    elif choice == "8":
        update_company()

    elif choice == "9":
        delete_company()

    elif choice == "10":
        apply_for_placement()

    elif choice == "11":
        view_applications()

    elif choice == "12":
        update_application_status()

    elif choice == "13":
        delete_application()

    elif choice == "14":
        search_filter_applications()

    elif choice == "15":
        placement_dashboard()

    elif choice == "16":
        check_student_eligibility()

    elif choice == "17":
        company_placement_report()

    elif choice == "18":
        highest_package_report()

    elif choice == "19":
        student_placement_history()

    elif choice == "20":
        student_placement_status()

    elif choice == "21":
        placement_statistics()

    elif choice == "22":
        top_placement_students()

    elif choice == "23":
        print("\nThank you for using Student Placement Management System!")
        break

    else:
        print("\nInvalid choice. Please enter a number from 1 to 23.")