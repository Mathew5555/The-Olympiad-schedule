import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView
from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import Qt
import welcome_window as ww

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
        self.run()

    def run(self):
        text = self.find_Edit.text().lower()
        self.olympiad_table.setColumnCount(4)
        self.olympiad_table.setHorizontalHeaderLabels(["Название", "Предмет", "Дата", "Место"])
        self.olympiad_table.setRowCount(0)
        filter_text = self.filter.currentText()
        if filter_text == "Без фильтра":
            result = self.cur.execute("select olympiad.title_ol, subjects.subject, olympiad.date, olympiad.place FROM "
                                      "olympiad LEFT JOIN subjects on subjects.id_subject = olympiad.subject_id where "
                                      f"title_ol LIKE '%{text}%'").fetchall()
        elif filter_text == "Название":
            result = self.cur.execute("select olympiad.title_ol, subjects.subject, olympiad.date, olympiad.place FROM "
                                      "olympiad LEFT JOIN subjects on subjects.id_subject = olympiad.subject_id where "
                                      f"title_ol LIKE '%{text}%' ORDER BY olympiad.title_ol").fetchall()
        elif filter_text == "Предмет":
            result = self.cur.execute("select olympiad.title_ol, subjects.subject, olympiad.date, olympiad.place FROM "
                                      "olympiad LEFT JOIN subjects on subjects.id_subject = olympiad.subject_id where "
                                      f"title_ol LIKE '%{text}%' ORDER BY subjects.subject").fetchall()
        else:
            result = self.cur.execute("select olympiad.title_ol, subjects.subject, olympiad.date, olympiad.place FROM "
                                      "olympiad LEFT JOIN subjects on subjects.id_subject = olympiad.subject_id where "
                                      f"title_ol LIKE '%{text}%'").fetchall()
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
        pass
        # self.add_window =


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
