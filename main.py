import sys
import datetime as dt
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView, QFileDialog, QMessageBox, QDialog
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QColor
import welcome_window as ww
from add_window import *
from stylesheets import *
from edit_and_delete import *
from upload import *
from exceptions import *
from edit_user import *


def translate(*args):
    res = []
    for el in args[0]:
        if el[-1] == "Победитель":
            res.append(list(el[:-1]) + [1])
        elif el[-1] == "Призер" or el[-1] == "Призёр":
            res.append(list(el[:-1]) + [2])
        elif el[-1] == "Участник":
            res.append(list(el[:-1]) + [3])
        else:
            res.append(list(el[:-1]) + [4])
    return res


def retranslate(args):
    res = []
    for el in args:
        if el[-1] == 1:
            res.append(el[:-1] + ["Победитель"])
        elif el[-1] == 2:
            res.append(el[:-1] + ["Призер"])
        elif el[-1] == 3:
            res.append(el[:-1] + ["Участник"])
        else:
            res.append(el[:-1] + ["Нет данных"])
    return res


class Main_Table_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        con = sqlite3.connect("olympiads.db")
        self.cur = con.cursor()
        if ww.USER_ID[0] == 0:
            uic.loadUi('admin.ui', self)
            self.pixmap_3 = QPixmap('admin_photo.png')
            self.label_photo_admin.setPixmap(self.pixmap_3)
            self.olympiad_table_3.cellDoubleClicked.connect(self.edit_users)
            self.olympiad_table_3.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.find_Edit_3.textChanged.connect(self.admin_table_run)
            self.upload_2.clicked.connect(self.upl_users)
            self.admin_table_run()
        else:
            uic.loadUi('main_window.ui', self)
        self.setFixedSize(1200, 800)
        self.setStyleSheet(stylesheet_main)
        self.user_name.setAlignment(Qt.AlignRight)
        self.find_Edit.textChanged.connect(self.olympiad_table_run)
        self.find_Edit_2.textChanged.connect(self.results_table_run)
        self.filter.addItems(["Без фильтра", "Название", "Предмет", "Дата", "Дата результатов"])
        self.filter_2.addItems(["Без фильтра", "Название", "Предмет", "Дата результатов", "Баллы", "Результаты"])
        self.filter.currentIndexChanged.connect(self.olympiad_table_run)
        self.olympiad_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.olympiad_table_2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.olympiad_table.cellDoubleClicked.connect(self.edit_olympiad)
        self.olympiad_table_2.cellDoubleClicked.connect(self.edit_results)
        self.add.clicked.connect(self.add_ol)
        self.user_name.setText(ww.USER_ID[1])
        self.update_button.clicked.connect(self.update_func)
        self.filter_2.currentIndexChanged.connect(self.results_table_run)
        self.download.clicked.connect(self.downl)
        self.upload.clicked.connect(self.upl)
        self.pixmap = QPixmap('cup.png')
        self.label_2.setPixmap(self.pixmap)
        self.pixmap_2 = QPixmap('main_photo.png')
        self.label_3.setPixmap(self.pixmap_2)
        self.olympiad_table_run()
        self.results_table_run()

    def update_func(self):
        self.olympiad_table_run()
        self.results_table_run()
        if ww.USER_ID[0] == 0:
            self.admin_table_run()

    def edit_olympiad(self, row, col):
        self.info_olymp = list(self.cur.execute("select olympiad.title_ol, subjects.subject, olympiad.date, "
                                                "olympiad.time, olympiad.place, olympiad.duration, "
                                                "olympiad.when_results FROM olympiad LEFT JOIN subjects on "
                                                f"subjects.id_subject = olympiad.subject_id where id_user = "
                                                f"{ww.USER_ID[0]} and olympiad.title_ol = "
                                                f"'{self.olympiad_table.item(row, 0).text()}'").fetchall())[0]
        self.edit_ol = Edit_Ol(ww.USER_ID, self.info_olymp)
        self.edit_ol.show()

    def edit_results(self, row, col):
        self.info_result = tuple(self.cur.execute("select title_ol, when_results, scores, results FROM "
                                                  f"olympiad where id_user = {ww.USER_ID[0]} and title_ol = "
                                                  f"'{self.olympiad_table_2.item(row, 0).text()}'").fetchall())[0]
        self.edit_res = Edit_Res(ww.USER_ID, self.info_result)
        self.edit_res.show()

    def edit_users(self, row, col):
        self.info_users = tuple(self.cur.execute(f"select user_id, username, password FROM users where user_id = "
                                                 f"{self.olympiad_table_3.item(row, 0).text()}").fetchall())[0]
        self.edit_user = Edit_User(self.info_users)
        self.edit_user.show()

    def admin_table_run(self):
        text = self.find_Edit_3.text().lower()
        self.olympiad_table_3.setColumnCount(3)
        self.olympiad_table_3.setHorizontalHeaderLabels(["ID", "Пользователь", "Пароль"])
        self.olympiad_table_3.setRowCount(0)
        users = self.cur.execute("select user_id, username, password FROM users where "
                                 f"username LIKE '%{text}%'").fetchall()
        for i, row in enumerate(users):
            self.olympiad_table_3.setRowCount(self.olympiad_table_3.rowCount() + 1)
            for j, el in enumerate(row):
                if j == 2:
                    self.olympiad_table_3.setItem(i, j, QTableWidgetItem("*" * len(str(el))))
                    continue
                self.olympiad_table_3.setItem(i, j, QTableWidgetItem(str(el)))
        self.olympiad_table_3.resizeColumnsToContents()
        column_head = self.olympiad_table_3.horizontalHeader()
        column_head.setSectionResizeMode(1, QHeaderView.Stretch)

    def results_table_run(self):
        text = self.find_Edit_2.text().lower()
        self.olympiad_table_2.setColumnCount(5)
        self.olympiad_table_2.setHorizontalHeaderLabels(["Название", "Предмет", "Дата результатов",
                                                         "Баллы", "Результаты"])
        self.olympiad_table_2.setRowCount(0)
        filter_text = self.filter_2.currentText()
        filter_string = ""
        if filter_text == "Название":
            filter_string = "ORDER BY olympiad.title_ol"
        elif filter_text == "Предмет":
            filter_string = "ORDER BY subjects.subject"
        elif filter_text == "Баллы":
            filter_string = "ORDER BY olympiad.scores DESC"
        result = self.cur.execute(
            "select olympiad.title_ol, subjects.subject, olympiad.when_results, olympiad.scores, "
            "results FROM olympiad LEFT JOIN subjects on subjects.id_subject = "
            "olympiad.subject_id where "
            f"title_ol LIKE '%{text}%' and id_user = {ww.USER_ID[0]} " + filter_string).fetchall()
        if filter_text == "Дата результатов":
            result = sorted(filter(lambda x: x[2], result), key=lambda x: (int(x[2].split(".")[2]),
                                                                           int(x[2].split(".")[1]),
                                                                           int(x[2].split(".")[0])))
        elif filter_text == "Результаты":
            result = sorted(translate(list(result)), key=lambda x: x[-1])
            result = retranslate(result)
        for i, row in enumerate(result):
            self.olympiad_table_2.setRowCount(self.olympiad_table_2.rowCount() + 1)
            if row[4] and row[4] == "Победитель":
                color = "#64fa46"
            elif row[4] and row[4] == "Призер":
                color = "#fffb00"
            elif row[4] and row[4] != "Нет данных":
                color = "#ff4800"
            else:
                color = "#8f8f8f"
            for j, el in enumerate(row):
                if not el:
                    self.olympiad_table_2.setItem(i, j, QTableWidgetItem("Нет данных"))
                else:
                    self.olympiad_table_2.setItem(i, j, QTableWidgetItem(str(el)))
                self.olympiad_table_2.item(i, j).setBackground(QColor(color))
        self.olympiad_table_2.resizeColumnsToContents()
        column_head = self.olympiad_table_2.horizontalHeader()
        column_head.setSectionResizeMode(0, QHeaderView.Stretch)

    def downl(self):
        fname = QFileDialog.getOpenFileName(self, 'Выбрать файл', '', 'Файл (*.csv)')[0]
        try:
            with open(fname, encoding="utf8") as csvfile:
                reader = csv.reader(csvfile, delimiter=';', quotechar='"')
                for index, row in enumerate(reader):
                    new_id = len(list(self.cur.execute(f"SELECT ol_id FROM olympiad where id_user = "
                                                       f"{ww.USER_ID[0]}").fetchall())) + 1
                    checker = list(self.cur.execute(f"SELECT title_ol FROM olympiad WHERE title_ol = '{row[0]}' "
                                                    f"and id_user = {ww.USER_ID[0]}").fetchall())
                    try:
                        sub_id = int(list(self.cur.execute(f"SELECT id_subject from subjects where '{row[1]}' = "
                                                           f"subject").fetchall())[0][0])
                    except IndexError:
                        subject = row[1]
                        sub_id = len(list(self.cur.execute(f"SELECT id_subject from subjects").fetchall())) + 1
                        self.cur.execute(f"""INSERT INTO subjects(id_subject, subject) VALUES({sub_id}, '{subject}')""")
                    zapros = ["ol_id", "title_ol", "subject_id"]
                    values = [f"{new_id}", f"'{row[0]}'", f"{sub_id}"]
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
                    if row[6] != " " and row[6]:
                        zapros.append("when_results")
                        values.append(f"'{row[6]}'")
                    if row[7] != " " and row[7]:
                        zapros.append("scores")
                        values.append(f"'{row[7]}'")
                    if row[8] != " " and row[8]:
                        zapros.append("results")
                        values.append(f"'{row[8]}'")
                    if not checker:
                        zapros.append("id_user")
                        values.append(f'{ww.USER_ID[0]}')
                        zapros = ", ".join(zapros)
                        values = ", ".join(values)
                        self.cur.execute(f"""INSERT INTO olympiad({zapros}) VALUES({values})""")
        except MyFileNotFoundError as e:
            warning_message_box(e, "Внимание")
        except Exception as e:
            if e.__class__.__name__ != "FileNotFoundError":
                msg = QMessageBox.warning(self, "Внимание!", "Неверный формат текста в файле")

    def upl(self):
        self.upload_win = Upload_Window_Olympiad()
        self.upload_win.show()

    def upl_users(self):
        self.upload_win_user = Upload_Window_Users()
        self.upload_win_user.show()

    def olympiad_table_run(self):
        text = self.find_Edit.text().lower()
        self.olympiad_table.setColumnCount(5)
        self.olympiad_table.setHorizontalHeaderLabels(["Название", "Предмет", "Дата", "Место", "Дата результатов"])
        self.olympiad_table.setRowCount(0)
        filter_text = self.filter.currentText()
        filter_string = ""
        if filter_text == "Название":
            filter_string = "ORDER BY olympiad.title_ol"
        elif filter_text == "Предмет":
            filter_string = "ORDER BY subjects.subject"
        elif filter_text == "Баллы":
            filter_string = "ORDER BY olympiad.scores DESC"
        result = self.cur.execute("select olympiad.title_ol, subjects.subject, olympiad.date, olympiad.place, "
                                  "when_results FROM olympiad LEFT JOIN subjects on subjects.id_subject = "
                                  f"olympiad.subject_id where title_ol LIKE '%{text}%' and id_user = {ww.USER_ID[0]} "
                                  + filter_string).fetchall()
        if filter_text == "Дата результатов":
            result = sorted(filter(lambda x: x[4], result), key=lambda x: (int(x[4].split(".")[2]),
                                                                           int(x[4].split(".")[1]),
                                                                           int(x[4].split(".")[0])))
        elif filter_text == "Дата":
            result = sorted(filter(lambda x: x[2], result), key=lambda x: (int(x[2].split(".")[2]),
                                                                           int(x[2].split(".")[1]),
                                                                           int(x[2].split(".")[0])))
        for i, row in enumerate(result):
            self.olympiad_table.setRowCount(self.olympiad_table.rowCount() + 1)
            if row[2] and dt.date(int(row[2].split(".")[2]), int(row[2].split(".")[1]),
                                  int(row[2].split(".")[0])) > dt.date.today():
                color = "#46b8fa"
            else:
                color = "#8f8f8f"
            for j, el in enumerate(row):
                if not el:
                    self.olympiad_table.setItem(i, j, QTableWidgetItem("Нет данных"))
                else:
                    self.olympiad_table.setItem(i, j, QTableWidgetItem(str(el)))
                self.olympiad_table.item(i, j).setBackground(QColor(color))
        self.olympiad_table.resizeColumnsToContents()
        column_head = self.olympiad_table.horizontalHeader()
        column_head.setSectionResizeMode(0, QHeaderView.Stretch)

    def add_ol(self):
        self.add_window = Add_olympiad(ww.USER_ID)
        self.add_window.show()

    def keyPressEvent(self, event):
        if int(event.modifiers()) == Qt.ControlModifier:
            if event.key() == Qt.Key_S:
                self.upload_win = Upload_Window_Olympiad()
                self.upload_win.show()
            elif event.key() == Qt.Key_V or event.key() == Qt.Key_X:
                self.downl()
            elif event.key() == Qt.Key_Question:
                pass


class Welcome(ww.Welcome):
    def __init__(self):
        super(Welcome, self).__init__()

    def closeEvent(self, event):
        self.main_window = Main_Table_Window()
        if ww.CLOSED_FLAG:
            self.main_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Welcome()
    w.show()
    # w = Main_Table_Window()
    # w.show()
    sys.exit(app.exec_())
