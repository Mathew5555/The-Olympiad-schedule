import sys
import sqlite3
import datetime as dt
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5 import uic

stylesheet_add = """
    Add_olympiad {
        background-image: url("add_back.jpg");
        background-repeat: no-repeat;
        background-position: center;
    } """


class Add_olympiad(QDialog):
    def __init__(self, user):
        super().__init__()
        self.user = user[0]
        uic.loadUi('add_ol.ui', self)
        self.setFixedSize(900, 643)
        self.setStyleSheet(stylesheet_add)
        self.con = sqlite3.connect("olympiads.db")
        self.lineEdit_2.hide()
        self.timeEdit.hide()
        self.calendarWidget.hide()
        self.spinBox.hide()
        self.spinBox.setMaximum(2147483647)
        self.comboBox.addItems(list(el[0] for el in self.con.cursor().execute(f"SELECT subject from subjects")))
        self.checkBox_5.clicked.connect(self.place)
        self.checkBox_2.clicked.connect(self.time)
        self.checkBox.clicked.connect(self.date)
        self.checkBox_6.clicked.connect(self.duration)
        self.pushButton.clicked.connect(self.run)
        self.place_val = None
        self.time_val = None
        self.date_val = None
        self.duration_val = None

    def place(self):
        if self.checkBox_5.isChecked():
            self.lineEdit_2.show()
        else:
            self.lineEdit_2.hide()

    def duration(self):
        if self.checkBox_6.isChecked():
            self.spinBox.show()
        else:
            self.spinBox.hide()

    def time(self):
        if self.checkBox_2.isChecked():
            self.timeEdit.show()
        else:
            self.timeEdit.hide()

    def date(self):
        if self.checkBox.isChecked():
            self.calendarWidget.show()
        else:
            self.calendarWidget.hide()

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

    def run(self):
        title = self.lineEdit.text()
        subject = self.comboBox.currentText()
        if not title or not subject:
            msg = QMessageBox.information(self, 'Внимание!', 'Вы не заполнили все поля.')
            return
        cur = self.con.cursor()
        temp = list(
            cur.execute(f"SELECT ol_id FROM olympiad").fetchall())
        result = list(
            cur.execute(f"SELECT title_ol FROM olympiad WHERE title_ol = '{title}'").fetchall())
        sub_id = int(
            list(cur.execute(f"SELECT id_subject from subjects where '{subject}' = subject").fetchall())[0][0])
        zapros = ["ol_id", "title_ol", "subject_id"]
        values = [f"{len(temp) + 1}", f"'{title}'", f"{sub_id}"]
        if self.checkBox.isChecked():
            date = self.calendarWidget.selectedDate().toString("yyyy.MM.dd")
            zapros.append("date")
            values.append(f"'{date}'")
            self.date = dt.date(int(date.split(".")[0]), int(date.split(".")[1]), int(date.split(".")[2]))
        if self.checkBox_2.isChecked():
            values.append(f"'{self.timeEdit.time().toString('hh.mm')}'")
            zapros.append("time")
            self.time = self.timeEdit.time().toPyTime()
        if self.checkBox_5.isChecked():
            zapros.append("place")
            values.append(f"'{self.lineEdit_2.text()}'")
        if self.checkBox_6.isChecked():
            zapros.append("duration")
            values.append(f"{int(self.spinBox.text())}")
        if not result:
            self.info_message_box('Успешно!', f'Добавлена олимпиада {title}')
            zapros.append("id_user")
            values.append(f'{self.user}')
            zapros = ", ".join(zapros)
            values = ", ".join(values)
            cur.execute(f"""INSERT INTO olympiad({zapros}) VALUES({values})""")
            self.close()
            self.con.commit()
            self.con.close()
        else:
            self.warning_message_box('Внимание!', f'Уже есть такая олимпиада!')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Add_olympiad(1)
    ex.show()
    sys.exit(app.exec_())
