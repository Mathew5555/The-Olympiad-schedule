import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5 import uic


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
        self.comboBox.hide()
        self.label_12.setText(self.elements[1])
        self.timeEdit.hide()
        self.label_13.setText(self.elements[2])
        self.label_14.setText(self.elements[3])
        self.spinBox.hide()
        self.label_15.setText(self.elements[4])
        self.dateEdit.hide()
        self.label_16.setText(self.elements[5])
        self.dateEdit_2.hide()
        self.label_17.setText(self.elements[6])
        self.lineEdit_2.hide()
        self.lineEdit.hide()
        self.spinBox.setMaximum(2147483647)
        self.comboBox.addItems(list(el[0] for el in self.con.cursor().execute(f"SELECT subject from subjects")))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Edit_Ol()
    ex.show()
    sys.exit(app.exec_())
