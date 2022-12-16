import sqlite3
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5 import uic
from messages_box import *
from PyQt5 import QtGui


class Edit_User(QDialog):
    def __init__(self, elements):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon('../data/background/icon.png'))
        self.elements = elements
        uic.loadUi('../data/graphics/edit_user.ui', self)
        self.setFixedSize(715, 250)
        self.con = sqlite3.connect("../data/olympiads.db")
        self.label_id.setText(str(self.elements[0]))
        self.label_login.setText(str(self.elements[1]))
        self.label_password.setText(str(self.elements[2]))
        self.edit_button.clicked.connect(self.func_edit)
        self.del_button.clicked.connect(self.func_del)

    def func_edit(self):
        cur = self.con.cursor()
        request = []
        if self.edit_login.text():
            request.append(f"username = '{str(self.edit_login.text())}'")
        if self.edit_password.text():
            request.append(f"password = '{str(self.edit_password.text())}'")
        if request:
            request = ", ".join(request)
            cur.execute(f"UPDATE users SET {request} WHERE user_id = {int(self.label_id.text())}")
            self.con.commit()
            self.close()

    def func_del(self):
        valid = QMessageBox.question(
            self, '', "Действительно удалить элементы  " + self.label_login.text(), QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            cur = self.con.cursor()
            cur.execute(f"DELETE FROM users WHERE user_id = {int(self.label_id.text())}")
            cur.execute(f"DELETE FROM olympiad WHERE id_user = {int(self.label_id.text())}")
            self.con.commit()
            self.close()
