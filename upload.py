import csv
import welcome_window as ww
from edit_and_delete import *


class Upload_Window(QDialog):
    def __init__(self):
        super(Upload_Window, self).__init__()
        uic.loadUi('upload_dialog.ui', self)
        con = sqlite3.connect("olympiads.db")
        self.cur = con.cursor()
        self.push_button_upload.clicked.connect(self.upload_func)
        self.radio_button_txt.nextCheckState()

    def upload_func(self):
        result = self.cur.execute("select olympiad.title_ol, subjects.subject, olympiad.date, olympiad.time, "
                                  "olympiad.place, olympiad.duration FROM olympiad LEFT JOIN subjects on "
                                  "subjects.id_subject = olympiad.subject_id  where id_user = "
                                  f"{ww.USER_ID[0]}").fetchall()
        if self.radio_button_txt.isChecked():
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
