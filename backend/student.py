from database.db_connection import get_db_connection
from backend.student_management import store_student_warning,create_notification
def get_student_profile(student_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT StudentDetails.*, Departments.DepartmentName
    FROM StudentDetails
    JOIN Departments ON StudentDetails.DepartmentID = Departments.DepartmentID
    WHERE StudentDetails.StudentID = %s
    """
    cursor.execute(query, (student_id,))
    profile = cursor.fetchone()
    cursor.close()
    connection.close()
    return profile

def get_courses_for_student(student_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT Courses.SubjectCode, Courses.CourseTitle, Courses.CreditHours, TeacherDetails.FirstName AS TeacherName, StudentRegistrations.Semester
    FROM StudentRegistrations
    JOIN Courses ON StudentRegistrations.CourseID = Courses.CourseID
    LEFT JOIN TeacherCourseAllocation ON Courses.CourseID = TeacherCourseAllocation.CourseID
    LEFT JOIN TeacherDetails ON TeacherCourseAllocation.TeacherID = TeacherDetails.TeacherID
    WHERE StudentRegistrations.StudentID = %s
    """
    cursor.execute(query, (student_id,))
    courses = cursor.fetchall()
    cursor.close()
    connection.close()
    return courses

def get_gpa(student_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT Courses.SubjectCode AS CourseCode, Courses.CourseTitle, Courses.CreditHours, Grades.Grade, 
           CASE 
               WHEN Grades.Grade = 'A+' THEN 4.0
               WHEN Grades.Grade = 'A' THEN 4.0
               WHEN Grades.Grade = 'B+' THEN 3.5
               WHEN Grades.Grade = 'B' THEN 3.0
               WHEN Grades.Grade = 'C+' THEN 2.5
               WHEN Grades.Grade = 'C' THEN 2.0
               WHEN Grades.Grade = 'D+' THEN 1.5
               WHEN Grades.Grade = 'D' THEN 1.0
               WHEN Grades.Grade = 'F' THEN 0.0
           END AS GradePoints,
           CASE 
               WHEN Grades.Grade = 'A+' THEN 4.0 * Courses.CreditHours
               WHEN Grades.Grade = 'A' THEN 4.0 * Courses.CreditHours
               WHEN Grades.Grade = 'B+' THEN 3.5 * Courses.CreditHours
               WHEN Grades.Grade = 'B' THEN 3.0 * Courses.CreditHours
               WHEN Grades.Grade = 'C+' THEN 2.5 * Courses.CreditHours
               WHEN Grades.Grade = 'C' THEN 2.0 * Courses.CreditHours
               WHEN Grades.Grade = 'D+' THEN 1.5 * Courses.CreditHours
               WHEN Grades.Grade = 'D' THEN 1.0 * Courses.CreditHours
               WHEN Grades.Grade = 'F' THEN 0.0 * Courses.CreditHours
           END AS Product
    FROM Grades
    JOIN Courses ON Grades.CourseID = Courses.CourseID
    WHERE Grades.StudentID = %s
    """
    cursor.execute(query, (student_id,))
    gpa_data = cursor.fetchall()
    cursor.close()
    connection.close()
    return gpa_data


def get_confirmed_courses(user_id, semester):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT Courses.SubjectCode, Courses.CourseTitle, Courses.CreditHours, TeacherDetails.FirstName AS TeacherName, ConfirmedCourses.CourseID
    FROM ConfirmedCourses
    JOIN Courses ON ConfirmedCourses.CourseID = Courses.CourseID
    LEFT JOIN TeacherCourseAllocation ON Courses.CourseID = TeacherCourseAllocation.CourseID
    LEFT JOIN TeacherDetails ON TeacherCourseAllocation.TeacherID = TeacherDetails.TeacherID
    WHERE ConfirmedCourses.Semester = %s AND ConfirmedCourses.Confirmed = TRUE
    """
    cursor.execute(query, (semester,))
    courses = cursor.fetchall()
    cursor.close()
    connection.close()
    return courses

def is_course_already_registered(student_id, course_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = """
    SELECT COUNT(*) FROM StudentRegistrations WHERE StudentID = %s AND CourseID = %s
    """
    cursor.execute(query, (student_id, course_id))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result[0] > 0

def register_courses(student_id, course_ids):
    connection = get_db_connection()
    cursor = connection.cursor()
    for course_id in course_ids:
        if not is_course_already_registered(student_id, course_id):
            query = """
            INSERT INTO StudentRegistrations (StudentID, CourseID, DepartmentID, Semester)
            SELECT %s, CourseID, DepartmentID, Semester FROM ConfirmedCourses WHERE CourseID = %s
            """
            cursor.execute(query, (student_id, course_id))
    connection.commit()
    cursor.close()
    connection.close()

def check_student_passed_courses(student_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT COUNT(*) AS UnpassedCourses
    FROM Grades
    JOIN CourseRoadmap ON Grades.CourseID = CourseRoadmap.CourseID
    WHERE Grades.StudentID = %s AND Grades.Grade = 'F'
    """
    cursor.execute(query, (student_id,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result['UnpassedCourses'] == 0

def get_student_transcript_data(student_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT Courses.SubjectCode AS CourseCode, Courses.CourseTitle, Courses.CreditHours, Grades.Grade
    FROM Grades
    JOIN Courses ON Grades.CourseID = Courses.CourseID
    WHERE Grades.StudentID = %s
    """
    cursor.execute(query, (student_id,))
    transcript_data = cursor.fetchall()
    cursor.close()
    connection.close()
    return transcript_data


# Update existing methods to include notification creation
def notify_students_of_confirmed_courses(department_id, semester):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = """
    SELECT StudentID FROM StudentDetails WHERE DepartmentID = %s AND CurrentSemesterNumber = %s
    """
    cursor.execute(query, (department_id, semester))
    students = cursor.fetchall()
    for student in students:
        create_notification(student['StudentID'], "New courses have been confirmed for your semester. Please register for them.")
    cursor.close()
    connection.close()

def get_notifications(student_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    notifications = []
    try:
        # Start a transaction
        cursor.execute("START TRANSACTION")

        # Fetch notifications
        query = "SELECT NotificationID, Message, Timestamp FROM Notifications WHERE StudentID = %s"
        cursor.execute(query, (student_id,))
        notifications = cursor.fetchall()

        # Delete fetched notifications
        if notifications:
            notification_ids = [notification['NotificationID'] for notification in notifications]
            delete_query = "DELETE FROM Notifications WHERE NotificationID IN (%s)" % ','.join(['%s'] * len(notification_ids))
            cursor.execute(delete_query, notification_ids)

        # Commit transaction
        connection.commit()
    except get_db_connection.connector.Error as err:
        connection.rollback()
        raise err
    finally:
        cursor.close()
        connection.close()
    
    return notifications