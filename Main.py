import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sqlite3
import re
from PyQt5.QtCore import *

db = sqlite3.connect('Data.db')
cr = db.cursor()
cr.execute("Create table if not exists user(name text, email text, password text, ID int auto_increment primary key)")


class WelcomePage(QWidget):
    def __init__(self):
        super(WelcomePage, self).__init__()

        with open('style/welcome.css') as file:
            style = file.read()
            self.setStyleSheet(style)

        self.setWindowTitle('Productivity Club')
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(50, 0, 50, 50)

        welcome_text = QLabel("Welcome To")
        welcome_text.setObjectName('wel')

        txt2 = QLabel("Productivity Club")
        txt2.setObjectName("txt2")

        welcome_text.setAlignment(Qt.AlignCenter)
        txt2.setAlignment(Qt.AlignCenter)

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
        main_layout.setContentsMargins(50, 50, 50, 50)

        back = QPushButton(self)
        back.setObjectName("back")
        back.setIcon(QIcon('Icons/previous.png'))
        back.setGeometry(20, 10, 30, 30)

        lb1 = QLabel("Login")
        lb1.setObjectName("lb1")
        lb2 = QLabel("Enter Your Email And Password")
        lb2.setObjectName("lb2")

        lb1.setAlignment(Qt.AlignCenter)
        lb2.setAlignment(Qt.AlignCenter)

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
        main_layout.insertSpacing(1, 50)
        main_layout.insertSpacing(2, 10)

        def go_back():
            Windows.setCurrentIndex(0)

        def check_input():
            cr.execute(f"select name , email , password from user "
                       f"where email='{email_field.text()}' and password='{password_field.text()}'")
            result = cr.fetchall()
            if email_field.text() == "" or password_field == "":
                QMessageBox.warning(self, "warning", "You can't leave any input field empty", QMessageBox.Ok)
            elif len(result) >= 1:
                # SET USER DATA
                home_page = Home(result[0][0], email_field.text(), password_field.text())
                Windows.addWidget(home_page)  # 9
                Windows.setCurrentIndex(9)
            else:
                QMessageBox.warning(self, "warning", "Email and Password are incorrect", QMessageBox.Ok)

        back.clicked.connect(go_back)
        login_btn.clicked.connect(check_input)
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
        back.setIcon(QIcon('Icons/previous.png'))
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
                home_p = Home(name.text(), email_field.text(), password_field.text())
                home_p.show()
                Windows.addWidget(home_p)
                Windows.setCurrentIndex(9)

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
        with open("style/btn.css") as file:
            style = file.read()
            self.setStyleSheet(style)


class Home(QWidget):
    def __init__(self, user_name, email, password):
        super().__init__()

        with open("style/home.css") as file:
            style = file.read()
            self.setStyleSheet(style)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 20, 50, 50)

        home_icon = QPushButton()
        home_icon.setIcon(QIcon("Icons/home.png"))
        home_icon.setIconSize(QSize(40, 40))

        txt1 = QLabel("Name : " + user_name)
        txt1.setObjectName("name")
        change_name = QPushButton()
        change_name.setIcon(QIcon("Icons/pencil.png"))
        change_name.setIconSize(QSize(20, 20))

        def c_name():
            text, ok = QInputDialog().getText(self, "Change Your Name", "User name:", QLineEdit.Normal)
            if ok:
                cr.execute(f"update user set name='{text}' where email='{email}' and password='{password}'")
                db.commit()
                txt1.setText("Name : " + text)

        change_name.clicked.connect(c_name)

        name_lay = QHBoxLayout()
        name_lay.addWidget(txt1)
        name_lay.addWidget(change_name)

        txt2 = QLabel("Email : " + email)
        txt2.setObjectName("name")
        change_email = QPushButton()
        change_email.setIcon(QIcon("Icons/pencil.png"))
        change_email.setIconSize(QSize(20, 20))

        def c_email():
            text, ok = QInputDialog().getText(self, "Change Your Email", "Email :", QLineEdit.Normal)
            if ok:
                reg = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
                is_email = re.fullmatch(reg, text)
                if is_email:
                    cr.execute("select email from user")
                    emails = cr.fetchall()
                    if (text,) in emails:
                        QMessageBox.warning(self, "warning", "This Email is already used, Please use another one",
                                            QMessageBox.Ok)
                    else:
                        cr.execute(f"update user set email='{text}' where email='{email}' and password='{password}'")
                        db.commit()
                        txt2.setText("Email : " + text)
                else:
                    QMessageBox.warning(self, "warning", "Please enter a valid email \nSuch as : Mostafa_12@gmail.com ",
                                        QMessageBox.Ok)

        change_email.clicked.connect(c_email)

        email_lay = QHBoxLayout()
        email_lay.addWidget(txt2)
        email_lay.addWidget(change_email)

        txt3 = QLabel("Password : " + len(password) * "*")
        txt3.setObjectName("name")
        change_pass = QPushButton()
        change_pass.setIcon(QIcon("Icons/pencil.png"))
        change_pass.setIconSize(QSize(20, 20))

        def c_pass():
            text, ok = QInputDialog().getText(self, "Change Your Name", "User name:", QLineEdit.Normal)
            if ok:
                cr.execute(f"update user set password='{text}' where email='{email}' ")
                db.commit()
                txt3.setText("Password : " + len(text) * "*")
                password = text

        change_pass.clicked.connect(c_pass)

        pass_lay = QHBoxLayout()
        pass_lay.addWidget(txt3)
        pass_lay.addWidget(change_pass)

        txt4 = QLabel("Our Features")
        txt4.setObjectName("title")
        txt4.setAlignment(Qt.AlignCenter)

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

        btn_lay = QVBoxLayout()
        btn_lay.addLayout(l1)
        btn_lay.addLayout(l2)
        btn_lay.setSpacing(10)

        def to_task():
            Windows.setCurrentIndex(3)

        task.clicked.connect(to_task)

        def to_timer():
            Windows.setCurrentIndex(4)

        timer.clicked.connect(to_timer)

        def to_note():
            Windows.setCurrentIndex(5)

        note.clicked.connect(to_note)

        def to_converter():
            Windows.setCurrentIndex(6)

        converter.clicked.connect(to_converter)

        def to_translator():
            Windows.setCurrentIndex(7)

        translator.clicked.connect(to_translator)

        def to_graph():
            Windows.setCurrentIndex(8)

        graph.clicked.connect(to_graph)

        main_layout.addWidget(home_icon)
        main_layout.addLayout(name_lay)
        main_layout.addLayout(email_lay)
        main_layout.addLayout(pass_lay)
        main_layout.addWidget(txt4)
        main_layout.addLayout(btn_lay)
        main_layout.setSpacing(30)
        main_layout.insertSpacing(4, 50)
        self.setLayout(main_layout)


class Task(QWidget):
    def __init__(self):
        super().__init__()
        # Mostafa


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
Windows.addWidget(Task())  # 3
Windows.addWidget(Timer())  # 4
Windows.addWidget(Note())  # 5
Windows.addWidget(Converter())  # 6
Windows.addWidget(Translator())  # 7
Windows.addWidget(Graph())  # 8
Windows.show()
sys.exit(app.exec_())
