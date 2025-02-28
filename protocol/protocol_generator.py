import sys
import sqlite3
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QMessageBox)
from docx import Document
from datetime import datetime
import psycopg2
from PyQt6.QtWidgets import QDateEdit
from PyQt6.QtCore import QDate

class ProtocolGenerator(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Генератор на протоколи за ремонт")

        self.date_label = QLabel("Дата:")
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())  # Задаване на текущата дата по подразбиране

        self.serial_number_label = QLabel("")
        self.serial_number_input = QLineEdit()

        self.serial_number_label = QLabel("Сериен номер:")
        self.serial_number_input = QLineEdit()

        self.serial_number_label = QLabel("Сериен номер:")
        self.serial_number_input = QLineEdit()

        self.serial_number_label = QLabel("Сериен номер:")
        self.serial_number_input = QLineEdit()

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
        layout.addWidget(self.date_label)
        layout.addWidget(self.date_edit)
        layout.addWidget(self.serial_number_label)
        layout.addWidget(self.serial_number_input)
        layout.addWidget(self.device_info_label)
        layout.addWidget(self.device_info_text)
        layout.addWidget(self.problem_description_label)
        layout.addWidget(self.problem_description_input)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

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

    def generate_protocol(self):
        serial_number = self.serial_number_input.text()
        problem_description = self.problem_description_input.text()

        if not serial_number or not problem_description:
            QMessageBox.warning(self, "Предупреждение", "Моля, въведете сериен номер и описание на проблема.")
            return

        conn = psycopg2.connect(
            "dbname=protocols user=postgres password=VA0885281774")  # Заменете с вашите данни за връзка
        cur = conn.cursor()

        # Изпълнение на SQL заявка за извличане на информация за продукта
        sql = "SELECT company_name, company_address, company_manager, device_address, phone_number, device, serial_number FROM devices WHERE serial_number = %s"
        cur.execute(sql, (serial_number,))
        device_info = cur.fetchone()


        if not device_info:
            QMessageBox.warning(self, "Предупреждение", "Не е намерена информация за устройството с този сериен номер.")
            return

        conn = psycopg2.connect(
            "dbname=protocols user=postgres password=VA0885281774")  # Заменете с вашите данни за връзка
        cur = conn.cursor()

        # Изпълнение на SQL заявка за извличане на информация за продукта
        sql = "SELECT id, serial_number, problem_description, date FROM protocols WHERE serial_number = %s"
        cur.execute(sql, (serial_number,))
        protocol_info = cur.fetchone()

        document = Document("template.doc")
        selected_date = self.date_edit.date()

        protocol_id = protocol_info[0]
        date_string = selected_date.toString("dd.MM.yyyy")  # Форматиране на датата
        company_name = device_info[0]
        company_address = device_info[1]
        company_manager = device_info[2]
        device_address = device_info[3]
        phone_number = device_info[4]
        device = device_info[5]
        serial_number = serial_number
        problem_description = protocol_info[2]

        for paragraph in document.paragraphs:
            if "[номер на протокол от базата данни]" in paragraph.text:
                paragraph.text = paragraph.text.replace("[номер на протокол от базата данни]", protocol_id)
            elif "[дата[дд-мм-гг]]" in paragraph.text:
                paragraph.text.replace("[дата[дд-мм-гг]]", date_string)
            elif "[Име на фирма]" in paragraph.text:
                paragraph.text.replace("[Име на фирма]", company_name)
            elif "[адрес на фирма]" in paragraph.text:
                paragraph.text.replace("[адрес на фирма]", company_address)
            elif "[управител]" in paragraph.text:
                paragraph.text.replace("[управител]", company_manager)
            elif "[адрес на устройството]" in paragraph.text:
                paragraph.text.replace("[адрес на устройството]", device_address)
            elif "[телефонен номер]" in paragraph.text:
                paragraph.text.replace("[телефонен номер]", phone_number)
            elif "[какво е оставено и име и модел]" in paragraph.text:
                paragraph.text.replace("[какво е оставено и име и модел]", device)
            elif "[сериен номер]" in paragraph.text:
                paragraph.text.replace("[сериен номер]", serial_number)
            elif "[описание на порблема]" in paragraph.text:
                paragraph.text.replace("[описание на порблема]", problem_description)
            # elif "[Сериен номер]" in paragraph.text:
            #     paragraph.text = paragraph.text.replace("[Сериен номер]", serial_number)
            # elif "[Модел]" in paragraph.text:
            #     paragraph.text = paragraph.text.replace("[Модел]", device[1])
            # elif "[Производител]" in paragraph.text:
            #     paragraph.text = paragraph.text.replace("[Производител]", device[2])
            # elif "[Описание на проблема]" in paragraph.text:
            #     paragraph.text = paragraph.text.replace("[Описание на проблема]", problem_description)

        document.save(f"protocol_{serial_number}_{date_string}.docx")

        QMessageBox.information(self, "Успех", "Протоколът беше генериран успешно.")

        self.save_protocol()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProtocolGenerator()
    window.show()
    sys.exit(app.exec())