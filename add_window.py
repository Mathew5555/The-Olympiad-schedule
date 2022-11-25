import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5 import uic

stylesheet_add = """
    Add_olympiad {
        background-image: url("add_back.jpg");
        background-repeat: no-repeat;
        background-position: center;
    } """

CLOSED_FLAG = 0


class Add_olympiad(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('add_ol.ui', self)
        self.setFixedSize(900, 643)
        self.setStyleSheet(stylesheet_add)
        self.con = sqlite3.connect("olympiads.db")
        self.lineEdit_2.hide()
        self.timeEdit.hide()
        self.calendarWidget.hide()
    #     self.btn_enter_reg.clicked.connect(self.reg_check)
    #
    # def info_message_box(self, title, message):
    #     msg_box = QMessageBox()
    #     msg_box.setIcon(QMessageBox.Information)
    #     msg_box.setWindowTitle(title)
    #     msg_box.setText(message)
    #     msg_box.setStandardButtons(QMessageBox.Ok)
    #     msg_box.exec_()
    #
    # def warning_message_box(self, title, message):
    #     msg_box = QMessageBox()
    #     msg_box.setIcon(QMessageBox.Critical)
    #     msg_box.setWindowTitle(title)
    #     msg_box.setText(message)
    #     msg_box.setStandardButtons(QMessageBox.Ok)
    #     msg_box.exec_()
    #
    # def reg_check(self):
    #     username = self.user_reg.text()
    #     password = self.password_reg.text()
    #     if not username or not password:
    #         msg = QMessageBox.information(self, 'Внимание!', 'Вы не заполнили все поля.')
    #         return
    #     cur = self.con.cursor()
    #     result = list(
    #         cur.execute(f"SELECT username FROM users WHERE username = '{username}'").fetchall())
    #     print(2)
    #     if not result:
    #         self.info_message_box('Успешно!', f'Регистрация прошла под логином {username}')
    #         temp = list(
    #             cur.execute(f"SELECT username FROM users").fetchall())
    #         cur.execute(f"""INSERT INTO users(user_id, username, password) VALUES({len(temp) + 1}, '{username}',
    #         '{password}')""")
    #         self.close()
    #         print(1)
    #         self.con.commit()
    #         self.con.close()
    #     else:
    #         self.warning_message_box('Внимание!', f'Уже есть пользователь с таким именем')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Add_olympiad()
    ex.show()
    sys.exit(app.exec_())
