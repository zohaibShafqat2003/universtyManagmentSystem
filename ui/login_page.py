from PyQt5.QtWidgets import QMainWindow, QMessageBox
from ui.login_page_ui import Ui_MainWindow
from backend.login import authenticate_user
from ui.student_dashboard import StudentDashboard
from ui.teacher_dashboard import TeacherDashboard
from ui.admin_dashboard import AdminDashboard

class LoginPage(QMainWindow, Ui_MainWindow):
    def __init__(self, role):
        super().__init__()
        self.role = role
        self.setupUi(self)
        self.setWindowTitle(f"{role} Login")

        self.loginButton.clicked.connect(self.login)

    def login(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        result = authenticate_user(username, password, self.role)
        if result:
            QMessageBox.information(self, 'Success', 'Login successful!')
            self.show_profile_page(result[0])
        else:
            QMessageBox.warning(self, 'Error', 'Invalid credentials.')

    def show_profile_page(self, user_id):
        if self.role == 'Student':
            self.profile_page = StudentDashboard(user_id)
        elif self.role == 'Teacher':
            self.profile_page = TeacherDashboard(user_id)
        elif self.role == 'Admin':
            self.profile_page = AdminDashboard(user_id)

        self.profile_page.show()
        self.close()
