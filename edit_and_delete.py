import sqlite3
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5 import uic
from messages_box import *
from PyQt5.QtCore import QDate
import datetime as dt


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
        date = dt.date.today()
        d = QDate(date.year, date.month, date.day)
        self.dateEdit_2.setDate(d)
        self.dateEdit.setDate(d)
        self.con = sqlite3.connect("olympiads.db")
        self.label_name_2.setText(self.elements[0])
        self.label_subject_2.setText(self.elements[1])
        self.label_date_2.setText(self.elements[2])
        self.label_time_2.setText(self.elements[3])
        self.label_place_2.setText(self.elements[4])
        self.label_duration_2.setText(str(self.elements[5]))
        self.label_date_result_2.setText(self.elements[6])
        self.spin_box_duration.setMaximum(2147483647)
        self.edit_button.clicked.connect(self.func_edit)
        self.del_button.clicked.connect(self.func_del)

    def func_edit(self):
        cur = self.con.cursor()
        request = []
        if self.edit_subject.text():
            try:
                sub_id = int(list(cur.execute(f"SELECT id_subject from subjects where '{self.edit_subject.text()}' = "
                                              f"subject").fetchall())[0][0])
            except IndexError:
                subject = self.edit_subject.text()
                sub_id = list(cur.execute(f"SELECT id_subject from subjects").fetchall())[-1][0] + 1
                # sub_id = len(list(cur.execute(f"SELECT id_subject from subjects").fetchall())) + 1
                cur.execute(f"""INSERT INTO subjects(id_subject, subject) VALUES({sub_id}, '{subject}')""")
            request = [f"subject_id = '{sub_id}'"]
        if self.edit_name.text():
            request.append(f"title_ol = '{self.edit_name.text()}'")
        if self.dateEdit.date().toString("dd.MM.yyyy") != "01.01.2000":
            request.append(f"date = '{self.dateEdit.date().toString('dd.MM.yyyy')}'")
        if self.timeEdit.time().toString('hh:mm') != "0:00":
            request.append(f"time = '{self.timeEdit.time().toString('hh:mm')}'")
        if self.edit_place.text():
            request.append(f"place = '{self.edit_place.text()}'")
        if self.spin_box_duration.text():
            request.append(f"duration = {int(self.spin_box_duration.text())}")
        if self.dateEdit_2.date().toString("dd.MM.yyyy") != "01.01.2000":
            request.append(f"when_results = '{self.dateEdit_2.date().toString('dd.MM.yyyy')}'")
        if request:
            request = ", ".join(request)
            cur.execute(f"UPDATE olympiad SET {request} WHERE id_user = {self.user} and title_ol = "
                        f"'{self.label_name_2.text()}'")
            self.con.commit()
            self.close()

    def func_del(self):
        valid = QMessageBox.question(
            self, '', "Действительно удалить элементы  " + self.label_name_2.text(), QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            cur = self.con.cursor()
            cur.execute(f"DELETE FROM olympiad WHERE id_user = {self.user} and title_ol = '{self.label_name_2.text()}'")
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
        self.setFixedSize(720, 357)
        self.con = sqlite3.connect("olympiads.db")
        date = dt.date.today()
        d = QDate(date.year, date.month, date.day)
        self.dateEdit.setDate(d)
        self.combo_res.addItems(["Победитель", "Призер", "Участник"])
        self.label_name_2.setText(self.elements[0])
        self.label_date_res_2.setText(self.elements[1])
        self.label_score_2.setText(str(self.elements[2]))
        self.label_res_2.setText(self.elements[3])
        self.spin_box_score.setMaximum(2147483647)
        self.edit_button.clicked.connect(self.edit_result_func)
        self.del_button.clicked.connect(self.delete_result_func)

    def edit_result_func(self):
        cur = self.con.cursor()
        request = []
        if self.edit_name.text():
            request.append(f"title_ol = '{self.edit_name.text()}'")
        if self.dateEdit.date().toString("dd.MM.yyyy") != "01.01.2000":
            request.append(f"when_results = '{self.dateEdit.date().toString('dd.MM.yyyy')}'")
        if self.combo_res.currentText():
            request.append(f"results = '{self.combo_res.currentText()}'")
        if self.spin_box_score.text():
            request.append(f"scores = {int(self.spin_box_score.text())}")
        if request:
            request = ", ".join(request)
            cur.execute(f"UPDATE olympiad SET {request} WHERE id_user = {self.user} and title_ol = "
                        f"'{self.label_name_2.text()}'")
            self.con.commit()
            self.close()

    def delete_result_func(self):
        valid = QMessageBox.question(
            self, '', "Действительно удалить элементы  " + self.label_name_2.text(), QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            cur = self.con.cursor()
            cur.execute(f"DELETE FROM olympiad WHERE id_user = {self.user} and title_ol = '{self.label_name_2.text()}'")
            self.con.commit()
            self.close()
