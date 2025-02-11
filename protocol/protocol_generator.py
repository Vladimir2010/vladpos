import sys
import sqlite3
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QMessageBox)
from docx import Document
from datetime import datetime

class ProtocolGenerator(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Генератор на протоколи за ремонт")

        self.serial_number_label = QLabel("Сериен номер:")
        self.serial_number_input = QLineEdit()

        self.device_info_label = QLabel("Информация за устройството:")
        self.device_info_text = QLabel()

        self.problem_description_label = QLabel("Описание на проблема:")
        self.problem_description_input = QLineEdit()

        self.generate_button = QPushButton("Генерирай протокол")
        self.generate_button.clicked.connect(self.generate_protocol)

        self.save_button = QPushButton("Запис")
        self.save_button.clicked.connect(self.save_protocol)

        layout = QVBoxLayout()
        layout.addWidget(self.serial_number_label)
        layout.addWidget(self.serial_number_input)
        layout.addWidget(self.device_info_label)
        layout.addWidget(self.device_info_text)
        layout.addWidget(self.problem_description_label)
        layout.addWidget(self.problem_description_input)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

        self.conn = sqlite3.connect('repair_protocols.db')
        self.cursor = self.conn.cursor()

        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS devices (
                serial_number TEXT PRIMARY KEY,
                model TEXT,
                manufacturer TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS protocols (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                serial_number TEXT,
                problem_description TEXT,
                date TEXT
            )
        ''')

        self.conn.commit()

    def generate_protocol(self):
        serial_number = self.serial_number_input.text()
        problem_description = self.problem_description_input.text()

        if not serial_number or not problem_description:
            QMessageBox.warning(self, "Предупреждение", "Моля, въведете сериен номер и описание на проблема.")
            return

        self.cursor.execute("SELECT * FROM devices WHERE serial_number=?", (serial_number,))
        device = self.cursor.fetchone()

        if not device:
            QMessageBox.warning(self, "Предупреждение", "Не е намерена информация за устройството с този сериен номер.")
            return

        document = Document("template.doc")
        now = datetime.now()
        date_string = now.strftime("%d.%m.%Y")

        for paragraph in document.paragraphs:
            if "[номер на протокол от базата данни]" in paragraph.text:
                paragraph.text = paragraph.text.replace("[номер на протокол от базата данни]", protocol_id)
            elif "[дата[дд-мм-гг]]" in paragraph.text:
                paragraph.text.replace("[дата[дд-мм-гг]]", date_string)
            elif "[Име на фирма]" in paragraph.text:
                paragraph.text.replace("[Име на фирма]", company_name)
            elif "[дата[дд-мм-гг]]" in paragraph.text:
                paragraph.text.replace("[дата[дд-мм-гг]]", date_string)
            elif "[дата[дд-мм-гг]]" in paragraph.text:
                paragraph.text.replace("[дата[дд-мм-гг]]", date_string)
            elif "[дата[дд-мм-гг]]" in paragraph.text:
                paragraph.text.replace("[дата[дд-мм-гг]]", date_string)
            elif "[дата[дд-мм-гг]]" in paragraph.text:
                paragraph.text.replace("[дата[дд-мм-гг]]", date_string)
            elif "[дата[дд-мм-гг]]" in paragraph.text:
                paragraph.text.replace("[дата[дд-мм-гг]]", date_string)
            elif "[дата[дд-мм-гг]]" in paragraph.text:
                paragraph.text.replace("[дата[дд-мм-гг]]", date_string)
            elif "[дата[дд-мм-гг]]" in paragraph.text:
                paragraph.text.replace("[дата[дд-мм-гг]]", date_string)
            # elif "[Сериен номер]" in paragraph.text:
            #     paragraph.text = paragraph.text.replace("[Сериен номер]", serial_number)
            # elif "[Модел]" in paragraph.text:
            #     paragraph.text = paragraph.text.replace("[Модел]", device[1])
            # elif "[Производител]" in paragraph.text:
            #     paragraph.text = paragraph.text.replace("[Производител]", device[2])
            # elif "[Описание на проблема]" in paragraph.text:
            #     paragraph.text = paragraph.text.replace("[Описание на проблема]", problem_description)


        for paragraph in document.paragraphs:
            if "[Дата]" in paragraph.text:
                paragraph.text = paragraph.text.replace("[Дата]", date_string)

        document.save(f"protocol_{serial_number}_{date_string}.docx")

        QMessageBox.information(self, "Успех", "Протоколът беше генериран успешно.")

        self.save_protocol()

    def save_protocol(self):
        serial_number = self.serial_number_input.text()
        problem_description = self.problem_description_input.text()

        if not serial_number or not problem_description:
            return

        now = datetime.now()
        date_string = now.strftime("%d.%m.%Y")

        self.cursor.execute("INSERT INTO protocols (serial_number, problem_description, date) VALUES (?, ?, ?)",
                           (serial_number, problem_description, date_string))
        self.conn.commit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProtocolGenerator()
    window.show()
    sys.exit(app.exec())