import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('welcome_window.ui', self)
        self.setFixedSize(1200, 800)


stylesheet_main = """
    MainWindow {
        background-image: url("bacground.jpg");
        background-repeat: no-repeat;
        background-position: center;
    } """

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.setStyleSheet(stylesheet_main)
    ex.show()
    sys.exit(app.exec_())
