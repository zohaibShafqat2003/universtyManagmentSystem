import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTableWidgetItem, QMessageBox
from PyQt5 import QtWidgets

from ui.teacher_dashboard_ui import Ui_MainWindow
from backend.teacher import get_teacher_profile, get_courses, get_students_in_course, mark_student_grade

class TeacherDashboard(QMainWindow):
    def __init__(self, user_id):
        super(TeacherDashboard, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.user_id = user_id  # Store user ID
        self.ui.icon_only_widget.hide()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.profile_btn_2.setChecked(True)

        self.setup_connections()
        self.load_profile()
        self.load_courses()  # Load courses when initializing
        self.populate_grade_combobox()  # Populate the grade combobox

    def setup_connections(self):
        self.ui.change_btn.toggled.connect(self.toggle_menu_style)
        self.ui.user_btn.clicked.connect(self.on_user_btn_clicked)
        self.ui.stackedWidget.currentChanged.connect(self.on_stackedWidget_currentChanged)

        self.ui.home_btn_1.toggled.connect(self.on_profile_btn_toggled)
        self.ui.dashborad_btn_1.toggled.connect(self.on_dashboard_btn_toggled)
        self.ui.orders_btn_1.toggled.connect(self.on_orders_btn_toggled)
        self.ui.profile_btn_2.toggled.connect(self.on_profile_btn_toggled)
        self.ui.view_course_btn_2.toggled.connect(self.on_dashboard_btn_toggled)
        self.ui.mark_grade_btn_2.toggled.connect(self.on_orders_btn_toggled)

        self.ui.apply_pushButton.clicked.connect(self.on_apply_course_selection)
        self.ui.submit_pushButton.clicked.connect(self.on_submit_grade)

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

    def on_dashboard_btn_toggled(self):
        if self.sender().isChecked():
            self.ui.stackedWidget.setCurrentIndex(1)
            self.load_courses()  # Load courses when switching to dashboard

    def on_orders_btn_toggled(self):
        if self.sender().isChecked():
            self.ui.stackedWidget.setCurrentIndex(2)

    def load_profile(self):
        profile = get_teacher_profile(self.user_id)
        if profile:
            self.ui.firstName_label2.setText(profile['FirstName'])
            self.ui.lastName_label2.setText(profile['LastName'])
            self.ui.department_label2.setText(profile['DepartmentName'])
            self.ui.institute_label2.setText(profile['Institute'])
            self.ui.mobileNo_label2.setText(profile['MobileNo'])
            self.ui.email_label2.setText(profile['Email'])

    def load_courses(self):
        courses = get_courses(self.user_id)
        self.ui.viewCourse_tableWidget.setRowCount(0)  # Clear existing rows
        for course in courses:
            row_position = self.ui.viewCourse_tableWidget.rowCount()
            self.ui.viewCourse_tableWidget.insertRow(row_position)
            self.ui.viewCourse_tableWidget.setItem(row_position, 0, QTableWidgetItem(course['SubjectCode']))
            self.ui.viewCourse_tableWidget.setItem(row_position, 1, QTableWidgetItem(course['CourseTitle']))
            self.ui.viewCourse_tableWidget.setItem(row_position, 2, QTableWidgetItem(str(course['CreditHours'])))
            self.ui.viewCourse_tableWidget.setItem(row_position, 3, QTableWidgetItem(str(course['DepartmentID'])))
        self.load_course_dropdown(courses)

    def load_course_dropdown(self, courses):
        self.ui.course_comboBox.clear()
        for course in courses:
            self.ui.course_comboBox.addItem(course['CourseTitle'], course['CourseID'])

    def on_apply_course_selection(self):
        selected_course = self.ui.course_comboBox.currentData()
        if selected_course:
            students = get_students_in_course(selected_course)
            self.ui.student_comboBox.clear()
            for student in students:
                self.ui.student_comboBox.addItem(student['Name'], student['StudentID'])

    def on_submit_grade(self):
        student_id = self.ui.student_comboBox.currentData()
        selected_grade = self.ui.markGrade_comboBox.currentText()
        course_id = self.ui.course_comboBox.currentData()
        if student_id and selected_grade and course_id:
            success, message = mark_student_grade(student_id, course_id, self.user_id, selected_grade)
            if success:
                QMessageBox.information(self, 'Success', message)
            else:
                QMessageBox.warning(self, 'Error', message)
        else:
            QMessageBox.warning(self, 'Error', 'Please select a student, course, and grade.')

    def populate_grade_combobox(self):
        grades = ['A+', 'A', 'B+', 'B', 'C+', 'C', 'D+', 'D', 'F']
        for grade in grades:
            self.ui.markGrade_comboBox.addItem(grade)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Replace 'user_id' with the actual user ID you want to view the profile of
    window = TeacherDashboard(user_id=1)
    window.show()

    sys.exit(app.exec())