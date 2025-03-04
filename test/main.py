from PyQt6.QtWidgets import QApplication, QDialog
from TEST_FLASK import MainWindow
from login_window import LoginWindow

if __name__ == "__main__":
    app = QApplication([])

    login_window = LoginWindow()

    if login_window.exec() == QDialog.DialogCode.Accepted:
        main_window = MainWindow()
        main_window.show()

    app.exec()