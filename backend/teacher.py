from database.db_connection import get_db_connection

def get_teachers():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT TeacherID, CONCAT(FirstName, ' ', LastName) AS Name FROM TeacherDetails")
    teachers = cursor.fetchall()
    cursor.close()
    connection.close()
    return teachers

def get_teacher_profile(teacher_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT FirstName, LastName, Institute, Departments.DepartmentName, MobileNo, Email 
    FROM TeacherDetails 
    JOIN Departments ON TeacherDetails.DepartmentID = Departments.DepartmentID 
    WHERE TeacherID = %s
    """
    cursor.execute(query, (teacher_id,))
    profile = cursor.fetchone()
    cursor.close()
    connection.close()
    return profile

def get_courses(teacher_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT Courses.SubjectCode, Courses.CourseTitle, Courses.CreditHours, TeacherCourseAllocation.DepartmentID, Courses.CourseID
    FROM Courses
    JOIN TeacherCourseAllocation ON Courses.CourseID = TeacherCourseAllocation.CourseID
    WHERE TeacherCourseAllocation.TeacherID = %s
    """
    cursor.execute(query, (teacher_id,))
    courses = cursor.fetchall()
    cursor.close()
    connection.close()
    return courses

def get_students_in_course(course_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT StudentDetails.StudentID, StudentDetails.Name
    FROM StudentDetails
    JOIN StudentRegistrations ON StudentDetails.StudentID = StudentRegistrations.StudentID
    WHERE StudentRegistrations.CourseID = %s
    """
    cursor.execute(query, (course_id,))
    students = cursor.fetchall()
    cursor.close()
    connection.close()
    return students

def mark_student_grade(student_id, course_id, teacher_id, grade):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Check if the grade already exists
        check_query = """
        SELECT Grade FROM Grades
        WHERE StudentID = %s AND CourseID = %s
        """
        cursor.execute(check_query, (student_id, course_id))
        existing_grade = cursor.fetchone()

        if existing_grade:
            cursor.close()
            connection.close()
            return False, "Grade already exists for this student and course."

        # Insert the new grade
        insert_query = """
        INSERT INTO Grades (StudentID, CourseID, TeacherID, Grade)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, (student_id, course_id, teacher_id, grade))
        connection.commit()
        cursor.close()
        connection.close()
        return True, "Grade submitted successfully."
    except Exception as e:
        print(f"Error: {e}")
        return False, str(e)

