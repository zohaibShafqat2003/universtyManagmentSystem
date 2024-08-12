INSERT INTO Departments (DepartmentName) VALUES
('Computer Science'),
('Electrical Engineering'),
('Business Administration');


INSERT INTO Login (UserName, Password, Salt, Role) VALUES
('zoahib', 'password1', 'salt3', 'teacher');
SELECT * FROM cms2.teacherdetails;
delete from login
where loginID -
-- Assuming LoginID 1 belongs to a student
INSERT INTO StudentDetails (StudentID, Enrollment, Name, DepartmentID, IntakeSemester, MobileNo, PersonalEmail, CurrentAddress, PermanentAddress, RegistrationNo, FatherName, DegreeDuration, MaxSemester, PhoneNo, UniversityEmail) VALUES
(1, 'CS-2024-001', 'John Doe', 1, '2024 Fall', '123-456-7890', 'john.doe@example.com', '123 Maple Street', '456 Oak Street', 'REG-001', 'Doe Senior', '4 years', '8', '321-654-0987', 'john.doe@university.com');

-- Assuming LoginID 2 belongs to a teacher
INSERT INTO TeacherDetails (TeacherID, FirstName, LastName, Institute, DepartmentID, MobileNo, Email) VALUES
(2, 'Jane', 'Doe', 'University of Example', 1, '321-654-0987', 'jane.doe@university.com');
-- Assuming LoginID 2 belongs to a teacher
INSERT INTO TeacherDetails (TeacherID, FirstName, LastName, Institute, DepartmentID, MobileNo, Email) VALUES
(6, 'zohaib', 'Doe', 'University of Example', 1, '301-654-0987', 'jane.doe@universoty.com');

-- Assuming LoginID 3 belongs to an admin
INSERT INTO AdminDetails (AdminID, DepartmentID, MobileNo, Email) VALUES
(3, 1, '987-654-3210', 'admin@university.com');

INSERT INTO Login (UserName, Password, Salt, Role) VALUES
('emily.turner', 'hashed_password4', 'salt4', 'Student'),
('michael.smith', 'hashed_password5', 'salt5', 'Student'),
('sarah.johnson', 'hashed_password6', 'salt6', 'Student'),
('alex.lee', 'hashed_password7', 'salt7', 'Student'),
('laura.white', 'hashed_password8', 'salt8', 'Student');

INSERT INTO StudentDetails (
    StudentID, Enrollment, Name, DepartmentID, IntakeSemester, MobileNo, PersonalEmail, CurrentAddress, PermanentAddress, RegistrationNo, FatherName, DegreeDuration, MaxSemester, PhoneNo, UniversityEmail
) VALUES
-- Student 2: Computer Science Department
(2, 'CS-2024-002', 'Emily Turner', 1, '2024 Fall', '555-234-5678', 'emily.turner@example.com', '234 Pine Street', '789 Birch Street', 'REG-002', 'Turner Senior', '4 years', '8', '666-777-8888', 'emily.turner@university.com'),

-- Student 3: Electrical Engineering Department
(3, 'EE-2024-001', 'Michael Smith', 2, '2024 Fall', '555-345-6789', 'michael.smith@example.com', '345 Cedar Lane', '890 Ash Lane', 'REG-003', 'Smith Senior', '4 years', '8', '777-888-9999', 'michael.smith@university.com'),

-- Student 4: Business Administration Department
(4, 'BA-2024-001', 'Sarah Johnson', 3, '2024 Fall', '555-456-7890', 'sarah.johnson@example.com', '456 Spruce Rd', '321 Pine Rd', 'REG-004', 'Johnson Senior', '4 years', '8', '888-999-0000', 'sarah.johnson@university.com'),

-- Student 5: Computer Science Department, Spring Intake
(5, 'CS-2025-001', 'Alex Lee', 1, '2025 Spring', '555-567-8901', 'alex.lee@example.com', '567 Oak Road', '432 Maple Road', 'REG-005', 'Lee Senior', '4 years', '8', '999-000-1111', 'alex.lee@university.com'),

-- Student 6: Electrical Engineering Department, Spring Intake
(6, 'EE-2025-002', 'Laura White', 2, '2025 Spring', '555-678-9012', 'laura.white@example.com', '678 Redwood Blvd', '543 Elm Blvd', 'REG-006', 'White Senior', '4 years', '8', '000-111-2222', 'laura.white@university.com');


INSERT INTO Login (UserName, Password, Salt, Role) VALUES
('susan.miller', 'hashed_password9', 'salt9', 'Teacher'),
('robert.brown', 'hashed_password10', 'salt10', 'Teacher'),
('lisa.jones', 'hashed_password11', 'salt11', 'Teacher');

-- Fetching newly created LoginIDs assuming the UserName is known and unique
-- It’s a best practice to fetch these IDs programmatically or from session data immediately after creation if this script runs separately

-- Placeholder variables (replace these with actual fetched LoginIDs)
SET @susanID = (SELECT LoginID FROM Login WHERE UserName = 'susan.miller');
SET @robertID = (SELECT LoginID FROM Login WHERE UserName = 'robert.brown');
SET @lisaID = (SELECT LoginID FROM Login WHERE UserName = 'lisa.jones');

INSERT INTO TeacherDetails (TeacherID, FirstName, LastName, Institute, DepartmentID, MobileNo, Email) VALUES
(@susanID, 'Susan', 'Miller', 'University of Example', 1, '321-000-0001', 'susan.miller@university.com'),
(@robertID, 'Robert', 'Brown', 'University of Example', 1, '321-000-0002', 'robert.brown@university.com'),
(@lisaID, 'Lisa', 'Jones', 'University of Example', 1, '321-000-0003', 'lisa.jones@university.com');






