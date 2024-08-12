import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTableWidgetItem, QCheckBox, QMessageBox
from PyQt5 import QtCore
from ui.admin_dashboard_ui import Ui_MainWindow
from backend.course_allocation import fetch_courses, populate_comboboxes, update_confirmed_courses
from backend.admin import fetch_admin_details
from backend.teacher_allocation import fetch_departments, fetch_teachers, fetch_courses_by_department, allocate_course_to_teacher, get_teacher_allocated_credit_hours, get_teacher_allocated_courses, get_course_credit_hours
from backend.student_management import fetch_unregistered_students, fetch_students_by_gpa_range, fetch_students_by_department_and_semester, store_student_warning, fetch_semesters

class AdminDashboard(QMainWindow):
    def __init__(self, user_id=None):
        super(AdminDashboard, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.icon_only_widget.hide()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.profile_btn_2.setChecked(True)
        self.user_id = user_id
        self.setup_connections()
        populate_comboboxes(self.ui.Department_comboBox, self.ui.Semester_comboBox)
        self.display_admin_details()
        self.populate_department_combobox()
        self.populate_unregistered_department_combobox()
        self.populate_gpa_department_combobox()
        self.populate_semester_combobox(self.ui.semester_comboBox)  # Populate semester combo box for warnings

    def setup_connections(self):
        self.ui.change_btn.toggled.connect(self.toggle_menu_style)
        self.ui.user_btn.clicked.connect(self.on_user_btn_clicked)
        self.ui.stackedWidget.currentChanged.connect(self.on_stackedWidget_currentChanged)
        self.ui.home_btn_1.toggled.connect(self.on_profile_btn_toggled)
        self.ui.dashborad_btn_1.toggled.connect(self.on_student_btn_toggled)
        self.ui.orders_btn_1.toggled.connect(self.on_teacher_btn_toggled)
        self.ui.profile_btn_2.toggled.connect(self.on_profile_btn_toggled)
        self.ui.student_btn_2.toggled.connect(self.on_student_btn_toggled)
        self.ui.teacher_btn_2.toggled.connect(self.on_teacher_btn_toggled)
        self.ui.pushButton_2.clicked.connect(self.on_unregistered_btn_clicked)
        self.ui.pushButton_4.clicked.connect(self.on_gpa_check_clicked)
        self.ui.pushButton_3.clicked.connect(self.on_warning_clicked)
        self.ui.pushButton.clicked.connect(self.on_unregistered_btn_clicked)
        self.ui.exit_btn_1.clicked.connect(self.close)
        self.ui.exit_btn_2.clicked.connect(self.close)
        self.ui.apply_pushButton.clicked.connect(self.load_courses)
        self.ui.DONE_pushButton.clicked.connect(self.confirm_courses)
        self.ui.Apply_pushButton.clicked.connect(self.load_teachers_and_courses)
        self.ui.Allocation_pushButton.clicked.connect(self.allocate_courses)
        self.ui.apply_pushButton_2.clicked.connect(self.load_unregistered_students)
        self.ui.Apply_pushButton_5.clicked.connect(self.load_students_by_gpa)
        self.ui.apply_pushButton_5.clicked.connect(self.load_students_for_warning)
        self.ui.Submit_pushButton_5.clicked.connect(self.submit_warning)

    def toggle_menu_style(self, checked):
        self.ui.icon_only_widget.setVisible(checked)
        self.ui.full_menu_widget.setHidden(checked)

    def on_user_btn_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(6)

    def on_stackedWidget_currentChanged(self, index):
        btn_list = self.ui.icon_only_widget.findChildren(QPushButton) + self.ui.full_menu_widget.findChildren(QPushButton)
        for btn in btn_list:
            if index in [5, 6]:
                btn.setAutoExclusive(False)
                btn.setChecked(False)
            else:
                btn.setAutoExclusive(True)

    def on_profile_btn_toggled(self):
        if self.sender().isChecked():
            self.ui.stackedWidget.setCurrentIndex(0)

    def on_student_btn_toggled(self):
        if self.sender().isChecked():
            self.ui.stackedWidget.setCurrentIndex(1)

    def on_teacher_btn_toggled(self):
        if self.sender().isChecked():
            self.ui.stackedWidget.setCurrentIndex(2)

    def on_unregistered_btn_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def on_gpa_check_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(4)

    def on_warning_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(5)

    def display_admin_details(self):
        if self.user_id is not None:
            details = fetch_admin_details(self.user_id)
            if details:
                admin_name = details.get("AdminName", "")
                department_name = details.get("DepartmentName", "")
                mobile_no = details.get("MobileNo", "")
                email = details.get("Email", "")
                self.ui.Name_label2.setText(admin_name)
                self.ui.Department_label2.setText(department_name)
                self.ui.Mobile_lable2.setText(mobile_no)
                self.ui.Email_label2.setText(email)
    def load_courses(self):
        department_id = self.ui.Department_comboBox.currentData()
        semester = self.ui.Semester_comboBox.currentText()
        if department_id and semester:
            courses = fetch_courses(department_id, semester)
            self.ui.tableWidget.setRowCount(len(courses))
            for row, course in enumerate(courses):
                course_id, course_code, course_title, credit_hours = course
                course_code_item = QTableWidgetItem(course_code)
                course_code_item.setData(QtCore.Qt.UserRole, course_id)
                self.ui.tableWidget.setItem(row, 0, course_code_item)
                self.ui.tableWidget.setItem(row, 1, QTableWidgetItem(course_title))
                self.ui.tableWidget.setItem(row, 2, QTableWidgetItem(str(credit_hours)))
                checkBox = QCheckBox()
                self.ui.tableWidget.setCellWidget(row, 3, checkBox)

    def confirm_courses(self):
        department_id = self.ui.Department_comboBox.currentData()
        semester = self.ui.Semester_comboBox.currentText()
        confirmed_courses = []
        for row in range(self.ui.tableWidget.rowCount()):
            checkBox = self.ui.tableWidget.cellWidget(row, 3)
            if checkBox.isChecked():
                course_id = self.ui.tableWidget.item(row, 0).data(QtCore.Qt.UserRole)
                confirmed_courses.append((course_id, department_id, semester))
        try:
            already_confirmed_courses = update_confirmed_courses(confirmed_courses)
            if already_confirmed_courses:
                self.show_message("Information", f"Some courses were already allocated: {', '.join(already_confirmed_courses)}")
            else:
                self.show_message("Success", "All selected courses have been successfully allocated.")
        except Exception as e:
            self.show_message("Error", f"An error occurred: {e}")

    def show_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()

    def populate_department_combobox(self):
        departments = fetch_departments()
        self.ui.DEpartment_comboBox.clear()
        self.ui.Department_comboBox_2.clear()
        self.ui.department_comboBox.clear()
        self.ui.Department_warnig_comboBox.clear()
        for department_id, department_name in departments:
            self.ui.DEpartment_comboBox.addItem(department_name, department_id)
            self.ui.Department_comboBox_2.addItem(department_name, department_id)
            self.ui.department_comboBox.addItem(department_name, department_id)
            self.ui.Department_warnig_comboBox.addItem(department_name, department_id)

    def populate_unregistered_department_combobox(self):
        departments = fetch_departments()
        self.ui.Department_comboBox_2.clear()
        for department_id, department_name in departments:
            self.ui.Department_comboBox_2.addItem(department_name, department_id)

    def populate_gpa_department_combobox(self):
        departments = fetch_departments()
        self.ui.department_comboBox.clear()
        for department_id, department_name in departments:
            self.ui.department_comboBox.addItem(department_name, department_id)

    def populate_semester_combobox(self, combobox):
        semesters = fetch_semesters()
        combobox.clear()
        for semester in semesters:
            combobox.addItem(semester)

    def load_teachers_and_courses(self):
        department_id = self.ui.DEpartment_comboBox.currentData()
        if department_id:
            teachers = fetch_teachers(department_id)
            self.ui.Teacher_comboBox.clear()
            for teacher_id, teacher_name in teachers:
                self.ui.Teacher_comboBox.addItem(teacher_name, teacher_id)

            courses = fetch_courses_by_department(department_id)
            self.ui.Course1_comboBox.clear()
            self.ui.Course2_comboBox.clear()
            self.ui.Course3_comboBox.clear()
            for course_id, course_title in courses:
                self.ui.Course1_comboBox.addItem(course_title, course_id)
                self.ui.Course2_comboBox.addItem(course_title, course_id)
                self.ui.Course3_comboBox.addItem(course_title, course_id)

    def allocate_courses(self):
        teacher_id = self.ui.Teacher_comboBox.currentData()
        department_id = self.ui.Department_comboBox_2.currentData()
        course_ids = [
            self.ui.Course1_comboBox.currentData(),
            self.ui.Course2_comboBox.currentData(),
            self.ui.Course3_comboBox.currentData()
        ]
        if teacher_id and department_id:
            allocated_credit_hours = get_teacher_allocated_credit_hours(teacher_id)
            allocated_courses = get_teacher_allocated_courses(teacher_id)

            if allocated_credit_hours >= 9 or allocated_courses >= 3:
                self.show_message("Warning", "This teacher has already been allocated the maximum credit hours or courses.")
                return

            for course_id in course_ids:
                if course_id:
                    try:
                        allocate_course_to_teacher(teacher_id, course_id, department_id)
                    except Exception as e:
                        self.show_message("Error", f"Failed to allocate course: {e}")
                        return

            if allocated_credit_hours + sum(get_course_credit_hours(course_id) for course_id in course_ids) >= 9 or allocated_courses + len(course_ids) >= 3:
                index = self.ui.Teacher_comboBox.findData(teacher_id)
                self.ui.Teacher_comboBox.removeItem(index)

            for course_id in course_ids:
                if course_id:
                    self.remove_course_from_comboboxes(course_id)

            self.show_message("Success", "Courses allocated successfully.")
        else:
            self.show_message("Warning", "Please select both a teacher and a department.")

    def remove_course_from_comboboxes(self, course_id):
        for combo_box in [self.ui.Course1_comboBox, self.ui.Course2_comboBox, self.ui.Course3_comboBox]:
            index = combo_box.findData(course_id)
            if index != -1:
                combo_box.removeItem(index)

    def load_unregistered_students(self):
        department_id = self.ui.Department_comboBox_2.currentData()
        if department_id:
            students = fetch_unregistered_students(department_id)
            self.ui.tableWidget_2.setRowCount(len(students))
            for row, student in enumerate(students):
                enrollment, name, semester = student
                self.ui.tableWidget_2.setItem(row, 0, QTableWidgetItem(enrollment))
                self.ui.tableWidget_2.setItem(row, 1, QTableWidgetItem(name))
                self.ui.tableWidget_2.setItem(row, 2, QTableWidgetItem(str(semester)))

    def load_students_by_gpa(self):
        department_id = self.ui.department_comboBox.currentData()
        gpa_range = self.ui.gpa_comboBox_4.currentText()
        if department_id and gpa_range:
            students = fetch_students_by_gpa_range(department_id, gpa_range)
            self.ui.student_tableWidget.setRowCount(len(students))
            for row, student in enumerate(students):
                enrollment, name, semester = student
                self.ui.student_tableWidget.setItem(row, 0, QTableWidgetItem(enrollment))
                self.ui.student_tableWidget.setItem(row, 1, QTableWidgetItem(name))
                self.ui.student_tableWidget.setItem(row, 2, QTableWidgetItem(str(semester)))

    def load_students_for_warning(self):
        department_id = self.ui.Department_warnig_comboBox.currentData()
        semester = self.ui.semester_comboBox.currentText()
        if department_id and semester:
            students = fetch_students_by_department_and_semester(department_id, semester)
            self.ui.Student_comboBox_4.clear()
            for student_id, student_name in students:
                self.ui.Student_comboBox_4.addItem(student_name, student_id)

    def submit_warning(self):
        student_id = self.ui.Student_comboBox_4.currentData()
        department_id = self.ui.Department_warnig_comboBox.currentData()
        semester = self.ui.semester_comboBox.currentText()
        warning_text = self.ui.Warring_textedit.toPlainText()
        if student_id and department_id and semester and warning_text:
            try:
                store_student_warning(student_id, department_id, semester, warning_text)
                self.show_message("Success", "Warning submitted successfully.")
            except Exception as e:
                self.show_message("Error", f"Failed to submit warning: {e}")
        else:
            self.show_message("Warning", "Please fill in all fields.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdminDashboard(user_id=1)
    window.show()
    sys.exit(app.exec())
