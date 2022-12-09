from PyQt5.QtWidgets import QMessageBox


def critical_message_box(exp, title):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Critical)
    msg_box.setWindowTitle(title)
    msg_box.setText(str(exp))
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec_()


def warning_message_box(exp, title):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Warning)
    msg_box.setWindowTitle(title)
    msg_box.setText(str(exp))
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec_()


def info_message_box(exp, title):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setWindowTitle(title)
    msg_box.setText(str(exp))
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec_()
