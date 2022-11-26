import sys
import csv
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView, QFileDialog, QMessageBox, QDialog
from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import Qt
import welcome_window as ww
import add_window as aw

stylesheet_main = """
    MainWindow {
        background-image: url("background_welcome_window.jpg");
        background-repeat: no-repeat;
        background-position: center;
    } """


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui', self)
        self.setFixedSize(1200, 800)
        self.setStyleSheet(stylesheet_main)
        self.user_name.setAlignment(Qt.AlignRight)
        self.find_Edit.textChanged.connect(self.run)
        self.filter.addItems(["Без фильтра", "Название", "Предмет", "Дата"])
        con = sqlite3.connect("olympiads.db")
        self.cur = con.cursor()
        self.filter.currentIndexChanged.connect(self.run)
        self.olympiad_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.add.clicked.connect(self.add_ol)
        self.user_name.setText(ww.USER_ID[1])
        self.add_2.clicked.connect(self.run)
        self.download.clicked.connect(self.downl)
        self.upload.clicked.connect(self.upl)
        self.run()

    def warning_message_box(self, title, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setDetailedText("Возможные проблемы:\n- Неверный формат данных(продолжительность задана строкой, "
                                "а не числом и т.п.\n- В строке меньше 6 строк.")
        msg_box.exec_()

    def downl(self):
        fname = QFileDialog.getOpenFileName(self, 'Выбрать файл', '', 'Файл (*.csv)')[0]
        try:
            with open(fname, encoding="utf8") as csvfile:
                reader = csv.reader(csvfile, delimiter=';', quotechar='"')
                for index, row in enumerate(reader):
                    print(row)
                    temp = list(
                        self.cur.execute(f"SELECT ol_id FROM olympiad where id_user = {ww.USER_ID[0]}").fetchall())
                    result = list(
                        self.cur.execute(f"SELECT title_ol FROM olympiad WHERE title_ol = '{row[0]}' and id_user "
                                         f"= {ww.USER_ID[0]}").fetchall())
                    try:
                        sub_id = int(list(self.cur.execute(f"SELECT id_subject from subjects where '{row[1]}' = "
                                                           f"subject").fetchall())[0][0])
                    except IndexError:
                        subject = row[1]
                        sub_id = len(list(self.cur.execute(f"SELECT id_subject from subjects").fetchall())) + 1
                        self.cur.execute(f"""INSERT INTO subjects(id_subject, subject) VALUES({sub_id}, '{subject}')""")
                    zapros = ["ol_id", "title_ol", "subject_id"]
                    values = [f"{len(temp) + 1}", f"'{row[0]}'", f"{sub_id}"]
                    if row[2] != " ":
                        zapros.append("date")
                        values.append(f"'{row[2]}'")
                    if row[3] != " ":
                        values.append(f"'{row[3]}'")
                        zapros.append("time")
                    if row[4] != " ":
                        zapros.append("place")
                        values.append(f"'{row[4]}'")
                    if row[5] != " " and row[5]:
                        zapros.append("duration")
                        values.append(f"{int(row[5])}")
                    if not result:
                        zapros.append("id_user")
                        values.append(f'{ww.USER_ID[0]}')
                        zapros = ", ".join(zapros)
                        values = ", ".join(values)
                        self.cur.execute(f"""INSERT INTO olympiad({zapros}) VALUES({values})""")
        except Exception as e:
            if e.__class__.__name__ != "FileNotFoundError":
                self.warning_message_box("Внимание!", "Неверный формат ввода файла")

    def upl(self):
        self.upload_win = Upload_Window()
        self.upload_win.show()

    def run(self):
        text = self.find_Edit.text().lower()
        self.olympiad_table.setColumnCount(4)
        self.olympiad_table.setHorizontalHeaderLabels(["Название", "Предмет", "Дата", "Место"])
        self.olympiad_table.setRowCount(0)
        filter_text = self.filter.currentText()
        if filter_text == "Без фильтра":
            result = self.cur.execute("select olympiad.title_ol, subjects.subject, olympiad.date, olympiad.place FROM "
                                      "olympiad LEFT JOIN subjects on subjects.id_subject = olympiad.subject_id where "
                                      f"title_ol LIKE '%{text}%' and id_user = {ww.USER_ID[0]}").fetchall()
        elif filter_text == "Название":
            result = self.cur.execute("select olympiad.title_ol, subjects.subject, olympiad.date, olympiad.place FROM "
                                      "olympiad LEFT JOIN subjects on subjects.id_subject = olympiad.subject_id where "
                                      f"title_ol LIKE '%{text}%' and id_user = {ww.USER_ID[0]} ORDER BY "
                                      f"olympiad.title_ol").fetchall()
        elif filter_text == "Предмет":
            result = self.cur.execute("select olympiad.title_ol, subjects.subject, olympiad.date, olympiad.place FROM "
                                      "olympiad LEFT JOIN subjects on subjects.id_subject = olympiad.subject_id where "
                                      f"title_ol LIKE '%{text}%' and id_user = {ww.USER_ID[0]} ORDER BY "
                                      f"subjects.subject").fetchall()
        else:
            result = self.cur.execute("select olympiad.title_ol, subjects.subject, olympiad.date, olympiad.place FROM "
                                      "olympiad LEFT JOIN subjects on subjects.id_subject = olympiad.subject_id where "
                                      f"title_ol LIKE '%{text}%' and id_user = {ww.USER_ID[0]}").fetchall()
            result = sorted(filter(lambda x: x[2], result), key=lambda x: (int(x[2].split(".")[2]),
                                                                           int(x[2].split(".")[1]),
                                                                           int(x[2].split(".")[0])))
        for i, row in enumerate(result):
            self.olympiad_table.setRowCount(self.olympiad_table.rowCount() + 1)
            for j, el in enumerate(row):
                if not el:
                    self.olympiad_table.setItem(i, j, QTableWidgetItem("Нет данных"))
                    continue
                self.olympiad_table.setItem(i, j, QTableWidgetItem(str(el)))
        self.olympiad_table.resizeColumnsToContents()
        column_head = self.olympiad_table.horizontalHeader()
        column_head.setSectionResizeMode(0, QHeaderView.Stretch)

    def add_ol(self):
        self.add_window = aw.Add_olympiad(ww.USER_ID)
        self.add_window.show()

    def keyPressEvent(self, event):
        if int(event.modifiers()) == Qt.ControlModifier:
            if event.key() == Qt.Key_S:
                self.upload_win = Upload_Window()
                self.upload_win.show()
            elif event.key() == Qt.Key_V or event.key() == Qt.Key_X:
                self.downl()


class Upload_Window(QDialog):
    def __init__(self):
        super(Upload_Window, self).__init__()
        uic.loadUi('upload_dialog.ui', self)
        con = sqlite3.connect("olympiads.db")
        self.cur = con.cursor()
        self.pushButton.clicked.connect(self.run)
        self.radioButton.nextCheckState()
        # self.radioButton.toggled.connect(self.run)
        # self.radioButton_3.toggled.connect(self.run)

    def run(self):
        result = self.cur.execute(
            "select olympiad.title_ol, subjects.subject, olympiad.date, olympiad.time, olympiad.place, "
            "olympiad.duration FROM olympiad "
            f"LEFT JOIN subjects on subjects.id_subject = olympiad.subject_id  where id_user = "
            f"{ww.USER_ID[0]}").fetchall()
        if self.radioButton.isChecked():
            with open('olymp.txt', 'wt', encoding="UTF-8") as f:
                for el in result:
                    f.write(f"Название: {el[0]}\nПредмет: {el[1]}\n")
                    if el[2]:
                        f.write(f"Дата: {el[2]}\n")
                    else:
                        f.write("Дата: Нет данных\n")
                    if el[3]:
                        f.write(f"Время: {el[3]}\n")
                    else:
                        f.write("Время: Нет данных\n")
                    if el[4]:
                        f.write(f"Место: {el[4]}\n")
                    else:
                        f.write("Место: Нет данных\n")
                    if el[5]:
                        f.write(f"Продолжительность: {el[5]}\n")
                    else:
                        f.write("Продолжительность: Нет данных\n")
                    f.write("----------------------------------------------------------\n")
                    self.close()
        else:
            with open('olymp.csv', 'w', newline='', encoding="utf8") as csvfile:
                writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(["Название", "Предмет", "Дата", "Время", "Место", "Длительность"])
                for el in result:
                    res = [el[0], el[1]]
                    for item in el[2::]:
                        if not item:
                            res.append("Нет данных")
                        else:
                            res.append(item)
                    self.close()
                    writer.writerow(res)


class Welcome(ww.Welcome):
    def __init__(self):
        super(Welcome, self).__init__()

    def closeEvent(self, event):
        self.main_window = MainWindow()
        if ww.CLOSED_FLAG:
            self.main_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # w = Welcome()
    # w.show()
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
