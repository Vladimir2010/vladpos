import sys
import serial.tools.list_ports as ports_list
import os
import sqlite3
import json
from openpyxl import Workbook, load_workbook
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QAction, QPixmap
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QFrame, QVBoxLayout, QHBoxLayout, QWidget, QMenu,
    QSizePolicy, QLabel, QLineEdit, QPushButton, QComboBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QDialog, QDialogButtonBox, QCalendarWidget, QTextEdit, QListWidget,
    QFileDialog, QAbstractItemView, QMessageBox, QTabWidget
)

DB_DIR = "database"
DB_PATH = "database/pos_system.db"


class SettingsWindow(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.setWindowTitle("Настройки")
        self.setGeometry(100, 100, 600, 400)
        self.main_window = main_window


        main_layout = QVBoxLayout()

        # Create a QTabWidget
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # Add the first tab
        self.tab1 = QWidget()
        self.tabs.addTab(self.tab1, "Основни")
        self.tab1_layout = QVBoxLayout()
        self.tab1.setLayout(self.tab1_layout)

        # First Frame
        first_frame = QFrame()
        first_frame.setFrameShape(QFrame.Shape.NoFrame)
        first_layout = QVBoxLayout()
        first_frame.setLayout(first_layout)

        row1_layout = QHBoxLayout()
        row2_layout = QHBoxLayout()
        row3_layout = QHBoxLayout()
        row4_layout = QHBoxLayout()
        row5_layout = QHBoxLayout()

        first_title = QLabel("Марка")
        first_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        first_input = QComboBox()
        self.second_input = QComboBox()
        self.second_input.addItems(["Something"])
        self.update_second_combo_box(first_input.currentIndex())
        first_input.currentIndexChanged.connect(self.update_second_combo_box)
        first_input.addItems(["Daisy", "Datecs", "Tremol"])
        row1_layout.addWidget(first_title)
        row1_layout.addWidget(first_input)

        second_title = QLabel("Модел")
        second_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        row2_layout.addWidget(second_title)
        row2_layout.addWidget(self.second_input)


        third_title = QLabel("Тип връзка")
        third_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        third_input = QComboBox()
        third_input.addItems(["COM порт"])
        row3_layout.addWidget(third_title)
        row3_layout.addWidget(third_input)

        fourth_title = QLabel("COM порт")
        fourth_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        fourth_input = QComboBox()
        fourth_input.addItems([port.device for port in ports_list.comports()])
        row4_layout.addWidget(fourth_title)
        row4_layout.addWidget(fourth_input)

        fifth_title = QLabel("Скорост")
        fifth_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        fifth_input = QComboBox()
        fifth_input.addItems(["9600", "19200", "38400", "57600", "115200"])
        row5_layout.addWidget(fifth_title)
        row5_layout.addWidget(fifth_input)

        first_layout.addLayout(row1_layout)
        first_layout.addLayout(row2_layout)
        first_layout.addLayout(row3_layout)
        first_layout.addLayout(row4_layout)
        first_layout.addLayout(row5_layout)

        # Second Frame
        second_frame = QFrame()
        second_frame.setFrameShape(QFrame.Shape.NoFrame)
        second_layout = QVBoxLayout()
        second_frame.setLayout(second_layout)

        second_title = QLabel("Настройки на оператор")
        second_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        second_layout.addWidget(second_title)

        self.operator_name_input = QLineEdit()
        self.operator_number_input = QLineEdit()
        save_button = QPushButton("Запази")
        save_button.clicked.connect(self.save_settings)

        second_layout.addWidget(QLabel("Име на оператор"))
        second_layout.addWidget(self.operator_name_input)
        second_layout.addWidget(QLabel("Номер на оператор"))
        second_layout.addWidget(self.operator_number_input)
        second_layout.addWidget(save_button)

        # Third Frame
        third_frame = QFrame()
        third_frame.setFrameShape(QFrame.Shape.NoFrame)
        third_layout = QVBoxLayout()
        third_frame.setLayout(third_layout)

        third_title = QLabel("Настройки на картов терминал")
        third_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        third_layout.addWidget(third_title)

        for i in range(5):
            row_layout = QHBoxLayout()
            label = QLabel(f"Етикет {i + 1}:")
            input = QComboBox()
            input.addItems([f"Option {j + 1}" for j in range(3)])
            row_layout.addWidget(label)
            row_layout.addWidget(input)
            third_layout.addLayout(row_layout)

        # Add frames to the first tab layout
        self.tab1_layout.addWidget(first_frame)
        self.tab1_layout.addWidget(second_frame)
        self.tab1_layout.addWidget(third_frame)


        # User Registration Tab
        user_registration_frame = QFrame()
        user_registration_layout = QVBoxLayout()
        user_registration_frame.setLayout(user_registration_layout)

        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        register_button = QPushButton("Register")
        register_button.clicked.connect(self.register_user)

        user_registration_layout.addWidget(QLabel("Username"))
        user_registration_layout.addWidget(self.username_input)
        user_registration_layout.addWidget(QLabel("Password"))
        user_registration_layout.addWidget(self.password_input)
        user_registration_layout.addWidget(register_button)

        self.tabs.addTab(user_registration_frame, "User Registration")

        # Add the second tab
        self.tab2 = QWidget()
        self.tabs.addTab(self.tab2, "Нова фирма")
        self.tab2_layout = QVBoxLayout()
        self.tab2.setLayout(self.tab2_layout)

        # Add labels and inputs to the second tab
        self.firm_name_label = QLabel("Име на фирма:")
        self.firm_name_input = QLineEdit()
        self.tab2_layout.addWidget(self.firm_name_label)
        self.tab2_layout.addWidget(self.firm_name_input)

        self.firm_eik_label = QLabel("Булстат:")
        self.firm_eik_input = QLineEdit()
        self.tab2_layout.addWidget(self.firm_eik_label)
        self.tab2_layout.addWidget(self.firm_eik_input)

        self.firm_dds_label = QLabel("ДДС Номер:")
        self.firm_dds_input = QLineEdit()
        self.tab2_layout.addWidget(self.firm_dds_label)
        self.tab2_layout.addWidget(self.firm_dds_input)

        self.firm_address_label = QLabel("Адрес:")
        self.firm_address_input = QLineEdit()
        self.tab2_layout.addWidget(self.firm_address_label)
        self.tab2_layout.addWidget(self.firm_address_input)

        self.firm_mol_label = QLabel("МОЛ:")
        self.firm_mol_input = QLineEdit()
        self.tab2_layout.addWidget(self.firm_mol_label)
        self.tab2_layout.addWidget(self.firm_mol_input)

        self.firm_phone_label = QLabel("Тел. номер:")
        self.firm_phone_input = QLineEdit()
        self.tab2_layout.addWidget(self.firm_phone_label)
        self.tab2_layout.addWidget(self.firm_phone_input)

        self.add_firm_button = QPushButton("Добави")
        self.add_firm_button.clicked.connect(self.add_firm)
        self.tab2_layout.addWidget(self.add_firm_button)

        self.setLayout(main_layout)


    def save_additional_settings(self):
        # Implement the code to save the additional settings
        additional_setting1 = self.additional_setting1_input.text()
        additional_setting2 = self.additional_setting2_input.text()

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

    def add_firm(self):
        # Implement the code to add a firm
        firm_name = self.firm_name_input.text()
        firm_eik = self.firm_eik_input.text()
        firm_dds = self.firm_dds_input.text()
        firm_address = self.firm_address_input.text()
        firm_mol = self.firm_mol_input.text()
        firm_phone = self.firm_phone_input.text()

        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO firm (name, eik, dds, address, mol, phone)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (firm_name, firm_eik, firm_dds, firm_address, firm_mol, firm_phone))
        connection.commit()
        connection.close()

        self.firm_name_input.clear()
        self.firm_eik_input.clear()
        self.firm_dds_input.clear()
        self.firm_address_input.clear()
        self.firm_mol_input.clear()
        self.firm_phone_input.clear()

    def register_user(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if username and password:
            connection = sqlite3.connect(DB_PATH)
            cursor = connection.cursor()
            cursor.execute('''
                   INSERT INTO users (username, password)
                   VALUES (?, ?)
               ''', (username, password))
            connection.commit()
            connection.close()
            self.username_input.clear()
            self.password_input.clear()
            QMessageBox.information(self, "Registration Successful", "User has been registered successfully.")

    def update_second_combo_box(self, index):
        self.second_input.clear()
        if index == 0:
            self.second_input.addItems(["Compact S 01", "Compact M 02", "Perfect S 01", "Perfect M 01", "eXpert SX 01"])
        elif index == 1:
            self.second_input.addItems(["DP-150", "DP-150 MX", "DP-25", "DP-25 MX", "WP-50"])
        elif index == 2:
            self.second_input.addItems(["S25", "M20", "M23", "ZM", "ZS", "S21", "A19 Plus"])

