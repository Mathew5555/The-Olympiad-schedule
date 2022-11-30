import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5 import uic
from messages_box import *
from exceptions import *


class Edit_Ol(QDialog):
    def __init__(self, user, elements):
        super().__init__()
        self.user = user[0]
        self.elements = []
        for el in elements:
            if not el:
                self.elements.append("Нет данных")
            else:
                self.elements.append(el)
        uic.loadUi('edit_and_delete.ui', self)
        self.setFixedSize(793, 491)
        self.con = sqlite3.connect("olympiads.db")
        self.label_11.setText(self.elements[0])
        self.label_12.setText(self.elements[1])
        self.label_13.setText(self.elements[2])
        self.label_14.setText(self.elements[3])
        self.label_15.setText(self.elements[4])
        self.label_16.setText(str(self.elements[5]))
        self.label_17.setText(self.elements[6])
        self.spinBox.setMaximum(2147483647)
        self.pushButton_2.clicked.connect(self.run)
        self.pushButton.clicked.connect(self.run_2)

    def run(self):
        cur = self.con.cursor()
        zapros = []
        if self.lineEdit_3.text():
            try:
                sub_id = int(list(cur.execute(f"SELECT id_subject from subjects where '{self.lineEdit_3.text()}' = "
                                              f"subject").fetchall())[0][0])
            except IndexError:
                subject = self.lineEdit_3.text()
                sub_id = len(list(cur.execute(f"SELECT id_subject from subjects").fetchall())) + 1
                cur.execute(f"""INSERT INTO subjects(id_subject, subject) VALUES({sub_id}, '{subject}')""")
            zapros = [f"subject_id = '{sub_id}'"]
        if self.lineEdit.text():
            zapros.append(f"title_ol = '{self.lineEdit.text()}'")
        if self.dateEdit.date().toString("dd.MM.yyyy") != "01.01.2000":
            zapros.append(f"date = '{self.dateEdit.date().toString('dd.MM.yyyy')}'")
        if self.timeEdit.time().toString('hh:mm') != "0:00":
            zapros.append(f"time = '{self.timeEdit.time().toString('hh:mm')}'")
        if self.lineEdit_2.text():
            zapros.append(f"place = '{self.lineEdit_2.text()}'")
        if self.spinBox.text():
            zapros.append(f"duration = {int(self.spinBox.text())}")
        if self.dateEdit_2.date().toString("dd.MM.yyyy") != "01.01.2000":
            zapros.append(f"when_results = '{self.dateEdit_2.date().toString('dd.MM.yyyy')}'")
        if zapros:
            zapros = ", ".join(zapros)
            print(zapros)
            cur.execute(
                f"UPDATE olympiad SET {zapros} WHERE id_user = {self.user} and title_ol = '{self.label_11.text()}'")
            self.con.commit()
            self.close()

    def run_2(self):
        valid = QMessageBox.question(
            self, '', "Действительно удалить элементы  " + self.label_11.text(), QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            cur = self.con.cursor()
            cur.execute(f"DELETE FROM olympiad WHERE id_user = {self.user} and title_ol = '{self.label_11.text()}'")
            self.con.commit()
            self.close()


class Edit_Res(QDialog):
    def __init__(self, user, elements):
        super().__init__()
        self.user = user[0]
        self.elements = []
        for el in elements:
            if not el:
                self.elements.append("Нет данных")
            else:
                self.elements.append(el)
        uic.loadUi('edit_res.ui', self)
        self.setFixedSize(720, 484)
        self.con = sqlite3.connect("olympiads.db")
        self.label_11.setText(self.elements[0])
        self.label_13.setText(self.elements[1])
        self.label_14.setText(str(self.elements[2]))
        self.label_15.setText(self.elements[3])
        self.spinBox.setMaximum(2147483647)
        self.pushButton_2.clicked.connect(self.run)
        self.pushButton.clicked.connect(self.run_2)

    def run(self):
        cur = self.con.cursor()
        zapros = []
        if self.lineEdit.text():
            zapros.append(f"title_ol = '{self.lineEdit.text()}'")
        if self.dateEdit.date().toString("dd.MM.yyyy") != "01.01.2000":
            zapros.append(f"when_results = '{self.dateEdit.date().toString('dd.MM.yyyy')}'")
        if self.lineEdit_2.text():
            zapros.append(f"results = '{self.lineEdit_2.text()}'")
        if self.spinBox.text():
            zapros.append(f"scores = {int(self.spinBox.text())}")
        if zapros:
            zapros = ", ".join(zapros)
            cur.execute(
                f"UPDATE olympiad SET {zapros} WHERE id_user = {self.user} and title_ol = '{self.label_11.text()}'")
            self.con.commit()
            self.close()

    def run_2(self):
        valid = QMessageBox.question(
            self, '', "Действительно удалить элементы  " + self.label_11.text(), QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            cur = self.con.cursor()
            cur.execute(f"DELETE FROM olympiad WHERE id_user = {self.user} and title_ol = '{self.label_11.text()}'")
            self.con.commit()
            self.close()
