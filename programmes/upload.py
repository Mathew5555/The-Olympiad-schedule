import csv
import welcome_window as ww
from edit_and_delete import *
from PyQt5 import QtGui


class Upload_Window_Olympiad(QDialog):
    def __init__(self):
        super(Upload_Window_Olympiad, self).__init__()
        self.setWindowIcon(QtGui.QIcon('../data/background/icon.png'))
        uic.loadUi('../data/graphics/upload_dialog.ui', self)
        con = sqlite3.connect("../data/olympiads.db")
        self.cur = con.cursor()
        self.push_button_upload.clicked.connect(self.upload_func)
        self.radio_button_txt.nextCheckState()

    def upload_func(self):
        try:
            result = self.cur.execute("select olympiad.title_ol, subjects.subject, olympiad.date, olympiad.time, "
                                      "olympiad.place, olympiad.duration, olympiad.when_results, olympiad.scores, "
                                      "olympiad.results FROM olympiad LEFT JOIN subjects on "
                                      "subjects.id_subject = olympiad.subject_id  where id_user = "
                                      f"{ww.USER_ID[0]}").fetchall()
            if self.radio_button_txt.isChecked():
                with open('../download_files/olymp.txt', 'wt', encoding="UTF-8") as f:
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
                        if el[6]:
                            f.write(f"Дата результатов: {el[6]}\n")
                        else:
                            f.write("Дата результатов: Нет данных\n")
                        if el[7]:
                            f.write(f"Баллы: {el[7]}\n")
                        else:
                            f.write("Баллы: Нет данных\n")
                        if el[8]:
                            f.write(f"Итоговый результат: {el[8]}\n")
                        else:
                            f.write("Итоговый результат: Нет данных\n")
                        f.write("----------------------------------------------------------\n")
                        self.close()
            else:
                with open('../download_files/olymp.csv', 'w', newline='', encoding="utf8") as csvfile:
                    writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(
                        ["Название", "Предмет", "Дата", "Время", "Место", "Длительность", "Дата результатов", "Баллы",
                         "Итог"])
                    for el in result:
                        res = [el[0], el[1]]
                        for item in el[2::]:
                            if not item:
                                res.append("Нет данных")
                            else:
                                res.append(item)
                        self.close()
                        writer.writerow(res)
        except Exception as e:
            print(e)


class Upload_Window_Users(QDialog):
    def __init__(self):
        super(Upload_Window_Users, self).__init__()
        self.setWindowIcon(QtGui.QIcon('../data/background/icon.png'))
        uic.loadUi('../data/graphics/upload_dialog.ui', self)
        con = sqlite3.connect("../data/olympiads.db")
        self.cur = con.cursor()
        self.push_button_upload.clicked.connect(self.upload_func)
        self.radio_button_txt.nextCheckState()

    def upload_func(self):
        result = self.cur.execute("select user_id, username, password FROM users").fetchall()
        if self.radio_button_txt.isChecked():
            with open('../download_files/users.txt', 'wt', encoding="UTF-8") as f:
                for el in result:
                    f.write(f"Id: {el[0]}\nЛогин: {el[1]}\nПароль: {el[2]}\n")
                    f.write("----------------------------------------------------------\n")
        else:
            with open('../download_files/users.csv', 'w', newline='', encoding="utf8") as csvfile:
                writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(["Id", "Логин", "Пароль"])
                for el in result:
                    writer.writerow([el[0], el[1], el[2]])
        self.close()
