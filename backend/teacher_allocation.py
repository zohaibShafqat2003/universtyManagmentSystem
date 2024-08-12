import mysql.connector
from database.db_connection import get_db_connection

def fetch_departments():
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "SELECT DepartmentID, DepartmentName FROM Departments"
    cursor.execute(query)
    departments = cursor.fetchall()
    cursor.close()
    connection.close()
    return departments

def fetch_teachers(department_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "SELECT TeacherID, firstName FROM TeacherDetails WHERE DepartmentID = %s"
    cursor.execute(query, (department_id,))
    teachers = cursor.fetchall()
    cursor.close()
    connection.close()
    return teachers

def fetch_courses_by_department(department_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = """
    SELECT c.CourseID, c.CourseTitle
    FROM Courses c
    JOIN CourseRoadmap cr ON c.CourseID = cr.CourseID
    WHERE cr.DepartmentID = %s
    """
    cursor.execute(query, (department_id,))
    courses = cursor.fetchall()
    cursor.close()
    connection.close()
    return courses

def allocate_course_to_teacher(teacher_id, course_id, department_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        # Check if the course is already allocated
        cursor.execute("""
        SELECT TeacherID FROM TeacherCourseAllocation 
        WHERE CourseID = %s AND DepartmentID = %s
        """, (course_id, department_id))
        result = cursor.fetchone()
        if result:
            raise Exception(f"Course {course_id} is already allocated to teacher {result[0]}")
        
        # Allocate the course to the teacher
        cursor.execute("""
        INSERT INTO TeacherCourseAllocation (TeacherID, CourseID, DepartmentID)
        VALUES (%s, %s, %s)
        """, (teacher_id, course_id, department_id))
        connection.commit()
    except mysql.connector.Error as err:
        connection.rollback()
        raise err
    finally:
        cursor.close()
        connection.close()

def get_teacher_allocated_credit_hours(teacher_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = """
    SELECT SUM(c.CreditHours)
    FROM TeacherCourseAllocation tca
    JOIN Courses c ON tca.CourseID = c.CourseID
    WHERE tca.TeacherID = %s
    """
    cursor.execute(query, (teacher_id,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result[0] if result[0] else 0

def get_teacher_allocated_courses(teacher_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = """
    SELECT COUNT(*)
    FROM TeacherCourseAllocation
    WHERE TeacherID = %s
    """
    cursor.execute(query, (teacher_id,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result[0] if result[0] else 0

def get_course_credit_hours(course_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "SELECT CreditHours FROM Courses WHERE CourseID = %s"
    cursor.execute(query, (course_id,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result[0] if result else 0
