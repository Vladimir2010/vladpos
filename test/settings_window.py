import sqlite3
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame
)

DB_PATH = "database/pos_syst.db"

class SettingsWindow(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.setWindowTitle("Settings Window")
        self.setGeometry(100, 100, 400, 300)
        self.main_window = main_window

        main_layout = QVBoxLayout()

        general_settings_frame = QFrame()
        general_settings_layout = QVBoxLayout()
        general_settings_frame.setLayout(general_settings_layout)

        self.operator_name_input = QLineEdit()
        self.operator_number_input = QLineEdit()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)

        general_settings_layout.addWidget(QLabel("Operator Name"))
        general_settings_layout.addWidget(self.operator_name_input)
        general_settings_layout.addWidget(QLabel("Operator Number"))
        general_settings_layout.addWidget(self.operator_number_input)
        general_settings_layout.addWidget(save_button)

        main_layout.addWidget(general_settings_frame)
        self.setLayout(main_layout)

    def save_settings(self):
        operator_name = self.operator_name_input.text()
        operator_number = self.operator_number_input.text()
        if operator_name and operator_number:
            connection = sqlite3.connect(DB_PATH)
            cursor = connection.cursor()
            cursor.execute('''
                INSERT INTO settings (operator_name, operator_number)
                VALUES (?, ?)
            ''', (operator_name, operator_number))
            connection.commit()
            connection.close()
            self.main_window.update_operator_label(f"{operator_name} - {operator_number}")
            self.accept()