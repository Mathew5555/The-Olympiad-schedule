import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit
from PyQt5 import uic
from stylesheets import *
from exceptions import *

CLOSED_FLAG = 0
USER_ID = (0, "")


class Reg_Dialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('reg.ui', self)
        self.setFixedSize(700, 500)
        self.setStyleSheet(stylesheet_reg)
        self.con = sqlite3.connect("olympiads.db")
        self.btn_enter_reg.clicked.connect(self.reg_check)
        self.password_reg.setEchoMode(QLineEdit.EchoMode.Password)

    def reg_check(self):
        global USER_ID
        username = self.user_reg.text()
        password = self.password_reg.text()
        if not username or not password:
            msg = QMessageBox.information(self, 'Внимание!', 'Вы не заполнили все поля.')
            return
        cur = self.con.cursor()
        result = list(
            cur.execute(f"SELECT username FROM users WHERE username = '{username}'").fetchall())
        try:
            if not result:
                info_message_box('Успешно!', f'Регистрация прошла под логином {username}')
                temp = list(
                    cur.execute(f"SELECT username FROM users").fetchall())
                cur.execute(f"""INSERT INTO users(user_id, username, password) VALUES({len(temp) + 1}, '{username}', 
                '{password}')""")
                self.close()
                self.con.commit()
                self.con.close()
            else:
                raise User_Error
        except Exception as e:
            warning_message_box(e, "Ошибка")


class Login_Dialog(QDialog):
    def __init__(self, obj):
        super().__init__()
        self.obj = obj
        uic.loadUi('log.ui', self)
        self.setFixedSize(700, 500)
        self.setStyleSheet(stylesheet_log)
        self.con = sqlite3.connect("olympiads.db")
        self.btn_enter_log.clicked.connect(self.login_check)

    def login_check(self):
        global CLOSED_FLAG, USER_ID
        username = self.user.text()
        password = self.password.text()
        if not username or not password:
            msg = QMessageBox.information(self, 'Внимание!', 'Вы не заполнили все поля.')
            return
        cur = self.con.cursor()
        result = list(cur.execute(f"SELECT user_id, username, password FROM users WHERE username = '{username}' and "
                                  f"password = '{password}'").fetchall())
        if result:
            CLOSED_FLAG = 1
            USER_ID = (result[0][0], result[0][1])
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
    try:
        app = QApplication(sys.argv)
        ex = Welcome()
        ex.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(e)
