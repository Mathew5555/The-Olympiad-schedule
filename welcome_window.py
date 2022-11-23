import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox
from PyQt5 import uic

stylesheet_welcome = """
    Welcome {
        background-image: url("background_welcome_window.jpg");
        background-repeat: no-repeat;
        background-position: center;
    } """
stylesheet_log = """
    Login_Dialog {
        background-image: url("background_log_reg.jpg");
        background-repeat: no-repeat;
        background-position: center;
    } """

stylesheet_reg = """
    Reg_Dialog {
        background-image: url("background_log_reg.jpg");
        background-repeat: no-repeat;
        background-position: center;
    } """


class Reg_Dialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('reg.ui', self)
        self.setFixedSize(700, 500)
        self.setStyleSheet(stylesheet_reg)
        self.con = sqlite3.connect("olympiads.db")
        self.btn_enter_reg.clicked.connect(self.reg_check)

    def info_message_box(self, title, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def warning_message_box(self, title, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def reg_check(self):
        username = self.user_reg.text()
        password = self.password_reg.text()
        if not username or not password:
            msg = QMessageBox.information(self, 'Внимание!', 'Вы не заполнили все поля.')
            return
        cur = self.con.cursor()
        result = list(
            cur.execute(f"SELECT username FROM users WHERE username = '{username}'").fetchall())
        print(2)
        if not result:
            self.info_message_box('Успешно!', f'Регистрация прошла под логином {username}')
            temp = list(
                cur.execute(f"SELECT username FROM users").fetchall())
            cur.execute(f"""INSERT INTO users(user_id, username, password) VALUES({len(temp) + 1}, '{username}', 
            '{password}')""")
            self.close()
            print(1)
            self.con.commit()
            self.con.close()
        else:
            self.warning_message_box('Внимание!', f'Уже есть пользователь с таким именем')


class Login_Dialog(QDialog):
    def __init__(self, obj):
        super().__init__()
        self.obj = obj
        uic.loadUi('log.ui', self)
        self.setFixedSize(700, 500)
        self.setStyleSheet(stylesheet_log)
        self.con = sqlite3.connect("olympiads.db")
        self.btn_enter_log.clicked.connect(self.login_check)

    def warning_message_box(self, title, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def login_check(self):
        username = self.user.text()
        password = self.password.text()
        if not username or not password:
            msg = QMessageBox.information(self, 'Внимание!', 'Вы не заполнили все поля.')
            return
        cur = self.con.cursor()
        result = list(cur.execute(f"SELECT username, password FROM users WHERE username = '{username}' and "
                                  f"password = '{password}'").fetchall())
        if result:
            self.close()
            self.con.close()
            self.obj.close()
        else:
            self.warning_message_box('Внимание!', 'Неправильное имя пользователя или пароль.\nПовторите попытку')


class Welcome(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('welcome_window.ui', self)
        self.setStyleSheet(stylesheet_welcome)
        self.setFixedSize(1200, 800)
        self.btn_enter.clicked.connect(self.login)
        self.btn_reg.clicked.connect(self.reg)

    def login(self):
        self.log_in = Login_Dialog(self)
        self.log_in.show()

    def reg(self):
        self.sign_up = Reg_Dialog()
        self.sign_up.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Welcome()
    ex.show()
    sys.exit(app.exec_())
