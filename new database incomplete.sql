CREATE DATABASE IF NOT EXISTS cms2;
USE cms2;

CREATE TABLE Login (
    LoginID INT AUTO_INCREMENT PRIMARY KEY,
    UserName VARCHAR(100) NOT NULL UNIQUE,
    Password VARCHAR(100) NOT NULL,
    Salt CHAR(32) NOT NULL,  -- Added for password security
    Role ENUM('Student', 'Teacher', 'Admin') NOT NULL
);

CREATE TABLE Departments (
    DepartmentID INT AUTO_INCREMENT PRIMARY KEY,
    DepartmentName VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE StudentDetails (
    StudentID INT PRIMARY KEY,
    Enrollment VARCHAR(100) NOT NULL UNIQUE,  -- Ensuring uniqueness for enrollment numbers
    Name VARCHAR(100) NOT NULL,
    DepartmentID INT,
    IntakeSemester VARCHAR(50),
    CurrentSemesterNumber INT,
    MobileNo VARCHAR(15),
    PersonalEmail VARCHAR(100),
    CurrentAddress VARCHAR(255),
    PermanentAddress VARCHAR(255),
    RegistrationNo VARCHAR(50) UNIQUE,
    FatherName VARCHAR(100),
    DegreeDuration VARCHAR(50),
    MaxSemester VARCHAR(50),
    PhoneNo VARCHAR(15),
    
    UniversityEmail VARCHAR(100) UNIQUE,  -- Ensuring uniqueness for university emails
    FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID),
    FOREIGN KEY (StudentID) REFERENCES Login(LoginID) ON DELETE CASCADE
);


CREATE TABLE TeacherDetails (
    TeacherID INT PRIMARY KEY,
    FirstName VARCHAR(100),
    LastName VARCHAR(100),
    Institute VARCHAR(100) NOT NULL,
    DepartmentID INT,
    MobileNo VARCHAR(15),
    Email VARCHAR(100) UNIQUE,  -- Ensuring uniqueness for email
    FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID),
    FOREIGN KEY (TeacherID) REFERENCES Login(LoginID) ON DELETE CASCADE
);

CREATE TABLE AdminDetails (
    AdminID INT PRIMARY KEY,
    DepartmentID INT,
    AdminName VARCHAR(255) NOT NULL,
    MobileNo VARCHAR(15),
    Email VARCHAR(100) NOT NULL UNIQUE,  -- Ensuring uniqueness for email
    FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID),
    FOREIGN KEY (AdminID) REFERENCES Login(LoginID) ON DELETE CASCADE
);



CREATE TABLE Courses (
    CourseID INT AUTO_INCREMENT PRIMARY KEY,
    SubjectCode VARCHAR(20) NOT NULL UNIQUE,  -- Ensuring uniqueness for subject codes
    CourseTitle VARCHAR(100) NOT NULL,
    CreditHours TINYINT NOT NULL  -- Changed to TINYINT for storage optimization
);



CREATE TABLE CourseRoadmap (
    RoadmapID INT AUTO_INCREMENT PRIMARY KEY,
    DepartmentID INT,
    Semester VARCHAR(20),
    CourseID INT,  -- Linking directly to Courses table
    FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID),
    FOREIGN KEY (CourseID) REFERENCES Courses(CourseID)
);

CREATE TABLE ConfirmedCourses (
    ConfirmationID INT AUTO_INCREMENT PRIMARY KEY,
    CourseID INT,
    Semester VARCHAR(20),
    DepartmentID INT,
    Confirmed BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (CourseID) REFERENCES Courses(CourseID),
    FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID)
);

CREATE TABLE StudentRegistrations (
    RegistrationID INT AUTO_INCREMENT PRIMARY KEY,
    StudentID INT,
    CourseID INT,
    DepartmentID INT,
    Semester VARCHAR(20),
    FOREIGN KEY (StudentID) REFERENCES StudentDetails(StudentID),
    FOREIGN KEY (CourseID) REFERENCES Courses(CourseID),
    FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID)
);


CREATE TABLE TeacherCourseAllocation (
    AllocationID INT AUTO_INCREMENT PRIMARY KEY,
    TeacherID INT,
    CourseID INT,
    DepartmentID INT,
    FOREIGN KEY (TeacherID) REFERENCES TeacherDetails(TeacherID),
    FOREIGN KEY (CourseID) REFERENCES Courses(CourseID),
    FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID)
);
-- Warnings table
CREATE TABLE Warnings (
    WarningID INT AUTO_INCREMENT PRIMARY KEY,
    StudentID INT,
    DepartmentID INT,
    Semester VARCHAR(20),
    WarningText TEXT NOT NULL,
    IssuedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (StudentID) REFERENCES StudentDetails(StudentID),
    FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID)
);

-- Grades table
CREATE TABLE Grades (
    GradeID INT AUTO_INCREMENT PRIMARY KEY,
    StudentID INT,
    CourseID INT,
    TeacherID INT,
    Grade CHAR(2) NOT NULL,
    FOREIGN KEY (StudentID) REFERENCES StudentDetails(StudentID),
    FOREIGN KEY (CourseID) REFERENCES Courses(CourseID),
    FOREIGN KEY (TeacherID) REFERENCES TeacherDetails(TeacherID)
);

-- Optional Transcripts table
CREATE TABLE Transcripts (
    TranscriptID INT AUTO_INCREMENT PRIMARY KEY,
    StudentID INT,
    GeneratedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FilePath VARCHAR(255),  -- Path to the generated PDF file
    FOREIGN KEY (StudentID) REFERENCES StudentDetails(StudentID)
);
-- Notifications table
CREATE TABLE Notifications (
    NotificationID INT AUTO_INCREMENT PRIMARY KEY,
    StudentID INT,
    Message TEXT,
    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (StudentID) REFERENCES StudentDetails(StudentID)
);


DELIMITER //

CREATE TRIGGER update_semester_number BEFORE INSERT ON StudentDetails
FOR EACH ROW
BEGIN
    DECLARE intake_year INT;
    DECLARE intake_semester VARCHAR(6);
    DECLARE current_year INT;
    DECLARE current_month INT;
    DECLARE semester_number INT;

    SET intake_year = SUBSTRING(NEW.IntakeSemester, 1, 4);
    SET intake_semester = SUBSTRING(NEW.IntakeSemester, 6);
    SET current_year = YEAR(CURDATE());
    SET current_month = MONTH(CURDATE());

    SET semester_number = (current_year - intake_year) * 2;

    IF intake_semester = 'Fall' THEN
        IF current_month > 6 THEN
            SET semester_number = semester_number + 2;
        ELSE
            SET semester_number = semester_number + 1;
        END IF;
    ELSEIF intake_semester = 'Spring' THEN
        IF current_month > 6 THEN
            SET semester_number = semester_number + 2;
        ELSE
            SET semester_number = semester_number + 1;
        END IF;
    END IF;

    SET NEW.CurrentSemesterNumber = semester_number;
END //

DELIMITER ;


-- Indexes
CREATE INDEX idx_student_department ON StudentDetails (DepartmentID);
CREATE INDEX idx_teacher_department ON TeacherDetails (DepartmentID);
CREATE INDEX idx_admin_department ON AdminDetails (DepartmentID);
CREATE INDEX idx_course_department ON Courses (DepartmentID);
CREATE INDEX idx_roadmap_department_course ON CourseRoadmap (DepartmentID, CourseID);
CREATE INDEX idx_registration_student_course ON StudentRegistrations (StudentID, CourseID);
CREATE INDEX idx_allocation_teacher_course ON TeacherCourseAllocation (TeacherID, CourseID);
CREATE INDEX idx_warning_student ON Warnings (StudentID);
CREATE INDEX idx_grades_student_course ON Grades (StudentID, CourseID);
CREATE INDEX idx_transcripts_student ON Transcripts (StudentID);
CREATE INDEX idx_notifications_user ON Notifications (UserID);