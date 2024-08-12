import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QStackedWidget
from ui.login_page import LoginPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CMS Dashboard")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.home_widget = QWidget()
        home_layout = QVBoxLayout()

        self.student_button = QPushButton('Student Login')
        self.teacher_button = QPushButton('Teacher Login')
        self.admin_button = QPushButton('Admin Login')

        self.student_button.clicked.connect(lambda: self.show_login_page('Student'))
        self.teacher_button.clicked.connect(lambda: self.show_login_page('Teacher'))
        self.admin_button.clicked.connect(lambda: self.show_login_page('Admin'))

        home_layout.addWidget(self.student_button)
        home_layout.addWidget(self.teacher_button)
        home_layout.addWidget(self.admin_button)

        self.home_widget.setLayout(home_layout)
        self.stacked_widget.addWidget(self.home_widget)

    def show_login_page(self, role):
        self.login_page = LoginPage(role)
        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.setCurrentWidget(self.login_page)
        self.login_page.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

