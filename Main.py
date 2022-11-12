import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sqlite3
import re
from PyQt5.QtCore import *

db = sqlite3.connect('Data.db')
cr = db.cursor()
cr.execute("Create table if not exists user(name text, email text, password text)")

UserName = "None"
email = "None"


class WelcomePage(QWidget):
    def __init__(self):
        super(WelcomePage, self).__init__()

        with open('style/welcome.css') as file:
            style = file.read()
            self.setStyleSheet(style)

        self.setWindowTitle('Productivity')
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(50, 0, 50, 50)

        welcome_text = QLabel("Welcome To")
        welcome_text.setObjectName('wel')

        txt2 = QLabel("Productivity Club")
        txt2.setObjectName("txt2")

        login_button = QPushButton("Login")
        sign_up_button = QPushButton("Sign Up")
        login_button.setObjectName("login")
        sign_up_button.setObjectName("login")

        main_layout.addWidget(welcome_text)
        main_layout.addWidget(txt2)
        main_layout.addWidget(login_button)
        main_layout.addWidget(sign_up_button)

        def go_to_login():
            Windows.setCurrentIndex(1)

        login_button.clicked.connect(go_to_login)

        def go_to_signup():
            Windows.setCurrentIndex(2)

        sign_up_button.clicked.connect(go_to_signup)
        self.setLayout(main_layout)


class LoginPage(QWidget):
    def __init__(self):
        super(LoginPage, self).__init__()
        with open("style/login.css") as file:
            style = file.read()
            self.setStyleSheet(style)
        main_layout = QVBoxLayout()
        # main_layout.addSpacing(50)
        main_layout.setContentsMargins(50, 0, 50, 50)

        back = QPushButton(self)
        back.setObjectName("back")
        back.setIcon(QIcon('Icons/back.svg'))
        back.setGeometry(20, 10, 30, 30)

        lb1 = QLabel("Login")
        lb1.setObjectName("lb1")
        lb2 = QLabel("Enter Your Email And Password")
        lb2.setObjectName("lb2")

        email_field = QLineEdit()
        email_field.setPlaceholderText("Email")
        email_field.setObjectName("field")

        password_field = QLineEdit()
        password_field.setEchoMode(QLineEdit.Password)
        password_field.setPlaceholderText("Password")
        password_field.setObjectName("field")

        login_btn = QPushButton("Login")
        login_btn.setObjectName("login")

        # main_layout.addWidget(back)
        main_layout.addWidget(lb1)
        main_layout.addWidget(lb2)
        main_layout.addWidget(email_field)
        main_layout.addWidget(password_field)
        main_layout.addWidget(login_btn)

        def go_back():
            Windows.setCurrentIndex(0)

        def checkinput():
            cr.execute(f"select name , email , password from user "
                       f"where email='{email_field.text()}' and password='{password_field.text()}'")
            result = cr.fetchall()
            if email_field.text() == "" or password_field == "":
                QMessageBox.warning(self, "warning", "You can't leave any input field empty", QMessageBox.Ok)
            elif len(result) >= 1:
                # SET USER DATA
                Windows.setCurrentIndex(3)
            else:
                QMessageBox.warning(self, "warning", "Email and Password are incorrect", QMessageBox.Ok)

        back.clicked.connect(go_back)
        login_btn.clicked.connect(checkinput)
        self.setLayout(main_layout)


class SignPage(QWidget):
    def __init__(self):
        super(SignPage, self).__init__()

        with open("style/signup.css") as file:
            style = file.read()
            self.setStyleSheet(style)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 0, 50, 50)

        back = QPushButton(self)
        back.setObjectName("back")
        back.setIcon(QIcon('Icons/back.svg'))
        back.setGeometry(20, 10, 30, 30)

        lb1 = QLabel("Sign Up")
        lb1.setObjectName("lb1")

        name = QLineEdit()
        name.setPlaceholderText("Your Name")
        name.setObjectName("field")

        email_field = QLineEdit()
        email_field.setPlaceholderText("Email")
        email_field.setObjectName("field")

        password_field = QLineEdit()
        password_field.setEchoMode(QLineEdit.Password)
        password_field.setPlaceholderText("Password")
        password_field.setObjectName("field")

        co_password_field = QLineEdit()
        co_password_field.setEchoMode(QLineEdit.Password)
        co_password_field.setPlaceholderText("Confirm Password")
        co_password_field.setObjectName("field")

        signup_btn = QPushButton("Sign Up")
        signup_btn.setObjectName("signup")

        def sign():
            cr.execute(f"select email from user")
            emails = cr.fetchall()
            reg = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
            is_email = re.fullmatch(reg, email_field.text())
            if name.text() == "" or email_field.text() == "" or password_field == "":
                QMessageBox.warning(self, "warning", "You can't leave any input field empty", QMessageBox.Ok)
            elif password_field.text() != co_password_field.text():
                QMessageBox.warning(self, "warning", "Password and Confirm Password aren't the same", QMessageBox.Ok)
            elif (email_field.text(),) in emails:
                QMessageBox.warning(self, "warning", "This Email is already used, Please use another one",
                                    QMessageBox.Ok)
            elif not is_email:
                QMessageBox.warning(self, "warning", "Please enter a valid email \nSuch as : Mostafa_12@gmail.com ",
                                    QMessageBox.Ok)
            else:
                cr.execute(
                    f"insert into user values('{name.text()}', '{email_field.text()}', '{password_field.text()}')")
                db.commit()
                db.close()
                Windows.setCurrentIndex(3)

        signup_btn.clicked.connect(sign)

        def go_back():
            Windows.setCurrentIndex(0)

        back.clicked.connect(go_back)

        main_layout.addWidget(lb1)
        main_layout.addWidget(name)
        main_layout.addWidget(email_field)
        main_layout.addWidget(password_field)
        main_layout.addWidget(co_password_field)
        main_layout.addWidget(signup_btn)

        self.setLayout(main_layout)


class Btn(QPushButton):
    def __init__(self, path):
        super().__init__()
        self.setIcon(QIcon(path))
        self.setIconSize(QSize(50, 50))


class Home(QWidget):
    def __init__(self):
        super().__init__()

        with open("style/btn.css") as file:
            style = file.read()
            self.setStyleSheet(style)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 50, 50, 50)
        txt = QLabel("User Name")
        l1 = QHBoxLayout()
        l2 = QHBoxLayout()

        task = Btn("Icons/task.png")
        timer = Btn("Icons/timer.png")
        note = Btn("Icons/Note.png")
        l1.addWidget(task)
        l1.addWidget(timer)
        l1.addWidget(note)

        converter = Btn("Icons/converter.png")
        translator = Btn("Icons/translator.png")
        graph = Btn("Icons/graph.png")
        l2.addWidget(converter)
        l2.addWidget(translator)
        l2.addWidget(graph)

        def to_task():
            Windows.setCurrentIndex(4)

        task.clicked.connect(to_task)

        def to_timer():
            Windows.setCurrentIndex(5)

        task.clicked.connect(to_task)

        def to_note():
            Windows.setCurrentIndex(6)

        task.clicked.connect(to_task)

        def to_converter():
            Windows.setCurrentIndex(7)

        task.clicked.connect(to_task)

        def to_translator():
            Windows.setCurrentIndex(8)

        task.clicked.connect(to_task)

        def to_graph():
            Windows.setCurrentIndex(9)

        task.clicked.connect(to_task)
        main_layout.addWidget(txt)
        main_layout.addLayout(l1)
        main_layout.addLayout(l2)
        self.setLayout(main_layout)


class Task(QWidget):
    def __init__(self):
        super().__init__()
        # Mostafa

        # This is an edit from Mostafa


class Timer(QWidget):
    def __init__(self):
        super().__init__()
        # Madboly


class Note(QWidget):
    def __init__(self):
        super().__init__()
        # Bessa


class Converter(QWidget):
    def __init__(self):
        super().__init__()
        # Safaa


class Translator(QWidget):
    def __init__(self):
        super().__init__()
        # Soha


class Graph(QWidget):
    def __init__(self):
        super().__init__()
        # Maram


app = QApplication(sys.argv)
Windows = QStackedWidget()
Windows.setGeometry(500, 100, 400, 600)
Windows.setStyleSheet('background-color: #00314f')
Windows.addWidget(WelcomePage())  # 0
Windows.addWidget(LoginPage())  # 1
Windows.addWidget(SignPage())  # 2
Windows.addWidget(Home())  # 3
Windows.addWidget(Task())  # 4
Windows.addWidget(Timer())  # 5
Windows.addWidget(Note())  # 6
Windows.addWidget(Converter())  # 7
Windows.addWidget(Translator())  # 8
Windows.addWidget(Graph())  # 9
Windows.show()
sys.exit(app.exec_())