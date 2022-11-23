import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
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
        self.setFixedSize(1200, 800)
        self.setStyleSheet(stylesheet_main)


class Welcome(ww.Welcome):
    def __init__(self):
        super(Welcome, self).__init__()

    def closeEvent(self, event):
        self.tmp = MainWindow()
        self.tmp.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Welcome()
    w.show()
    sys.exit(app.exec_())
