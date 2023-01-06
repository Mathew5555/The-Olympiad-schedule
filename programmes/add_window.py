import sys
import sqlite3
import datetime as dt
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5 import uic
from PyQt5.QtCore import QDate
from exceptions import *
from messages_box import *
from PyQt5 import QtGui

stylesheet_add = """
    Add_olympiad {
        background-image: url("../data/background/add_back.jpg");
        background-repeat: no-repeat;
        background-position: center;
    } """


class Add_olympiad(QDialog):
    def __init__(self, user):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon('../data/background/icon.png'))
        self.user = user[0]
        uic.loadUi("../data/graphics/add_ol.ui", self)
        self.setFixedSize(900, 643)
        self.setStyleSheet(stylesheet_add)
        self.con = sqlite3.connect("../data/olympiads.db")
        self.edit_place.hide()
        self.timeEdit.hide()
        self.calendarWidget.hide()
        self.spinbox_duration.hide()
        self.dateEdit_2.hide()
        date = dt.date.today()
        d = QDate(date.year, date.month, date.day)
        self.dateEdit_2.setDate(d)
        self.spinbox_duration.setMaximum(2147483647)
        self.checkBox_place.clicked.connect(self.place)
        self.checkBox_time.clicked.connect(self.time)
        self.checkBox_date.clicked.connect(self.date)
        self.checkBox_duration.clicked.connect(self.duration)
        self.pushButton.clicked.connect(self.new_olympiad)
        self.checkBox_dateres.clicked.connect(self.date_res)
        self.place_val = None
        self.time_val = None
        self.date_val = None
        self.duration_val = None
        self.date_result = None

    def place(self):
        if self.checkBox_place.isChecked():
            self.edit_place.show()
        else:
            self.edit_place.hide()

    def date_res(self):
        if self.checkBox_dateres.isChecked():
            self.dateEdit_2.show()
        else:
            self.dateEdit_2.hide()

    def duration(self):
        if self.checkBox_duration.isChecked():
            self.spinbox_duration.show()
        else:
            self.spinbox_duration.hide()

    def time(self):
        if self.checkBox_time.isChecked():
            self.timeEdit.show()
        else:
            self.timeEdit.hide()

    def date(self):
        if self.checkBox_date.isChecked():
            self.calendarWidget.show()
        else:
            self.calendarWidget.hide()

    def new_olympiad(self):
        title = self.edit_title.text()
        subject = self.edit_subject.text()
        try:
            if not title or not subject:
                raise Space_Olympiad_Error
            cur = self.con.cursor()
            new_olymp_id = list(cur.execute(f"SELECT ol_id FROM olympiad").fetchall())[-1][0] + 1
            result = list(cur.execute(f"SELECT title_ol FROM olympiad WHERE title_ol = '{title}'").fetchall())
            try:
                sub_id = int(list(cur.execute(f"SELECT id_subject from subjects where '{self.edit_subject.text()}' = "
                                              f"subject").fetchall())[0][0])
            except IndexError:
                sub_id = list(cur.execute(f"SELECT id_subject from subjects").fetchall())[-1][0] + 1
                cur.execute(f"""INSERT INTO subjects(id_subject, subject) VALUES({sub_id}, '{subject}')""")
            request = ["ol_id", "title_ol", "subject_id"]
            values = [f"{new_olymp_id}", f"'{title}'", f"{sub_id}"]
            if self.checkBox_duration.isChecked():
                date = self.calendarWidget.selectedDate().toString("dd.MM.yyyy")
                request.append("date")
                values.append(f"'{date}'")
            if self.checkBox_time.isChecked():
                values.append(f"'{self.timeEdit.time().toString('hh:mm')}'")
                request.append("time")
            if self.checkBox_place.isChecked():
                request.append("place")
                values.append(f"'{self.edit_place.text()}'")
            if self.checkBox_duration.isChecked():
                request.append("duration")
                values.append(f"{int(self.spinbox_duration.text())}")
            if self.checkBox_dateres.isChecked():
                request.append("when_results")
                values.append(f"'{self.dateEdit_2.date().toString('dd.MM.yy')}'")
            if not result:
                msg = QMessageBox.information(self, 'Успешно!', f'Добавлена олимпиада {title}', QMessageBox.Ok)
                request.append("id_user")
                values.append(f'{self.user}')
                request = ", ".join(request)
                values = ", ".join(values)
                cur.execute(f"""INSERT INTO olympiad({request}) VALUES({values})""")
                self.close()
                self.con.commit()
                self.con.close()
            else:
                raise Olymp_Error
        except Space_Olympiad_Error as e:
            info_message_box(e, "Обратите внимание!")
        except Olymp_Error as e:
            warning_message_box(e, "Внимание!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Add_olympiad((0, ""))
    ex.show()
    sys.exit(app.exec_())
