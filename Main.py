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
task_cr = db.cursor()
task_cr.execute("Create table if not exists tasks(task text, email text)")
task_cr.execute("Create table if not exists pomodoro(task text, email text)")


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
                Windows.addWidget(home_page)  # 8
                Windows.setCurrentIndex(8)
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
        lb1.setAlignment(Qt.AlignCenter)

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
                # home_p.show()
                Windows.addWidget(home_p)
                Windows.setCurrentIndex(8)

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
        main_layout.setContentsMargins(30, 20, 30, 30)

        home_icon = QPushButton()
        home_icon.setIcon(QIcon("Icons/home.png"))
        home_icon.setIconSize(QSize(40, 40))

        txt1 = QLabel("Name : " + user_name)
        txt1.setObjectName("name")
        change_name = QPushButton()
        change_name.setIcon(QIcon("Icons/pencil.png"))
        change_name.setIconSize(QSize(20, 20))
        change_name.setFixedSize(35, 35)
        change_name.setObjectName("pen")

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
        change_email.setFixedSize(35, 35)
        change_email.setObjectName("pen")

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
        change_pass.setFixedSize(35, 35)
        change_pass.setObjectName("pen")

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

        hl1 = QHBoxLayout()
        hl2 = QHBoxLayout()

        vl1 = QVBoxLayout()
        vl2 = QVBoxLayout()
        vl3 = QVBoxLayout()
        vl4 = QVBoxLayout()
        vl5 = QVBoxLayout()
        vl6 = QVBoxLayout()
        task = Btn("Icons/task.png")
        l_task = QLabel("Tasks")
        l_task.setObjectName("IconLabel")
        l_task.setAlignment(Qt.AlignCenter)
        vl1.addWidget(task)
        vl1.addWidget(l_task)

        timer = Btn("Icons/timer.png")
        l_timer = QLabel("Pomodoro")
        l_timer.setObjectName("IconLabel")
        l_timer.setAlignment(Qt.AlignCenter)
        vl2.addWidget(timer)
        vl2.addWidget(l_timer)

        note = Btn("Icons/Note.png")
        l_note = QLabel("Note")
        l_note.setObjectName("IconLabel")
        l_note.setAlignment(Qt.AlignCenter)
        vl3.addWidget(note)
        vl3.addWidget(l_note)

        hl1.addLayout(vl1)
        hl1.addLayout(vl2)
        hl1.addLayout(vl3)

        converter = Btn("Icons/converter.png")
        l_converter = QLabel("Converter")
        l_converter.setObjectName("IconLabel")
        l_converter.setAlignment(Qt.AlignCenter)
        vl4.addWidget(converter)
        vl4.addWidget(l_converter)

        translator = Btn("Icons/translator.png")
        l_translator = QLabel("translator")
        l_translator.setObjectName("IconLabel")
        l_translator.setAlignment(Qt.AlignCenter)
        vl5.addWidget(translator)
        vl5.addWidget(l_translator)

        graph = Btn("Icons/graph.png")
        l_graph = QLabel("graph")
        l_graph.setObjectName("IconLabel")
        l_graph.setAlignment(Qt.AlignCenter)
        vl6.addWidget(graph)
        vl6.addWidget(l_graph)

        hl2.addLayout(vl4)
        hl2.addLayout(vl5)
        hl2.addLayout(vl6)

        btn_lay = QVBoxLayout()
        btn_lay.addLayout(hl1)
        btn_lay.addLayout(hl2)
        btn_lay.insertSpacing(1, 20)
        btn_lay.setSpacing(2)

        def to_task():
            task_page.set_email(email)
            Windows.addWidget(task_page)
            Windows.setCurrentIndex(Windows.count() - 1)

        task.clicked.connect(to_task)

        def to_timer():
            Windows.setCurrentIndex(3)

        timer.clicked.connect(to_timer)

        def to_note():
            Windows.setCurrentIndex(4)

        note.clicked.connect(to_note)

        def to_converter():
            Windows.setCurrentIndex(5)

        converter.clicked.connect(to_converter)

        def to_translator():
            Windows.setCurrentIndex(6)

        translator.clicked.connect(to_translator)

        def to_graph():
            Windows.setCurrentIndex(7)

        graph.clicked.connect(to_graph)

        main_layout.addWidget(home_icon)
        main_layout.addLayout(name_lay)
        main_layout.addLayout(email_lay)
        main_layout.addLayout(pass_lay)
        main_layout.addWidget(txt4)
        main_layout.addLayout(btn_lay)
        main_layout.setSpacing(20)
        main_layout.insertSpacing(4, 50)
        self.setLayout(main_layout)


class TaskButton(QPushButton):
    def __init__(self, task, email):
        super().__init__(f"   {task}")
        self.setIcon(QIcon("Icons/check.png"))

        def update():
            task_cr.execute(f"insert into pomodoro values ('{task}','{email}')")
            db.commit()
            task_cr.execute(f"delete from tasks where task='{task}' and email='{email}'")
            db.commit()
            task_page.ClearLayout(task_page.main_lay)
            task_page.reload_UI()

        self.clicked.connect(update)


class Task(QMainWindow):
    def __init__(self, email):
        super().__init__()
        # Mostafa
        self.email = email
        self.widget = QWidget()
        with open("Style/task.css") as file:
            style = file.read()
            self.widget.setStyleSheet(style)
        self.setStyleSheet("QScrollBar{ background-color: none }")

        self.scroll = QScrollArea()
        self.main_lay = QVBoxLayout()
        self.main_lay.setContentsMargins(20, 50, 20, 10)

        back = QPushButton(self.widget)
        back.setObjectName("back")
        back.setIcon(QIcon('Icons/previous.png'))
        back.setGeometry(20, 10, 30, 30)

        self.logo = QPushButton()
        self.logo.setIcon(QIcon("Icons/task.png"))
        self.logo.setIconSize(QSize(60, 60))
        self.logo.setObjectName("logo")

        self.title = QLabel("To-Do List")
        self.title.setObjectName("title")
        self.title.setAlignment(Qt.AlignCenter)

        self.add = QPushButton()
        self.add.setObjectName("add")
        self.add.setIcon(QIcon("Icons/add.png"))
        self.add.setIconSize(QSize(20, 20))
        self.add.setFixedWidth(40)

        note = QLabel("On clicking on a task \nit will be moved to Pomodoro technique")
        note.setObjectName("note")

        self.add_lay = QHBoxLayout()
        self.add_lay.addWidget(note)
        self.add_lay.addWidget(self.add)

        self.sub_title = QLabel("Your To-Do List")
        self.sub_title.setObjectName("sub")
        self.sub_title.setAlignment(Qt.AlignCenter)

        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.setCentralWidget(self.scroll)
        self.setCentralWidget(self.scroll)
        self.resize(300, 200)
        self.reload_UI()

        def go_back():
            Windows.setCurrentIndex(8)

        back.clicked.connect(go_back)

    def add_item(self):
        text, ok = QInputDialog().getText(self.widget, "Add new task", "New Task : ", QLineEdit.Normal)
        if ok:
            task_cr.execute(f"insert into tasks values ('{text}','{self.email}')")
            db.commit()
            self.ClearLayout(self.main_lay)
            self.reload_UI()

    def set_email(self, email):
        self.email = email
        self.add.clicked.connect(self.add_item)
        self.ClearLayout(self.main_lay)
        self.reload_UI()

    def reload_UI(self):
        self.main_lay.addWidget(self.logo)
        self.main_lay.addWidget(self.title)
        self.main_lay.addLayout(self.add_lay)
        self.main_lay.addWidget(self.sub_title)
        self.main_lay.alignment()
        task_cr.execute(f"select task from tasks where email='{self.email}'")
        tasks = task_cr.fetchall()
        if len(tasks) == 0:
            self.sub_title.setText("Your To-Do List Is Empty")
        else:
            self.sub_title.setText("Your To-Do List")

        for task in tasks:
            add_task = TaskButton(task[0], self.email)
            add_task.setObjectName("task")
            self.main_lay.addWidget(add_task)
        self.main_lay.insertSpacing(2, 40)
        self.widget.setLayout(self.main_lay)

    def ClearLayout(self, layout):
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() == self.sub_title or \
                        child.widget() == self.title or \
                        child.layout() == self.add_lay or \
                        child.widget() == self.logo:
                    continue
                if child.widget() is not None:
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    self.ClearLayout(child.layout())


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
task_page = Task("test")
Windows = QStackedWidget()
Windows.setGeometry(500, 100, 400, 600)
Windows.setStyleSheet('background-color: #00314f')
Windows.addWidget(WelcomePage())  # 0
Windows.addWidget(LoginPage())  # 1
Windows.addWidget(SignPage())  # 2
Windows.addWidget(Timer())  # 3
Windows.addWidget(Note())  # 4
Windows.addWidget(Converter())  # 5
Windows.addWidget(Translator())  # 6
Windows.addWidget(Graph())  # 7
Windows.show()
sys.exit(app.exec_())
