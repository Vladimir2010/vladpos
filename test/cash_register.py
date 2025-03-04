import sys
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

class CashRegisterWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Фискално устройство")
        self.setGeometry(100, 100, 600, 400)
        main_layout = QVBoxLayout()

        # First Frame
        first_frame = QFrame()
        first_frame.setFrameShape(QFrame.Shape.NoFrame)
        first_layout = QVBoxLayout()
        first_frame.setLayout(first_layout)

        first_title = QLabel("First Title")
        first_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        first_layout.addWidget(first_title)

        first_row_layout = QHBoxLayout()
        first_label = QLabel("Label:")
        first_input = QLineEdit()
        plus_button = QPushButton("+")
        minus_button = QPushButton("-")
        first_row_layout.addWidget(first_label)
        first_row_layout.addWidget(first_input)
        first_row_layout.addWidget(plus_button)
        first_row_layout.addWidget(minus_button)
        first_layout.addLayout(first_row_layout)

        # Second Frame
        second_frame = QFrame()
        second_frame.setFrameShape(QFrame.Shape.NoFrame)
        second_layout = QVBoxLayout()
        second_frame.setLayout(second_layout)

        second_title = QLabel("Second Title")
        second_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        second_layout.addWidget(second_title)

        second_row_layout1 = QHBoxLayout()
        second_label1 = QLabel("Label 1:")
        second_label2 = QLabel("Label 2:")
        second_row_layout1.addWidget(second_label1)
        second_row_layout1.addWidget(second_label2)
        second_layout.addLayout(second_row_layout1)

        second_row_layout2 = QHBoxLayout()
        second_input1 = QCalendarWidget()
        second_input2 = QCalendarWidget()
        second_row_layout2.addWidget(second_input1)
        second_row_layout2.addWidget(second_input2)
        second_layout.addLayout(second_row_layout2)

        second_button = QPushButton("Button")
        second_layout.addWidget(second_button)

        # Third Frame
        third_frame = QFrame()
        third_frame.setFrameShape(QFrame.Shape.NoFrame)
        third_layout = QVBoxLayout()
        third_frame.setLayout(third_layout)

        third_title = QLabel("Third Title")
        third_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        third_layout.addWidget(third_title)

        third_row_layout1 = QHBoxLayout()
        third_label1 = QLabel("Label 1:")
        third_label2 = QLabel("Label 2:")
        third_row_layout1.addWidget(third_label1)
        third_row_layout1.addWidget(third_label2)
        third_layout.addLayout(third_row_layout1)

        third_row_layout2 = QHBoxLayout()
        third_input1 = QCalendarWidget()
        third_input2 = QCalendarWidget()
        third_row_layout2.addWidget(third_input1)
        third_row_layout2.addWidget(third_input2)
        third_layout.addLayout(third_row_layout2)

        third_button = QPushButton("Button")
        third_layout.addWidget(third_button)

        # Fourth Frame
        fourth_frame = QFrame()
        fourth_frame.setFrameShape(QFrame.Shape.NoFrame)
        fourth_layout = QVBoxLayout()
        fourth_frame.setLayout(fourth_layout)

        fourth_title = QLabel("Fourth Title")
        fourth_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        fourth_layout.addWidget(fourth_title)

        fourth_button = QPushButton("Button")
        fourth_layout.addWidget(fourth_button)

        # Add frames to main layout
        main_layout.addWidget(first_frame)
        main_layout.addWidget(second_frame)
        main_layout.addWidget(third_frame)
        main_layout.addWidget(fourth_frame)

        self.setLayout(main_layout)
