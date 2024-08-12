import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTableWidgetItem, QMessageBox, QCheckBox, QListWidgetItem
from ui.student_dashboard_ui import Ui_MainWindow
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import QPropertyAnimation, QRect
from backend.student import get_student_profile, get_courses_for_student, get_gpa, get_confirmed_courses, register_courses, is_course_already_registered, check_student_passed_courses, get_student_transcript_data, get_notifications
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PyQt5.QtWidgets import QMessageBox

class NotificationDialog(QDialog):
    def __init__(self, notifications, parent=None):
        super(NotificationDialog, self).__init__(parent)
        self.setWindowTitle("Notifications")
        self.setGeometry(300, 300, 400, 200)
        layout = QVBoxLayout(self)

        for notification in notifications:
            label = QLabel(notification['Message'], self)
            layout.addWidget(label)

        ok_button = QPushButton("OK", self)
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)

        self.setLayout(layout)
        self.setup_animation()

    def setup_animation(self):
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(1000)
        self.animation.setStartValue(QRect(self.x(), self.y(), 0, 0))
        self.animation.setEndValue(QRect(self.x(), self.y(), self.width(), self.height()))
        self.animation.start()


class StudentDashboard(QMainWindow):
    def __init__(self, user_id):
        super(StudentDashboard, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.user_id = user_id  # Store user ID
        self.ui.icon_only_widget.hide()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.profile_btn_2.setChecked(True)

        self.setup_connections()
        self.load_profile()
        self.load_courses()
        self.load_gpa()
        self.load_confirmed_courses()
        self.load_notifications()  # Load notifications

    def setup_connections(self):
        self.ui.change_btn.toggled.connect(self.toggle_menu_style)
        self.ui.user_btn.clicked.connect(self.on_user_btn_clicked)
        self.ui.stackedWidget.currentChanged.connect(self.on_stackedWidget_currentChanged)

        self.ui.profile_btn_2.toggled.connect(self.on_profile_btn_toggled)
        self.ui.registration_btn_2.toggled.connect(self.on_registration_btn_toggled)
        self.ui.courses_btn_2.toggled.connect(self.on_courses_btn_toggled)
        self.ui.GPA_btn_2.toggled.connect(self.on_GPA_btn_toggled)
        self.ui.transcript_btn_2.toggled.connect(self.on_transcript_btn_toggled)

        self.ui.student_btn_1.toggled.connect(self.on_profile_btn_toggled)
        self.ui.registor_btn_1.toggled.connect(self.on_registration_btn_toggled)
        self.ui.courses_btn_1.toggled.connect(self.on_courses_btn_toggled)
        self.ui.gpa_btn_1.toggled.connect(self.on_GPA_btn_toggled)
        self.ui.exit_btn_2.clicked.connect(self.close)
        self.ui.exit_btn_1.clicked.connect(self.close)

        self.ui.registor_pushButton.clicked.connect(self.register_courses)  # Connect register button
        self.ui.generatePdf_pushButton.clicked.connect(self.generate_transcript_pdf)  # Connect transcript button

    def toggle_menu_style(self, checked):
        self.ui.icon_only_widget.setVisible(checked)
        self.ui.full_menu_widget.setHidden(checked)

    def on_user_btn_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def on_stackedWidget_currentChanged(self, index):
        btn_list = self.ui.icon_only_widget.findChildren(QPushButton) + self.ui.full_menu_widget.findChildren(QPushButton)
        for btn in btn_list:
            if index in [5, 6]:  # Adjust the indices as necessary
                btn.setAutoExclusive(False)
                btn.setChecked(False)
            else:
                btn.setAutoExclusive(True)

    def on_profile_btn_toggled(self):
        if self.sender().isChecked():
            self.ui.stackedWidget.setCurrentIndex(0)
            self.load_profile()  # Reload profile information

    def on_registration_btn_toggled(self):
        if self.sender().isChecked():
            self.ui.stackedWidget.setCurrentIndex(1)
            self.load_confirmed_courses()  # Load confirmed courses when switching to registration

    def on_courses_btn_toggled(self):
        if self.sender().isChecked():
            self.ui.stackedWidget.setCurrentIndex(2)

    def on_GPA_btn_toggled(self):
        if self.sender().isChecked():
            self.ui.stackedWidget.setCurrentIndex(3)
            self.load_gpa()

    def on_transcript_btn_toggled(self):
        if self.sender().isChecked():
            self.ui.stackedWidget.setCurrentIndex(4)

    def load_profile(self):
        profile = get_student_profile(self.user_id)
        if profile:
            self.ui.enrollment_label2.setText(profile['Enrollment'])
            self.ui.name_label2.setText(profile['Name'])
            self.ui.department_label2.setText(profile['DepartmentName'])
            self.ui.intakesemester_label2.setText(profile['IntakeSemester'])
            self.ui.mobile_label2.setText(profile['MobileNo'])
            self.ui.personalEmail_label2.setText(profile['PersonalEmail'])
            self.ui.currentAddress_label2.setText(profile['CurrentAddress'])
            self.ui.permanentAddress_label2.setText(profile['PermanentAddress'])
            self.ui.registrationNo_label2.setText(profile['RegistrationNo'])
            self.ui.fathername_label2.setText(profile['FatherName'])
            self.ui.degreeDuration_label2.setText(profile['DegreeDuration'])
            self.ui.maxsemester_label2.setText(profile['MaxSemester'])
            self.ui.phoneNo_label2.setText(profile['PhoneNo'])
            self.ui.universityEmail_label2.setText(profile['UniversityEmail'])

    def load_courses(self):
        courses = get_courses_for_student(self.user_id)
        self.ui.course_tableWidget.setRowCount(0)  # Clear existing rows
        for course in courses:
            row_position = self.ui.course_tableWidget.rowCount()
            self.ui.course_tableWidget.insertRow(row_position)
            self.ui.course_tableWidget.setItem(row_position, 0, QTableWidgetItem(course['SubjectCode']))
            self.ui.course_tableWidget.setItem(row_position, 1, QTableWidgetItem(course['CourseTitle']))
            self.ui.course_tableWidget.setItem(row_position, 2, QTableWidgetItem(str(course['CreditHours'])))
            self.ui.course_tableWidget.setItem(row_position, 3, QTableWidgetItem(course['TeacherName']))
            self.ui.course_tableWidget.setItem(row_position, 4, QTableWidgetItem(course['Semester']))

    def load_gpa(self):
        gpa_data = get_gpa(self.user_id)
        self.ui.GPA_tableWidget_3.setRowCount(0)  # Clear existing rows
        total_credits = 0.0
        total_points = 0.0
        for entry in gpa_data:
            row_position = self.ui.GPA_tableWidget_3.rowCount()
            self.ui.GPA_tableWidget_3.insertRow(row_position)
            self.ui.GPA_tableWidget_3.setItem(row_position, 0, QTableWidgetItem(entry['CourseCode']))
            self.ui.GPA_tableWidget_3.setItem(row_position, 1, QTableWidgetItem(entry['CourseTitle']))
            self.ui.GPA_tableWidget_3.setItem(row_position, 2, QTableWidgetItem(str(entry['CreditHours'])))
            self.ui.GPA_tableWidget_3.setItem(row_position, 3, QTableWidgetItem(entry['Grade']))
            grade_points = float(entry['GradePoints']) if entry['GradePoints'] is not None else 0.0
            product = float(entry['Product']) if entry['Product'] is not None else 0.0
            self.ui.GPA_tableWidget_3.setItem(row_position, 4, QTableWidgetItem(str(grade_points)))
            self.ui.GPA_tableWidget_3.setItem(row_position, 5, QTableWidgetItem(str(product)))
            total_credits += entry['CreditHours']
            total_points += product
        gpa = total_points / total_credits if total_credits != 0 else 0
        self.ui.GPA_label2.setText(f"{gpa:.2f}")


    def load_confirmed_courses(self):
        semester = 1  # Replace with actual current semester
        courses = get_confirmed_courses(self.user_id, semester)
        self.ui.Courseregistration_tableWidget.setRowCount(0)  # Clear existing rows
        for course in courses:
            row_position = self.ui.Courseregistration_tableWidget.rowCount()
            self.ui.Courseregistration_tableWidget.insertRow(row_position)
            self.ui.Courseregistration_tableWidget.setItem(row_position, 0, QTableWidgetItem(course['SubjectCode']))
            self.ui.Courseregistration_tableWidget.setItem(row_position, 1, QTableWidgetItem(course['CourseTitle']))
            self.ui.Courseregistration_tableWidget.setItem(row_position, 2, QTableWidgetItem(str(course['CreditHours'])))
            self.ui.Courseregistration_tableWidget.setItem(row_position, 3, QTableWidgetItem(course['TeacherName']))
            check_box = QCheckBox()
            check_box.setObjectName(f"course_{course['CourseID']}")
            self.ui.Courseregistration_tableWidget.setCellWidget(row_position, 4, check_box)

    def register_courses(self):
        rows = self.ui.Courseregistration_tableWidget.rowCount()
        selected_courses = []
        for row in range(rows):
            check_box = self.ui.Courseregistration_tableWidget.cellWidget(row, 4)
            if check_box.isChecked():
                course_id = check_box.objectName().split('_')[1]
                if not is_course_already_registered(self.user_id, int(course_id)):
                    selected_courses.append(int(course_id))
                else:
                    QMessageBox.warning(self, "Already Registered", f"Course ID {course_id} is already registered.")

        if selected_courses:
            try:
                register_courses(self.user_id, selected_courses)
                QMessageBox.information(self, "Success", "Courses registered successfully!")
                self.load_courses()  # Reload the courses to reflect new registrations
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred during registration: {str(e)}")
        else:
            QMessageBox.warning(self, "No Selection", "Please select at least one course to register.")

    def generate_transcript_pdf(self):
        # Check if the student has passed all courses according to the roadmap
        if not check_student_passed_courses(self.user_id):
            QMessageBox.warning(self, "Incomplete Courses", "You have not passed all the required courses according to your roadmap.")
            return

        # Generate the transcript PDF
        profile = get_student_profile(self.user_id)
        courses = get_student_transcript_data(self.user_id)

        pdf_filename = f"{profile['Name']}_transcript.pdf"
        c = canvas.Canvas(pdf_filename, pagesize=letter)
        width, height = letter

        # Add title
        c.setFont("Helvetica-Bold", 16)
        c.drawString(200, height - 40, "Official Transcript")

        # Add profile information
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 80, f"Name: {profile['Name']}")
        c.drawString(50, height - 100, f"Enrollment: {profile['Enrollment']}")
        c.drawString(50, height - 120, f"Department: {profile['DepartmentName']}")
        c.drawString(50, height - 140, f"Intake Semester: {profile['IntakeSemester']}")

        # Add table headers
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, height - 180, "Course Code")
        c.drawString(150, height - 180, "Course Title")
        c.drawString(300, height - 180, "Credit Hours")
        c.drawString(400, height - 180, "Grade")

        # Add table rows
        c.setFont("Helvetica", 12)
        y = height - 200
        for course in courses:
            c.drawString(50, y, course['CourseCode'])
            c.drawString(150, y, course['CourseTitle'])
            c.drawString(300, y, str(course['CreditHours']))
            c.drawString(400, y, course['Grade'])
            y -= 20

        c.save()
        QMessageBox.information(self, "PDF Generated", f"Transcript has been generated and saved as {pdf_filename}.")

    def load_notifications(self):
        notifications = get_notifications(self.user_id)
        if notifications:
            dialog = NotificationDialog(notifications, self)
            dialog.exec_()
  
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudentDashboard(user_id=1)
    window.show()
    sys.exit(app.exec())

