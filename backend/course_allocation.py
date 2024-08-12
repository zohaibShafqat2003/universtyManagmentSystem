import mysql.connector
from database.db_connection import get_db_connection

def fetch_courses(department_id, semester):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = """
    SELECT c.CourseID, c.SubjectCode, c.CourseTitle, c.CreditHours
    FROM Courses c
    JOIN CourseRoadmap cr ON c.CourseID = cr.CourseID
    WHERE cr.DepartmentID = %s AND cr.Semester = %s
    """
    cursor.execute(query, (department_id, semester))
    courses = cursor.fetchall()
    cursor.close()
    connection.close()
    return courses

def populate_comboboxes(department_combobox, semester_combobox):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Populate Department ComboBox
    cursor.execute("SELECT DepartmentID, DepartmentName FROM Departments")
    departments = cursor.fetchall()
    department_combobox.clear()
    for department_id, department_name in departments:
        department_combobox.addItem(department_name, department_id)

    # Populate Semester ComboBox (example values)
    semesters = ["1", "2", "3", "4","5","6","7","8"]
    semester_combobox.clear()
    for semester in semesters:
        semester_combobox.addItem(semester)

    cursor.close()
    connection.close()


def update_confirmed_courses(confirmed_courses):
    connection = get_db_connection()
    cursor = connection.cursor()
    already_confirmed_courses = []
    try:
        for course_id, department_id, semester in confirmed_courses:
            cursor.execute("""
            SELECT Confirmed FROM ConfirmedCourses WHERE CourseID = %s AND DepartmentID = %s AND Semester = %s
            """, (course_id, department_id, semester))
            result = cursor.fetchone()
            if result and result[0]:
                already_confirmed_courses.append(course_id)
            else:
                cursor.execute("""
                INSERT INTO ConfirmedCourses (CourseID, DepartmentID, Semester, Confirmed)
                VALUES (%s, %s, %s, TRUE)
                """, (course_id, department_id, semester))
                notify_students(department_id, semester, course_id)
        connection.commit()
    except mysql.connector.Error as err:
        connection.rollback()
        print(f"Error: {err}")
        raise err
    finally:
        cursor.close()
        connection.close()
    return already_confirmed_courses

def notify_students(department_id, semester, course_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        # Fetch students of the specified department and semester
        cursor.execute("""
        SELECT StudentID FROM StudentDetails WHERE DepartmentID = %s AND CurrentSemesterNumber = %s
        """, (department_id, semester))
        students = cursor.fetchall()
        
        # Insert notification for each student
        for student in students:
            message = f"A new course (CourseID: {course_id}) has been confirmed for your semester. Please register for the course."
            cursor.execute("""
            INSERT INTO Notifications (StudentID, Message)
            VALUES (%s, %s)
            """, (student['StudentID'], message))
        connection.commit()
    except mysql.connector.Error as err:
        connection.rollback()
        print(f"Error while sending notifications: {err}")
        raise err
    finally:
        cursor.close()
        connection.close()