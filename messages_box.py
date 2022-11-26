from PyQt5.QtWidgets import QMessageBox


def warning_message_box(exp, title):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Warning)
    msg_box.setWindowTitle(title)
    msg_box.setText(f"Внимание! {str(exp)}")
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec_()


def info_message_box(title, message):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec_()
