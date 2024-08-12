import mysql.connector
from database.db_connection import get_db_connection

def fetch_unregistered_students(department_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = """
    SELECT s.Enrollment, s.Name, s.CurrentSemesterNumber
    FROM StudentDetails s
    LEFT JOIN StudentRegistrations sr ON s.StudentID = sr.StudentID
    WHERE sr.StudentID IS NULL AND s.DepartmentID = %s
    """
    cursor.execute(query, (department_id,))
    students = cursor.fetchall()
    cursor.close()
    connection.close()
    return students

def fetch_students_by_gpa_range(department_id, gpa_range):
    connection = get_db_connection()
    cursor = connection.cursor()

    gpa_condition = ""
    if gpa_range == ">3":
        gpa_condition = "HAVING GPA > 3.0"
    elif gpa_range == "2-3":
        gpa_condition = "HAVING GPA BETWEEN 2.0 AND 3.0"
    elif gpa_range == "<2":
        gpa_condition = "HAVING GPA < 2.0"

    query = f"""
    SELECT 
        s.Enrollment,
        s.Name,
        s.CurrentSemesterNumber,
        AVG(CASE 
            WHEN g.Grade = 'A' THEN 4.0
            WHEN g.Grade = 'B' THEN 3.0
            WHEN g.Grade = 'C' THEN 2.0
            WHEN g.Grade = 'D' THEN 1.0
            WHEN g.Grade = 'F' THEN 0.0
            ELSE NULL
        END) AS GPA
    FROM 
        StudentDetails s
    JOIN 
        Grades g ON s.StudentID = g.StudentID
    WHERE 
        s.DepartmentID = %s
    GROUP BY 
        s.StudentID
    {gpa_condition};
    """

    cursor.execute(query, (department_id,))
    results = cursor.fetchall()
    cursor.close()
    connection.close()

    return [(row[0], row[1], row[2]) for row in results]

def fetch_students_by_department_and_semester(department_id, semester):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = """
    SELECT StudentID, Name 
    FROM StudentDetails 
    WHERE DepartmentID = %s AND CurrentSemesterNumber = %s
    """
    cursor.execute(query, (department_id, semester))
    students = cursor.fetchall()
    cursor.close()
    connection.close()
    return students

def create_notification(student_id, message):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = """
    INSERT INTO Notifications (StudentID, Message) VALUES (%s, %s)
    """
    cursor.execute(query, (student_id, message))
    connection.commit()
    cursor.close()
    connection.close()

def store_student_warning(student_id, department_id, semester, warning_text):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = """
    INSERT INTO Warnings (StudentID, DepartmentID, Semester, WarningText) 
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (student_id, department_id, semester, warning_text))
    connection.commit()
    create_notification(student_id, f"You have received a warning: {warning_text}")
    cursor.close()
    connection.close()

def fetch_semesters():
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "SELECT DISTINCT Semester FROM CourseRoadmap"
    cursor.execute(query)
    semesters = [row[0] for row in cursor.fetchall()]
    cursor.close()
    connection.close()
    return semesters
