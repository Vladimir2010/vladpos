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
from customer_window import CustomersWindow
from documents_window import DocumentsWindow
from invoices_window import InvoicesWindow
from database import create_database
from products_window import ProductsWindow
from settings_window import SettingsWindow
from help_window import HelpWindow
from cash_register import CashRegisterWindow
# from login_window import LoginWindow


DB_DIR = "database"
DB_PATH = "database/pos_system.db"

create_database()
# class SpravkiDocumentsWindow(QDialog):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Spravki Documents")
#         self.setGeometry(100, 100, 400, 300)
#         layout = QVBoxLayout()
#         label = QLabel("Spravki Documents Window")
#         layout.addWidget(label)
#         button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
#         button_box.accepted.connect(self.accept)
#         layout.addWidget(button_box)
#         self.setLayout(layout)
#
# class SpravkiClientsWindow(QDialog):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Spravki Clients")
#         self.setGeometry(100, 100, 400, 300)
#         layout = QVBoxLayout()
#         label = QLabel("Spravki Clients Window")
#         layout.addWidget(label)
#         button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
#         button_box.accepted.connect(self.accept)
#         layout.addWidget(button_box)
#         self.setLayout(layout)
#
# class SpravkiSalesWindow(QDialog):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Spravki Sales")
#         self.setGeometry(100, 100, 400, 300)
#         layout = QVBoxLayout()
#         label = QLabel("Spravki Sales Window")
#         layout.addWidget(label)
#         button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
#         button_box.accepted.connect(self.accept)
#         layout.addWidget(button_box)
#         self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("VladPos")
        self.setWindowIcon(QIcon('vladpos_logo.png'))
        self.setGeometry(100, 100, 800, 600)
        self.showMaximized()

        # Set up the central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Create frames
        frame1 = QFrame()
        frame1.setFrameShape(QFrame.Shape.NoFrame)
        frame1.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

        frame2 = QFrame()
        frame2.setFrameShape(QFrame.Shape.NoFrame)
        frame2.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

        frame3 = QFrame()
        frame3.setFrameShape(QFrame.Shape.NoFrame)
        frame3.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

        # Add frames to layout
        main_layout.addWidget(frame1, 1)
        main_layout.addWidget(frame2, 5)
        main_layout.addWidget(frame3, 2)

        # Create menubar
        menubar = self.menuBar()

        # Create Cash Register menu
        cash_register_menu = QMenu("Касов апарат", self)
        cash_register_menu.setIcon(QIcon('receipt.png'))
        cash_register_action = QAction(QIcon('receipt.png'), 'Касов апарат', self)
        cash_register_action.triggered.connect(self.open_cash_register_window)
        cash_register_menu.addAction(cash_register_action)
        menubar.addMenu(cash_register_menu)

        # Create Spravki menu
        spravki_menu = QMenu("Справки", self)
        spravki_menu.setIcon(QIcon('paper.png'))

        # Spravki Documents submenu
        spravki_documents_action = QAction('Справка по документи', self)
        spravki_documents_action.triggered.connect(self.open_spravki_documents_window)
        spravki_menu.addAction(spravki_documents_action)

        # Spravki Clients submenu
        spravki_clients_action = QAction('Справка по контрагенти', self)
        spravki_clients_action.triggered.connect(self.open_spravki_clients_window)
        spravki_menu.addAction(spravki_clients_action)

        # Spravki Sales submenu
        spravki_sales_action = QAction('Справка по продажби', self)
        spravki_sales_action.triggered.connect(self.open_spravki_sales_window)
        spravki_menu.addAction(spravki_sales_action)

        menubar.addMenu(spravki_menu)

        # Create New Menu
        new_menu = QMenu("Продукти", self)
        new_menu.setIcon(QIcon('products.png'))
        new_action = QAction(QIcon('new_action_icon.png'), 'Работа с продукти', self)
        new_action.triggered.connect(self.open_new_window)
        new_menu.addAction(new_action)

        menubar.addMenu(new_menu)

        # Add the following code in the menubar section to create the Customers menu
        customers_menu = QMenu("Контрагенти", self)
        customers_menu.setIcon(QIcon('user-2.png'))
        customers_action = QAction(QIcon('customer_action_icon.png'), 'Контрагенти', self)
        customers_action.triggered.connect(self.open_customers_window)
        customers_menu.addAction(customers_action)
        menubar.addMenu(customers_menu)

        # Add the following code in the menubar section to create the Documents menu
        documents_menu = QMenu("Документи", self)
        documents_menu.setIcon(QIcon('paper.png'))
        documents_action = QAction(QIcon('document_action_icon.png'), 'Документи', self)
        documents_action.triggered.connect(self.open_documents_window)
        documents_menu.addAction(documents_action)
        menubar.addMenu(documents_menu)

        # Add the following code in the menubar section to create the Invoices menu
        invoices_menu = QMenu("Фактури", self)
        invoices_menu.setIcon(QIcon('invoice.png'))
        invoices_action = QAction(QIcon('invoice.png'), 'Фактури', self)
        invoices_action.triggered.connect(self.open_invoices_window)
        invoices_menu.addAction(invoices_action)
        menubar.addMenu(invoices_menu)

        # Create Settings menu
        settings_menu = QMenu("Настройки", self)
        settings_menu.setIcon(QIcon('setting.png'))
        settings_action = QAction(QIcon('setting.png'), 'Настройки', self)
        settings_action.triggered.connect(self.open_settings_window)
        settings_menu.addAction(settings_action)
        menubar.addMenu(settings_menu)

        # Create Help menu
        help_menu = QMenu("Помощ", self)
        help_menu.setIcon(QIcon('question.png'))
        help_action = QAction(QIcon('help.png'), 'Помощ', self)
        help_action.triggered.connect(self.open_help_window)
        help_menu.addAction(help_action)
        # Add Exit action to the Help menu
        exit_action = QAction("Изход", self)
        exit_action.triggered.connect(self.exit_program)
        help_menu.addAction(exit_action)
        menubar.addMenu(help_menu)

        # Frame 1 Contents
        frame1_layout = QHBoxLayout()
        frame1.setLayout(frame1_layout)

        self.input1 = QLineEdit()
        self.input1.setPlaceholderText("Име/баркод на продукта")
        self.input1.textChanged.connect(self.suggestions)
        frame1_layout.addWidget(self.input1, 3)  # Biggest

        self.suggestions_list = QListWidget()
        self.suggestions_list.setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.suggestions_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.suggestions_list.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.suggestions_list.setStyleSheet("QListWidget { background-color: white; border: 1px solid gray; }")
        self.suggestions_list.hide()
        frame1_layout.addWidget(self.suggestions_list)
        self.suggestions_list.itemClicked.connect(self.select_suggestion)

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.hide_suggestions)

        self.input2 = QLineEdit()
        self.input2.setPlaceholderText("Количество")
        frame1_layout.addWidget(self.input2, 1)  # Small

        self.input3 = QLineEdit()
        self.input3.setPlaceholderText("Ед. цена")
        frame1_layout.addWidget(self.input3, 1)  # Like the second

        self.popup_menu1 = QComboBox()
        self.popup_menu1.addItems(["А", "Б", "В", "Г"])
        frame1_layout.addWidget(self.popup_menu1, 2)  # A little bit more bigger

        self.add_button = QPushButton("Добави")
        self.add_button.setIcon(QIcon('ecommerce.png'))
        frame1_layout.addWidget(self.add_button, 2)  # Bigger

        # Frame 2 Contents
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Име", "К-во", "Ед. цена", "Дан. група", "Цена", "Изтрий"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        frame2_layout = QVBoxLayout()
        frame2.setLayout(frame2_layout)
        frame2_layout.addWidget(self.table)

        # Frame 3 Contents
        frame3_layout = QVBoxLayout()
        frame3.setLayout(frame3_layout)

        sub_frame1 = QFrame()
        sub_frame1.setFrameShape(QFrame.Shape.NoFrame)
        sub_frame1_layout = QVBoxLayout()
        sub_frame1.setLayout(sub_frame1_layout)
        image_label = QLabel()
        image_label.setPixmap(QPixmap('user.png'))
        image_label.setScaledContents(True)  # Scale the image to fit the label
        image_label.setMaximumSize(100,100)  # Set maximum size for the image label
        sub_frame1_layout.addWidget(image_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.image_text_label = QLabel("Оператор - 1")
        self.image_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text under the image
        sub_frame1_layout.addWidget(self.image_text_label)

        sub_frame2 = QFrame()
        sub_frame2.setFrameShape(QFrame.Shape.NoFrame)
        sub_frame2_layout = QVBoxLayout()
        sub_frame2.setLayout(sub_frame2_layout)
        self.popup_menu2 = QComboBox()
        self.popup_menu2.addItems(["В брой", "С карта", "По банка", "С ваучер"])
        sub_frame2_layout.addWidget(self.popup_menu2)
        button1 = QPushButton("Фискален бон")
        sub_frame2_layout.addWidget(button1)
        button2 = QPushButton("Ф-ра")
        sub_frame2_layout.addWidget(button2)

        sub_frame3 = QFrame()
        sub_frame3.setFrameShape(QFrame.Shape.NoFrame)
        sub_frame3_layout = QVBoxLayout()
        sub_frame3.setLayout(sub_frame3_layout)
        self.input4 = QLineEdit()
        self.input4.setPlaceholderText("Обща сума")
        sub_frame3_layout.addWidget(self.input4)
        button3 = QPushButton("X отчет")
        sub_frame3_layout.addWidget(button3)
        button4 = QPushButton("Z отчет")
        sub_frame3_layout.addWidget(button4)

        sub_frame4 = QFrame()
        sub_frame4.setFrameShape(QFrame.Shape.NoFrame)
        sub_frame4_layout = QVBoxLayout()
        sub_frame4.setLayout(sub_frame4_layout)
        self.input5 = QLineEdit()
        self.input5.setPlaceholderText("Платено")
        sub_frame4_layout.addWidget(self.input5)
        self.input6 = QLineEdit()
        self.input6.setPlaceholderText("Ресто")
        sub_frame4_layout.addWidget(self.input6)
        button5 = QPushButton("Служебен бон")
        sub_frame4_layout.addWidget(button5)
        # button6 = QPushButton("Button 6")
        # sub_frame4_layout.addWidget(button6)
        self.input5.textChanged.connect(self.update_change)
        button1.clicked.connect(self.save_to_database)


        frame3_sub_layout = QHBoxLayout()
        frame3_layout.addLayout(frame3_sub_layout)
        frame3_sub_layout.addWidget(sub_frame1)
        frame3_sub_layout.addWidget(sub_frame2)
        frame3_sub_layout.addWidget(sub_frame3)
        frame3_sub_layout.addWidget(sub_frame4)

        # Set equal stretch for sub-frames
        frame3_sub_layout.setStretch(0, 1)
        frame3_sub_layout.setStretch(1, 1)
        frame3_sub_layout.setStretch(2, 1)
        frame3_sub_layout.setStretch(3, 1)

        # Connect the add button to the function
        self.add_button.clicked.connect(self.add_to_table)

    def suggestions(self):
        text = self.input1.text()
        if text:
            connection = sqlite3.connect(DB_PATH)
            cursor = connection.cursor()
            cursor.execute('''
                SELECT name, barcode FROM products
                WHERE name LIKE ? OR barcode LIKE ?
            ''', ('%' + text + '%', '%' + text + '%'))
            suggestions = cursor.fetchall()
            connection.close()

            self.suggestions_list.clear()
            for suggestion in suggestions:
                self.suggestions_list.addItem(f"{suggestion[0]} ({suggestion[1]})")

            self.suggestions_list.show()
        else:
            self.suggestions_list.hide()

    def hide_suggestions(self):
        self.suggestions_list.hide()

    def update_operator_label(self, text):
        self.image_text_label.setText(text)

    def select_suggestion(self, item):
        text = item.text()
        name = text.split(' (')[0]
        self.input1.setText(name)
        self.suggestions_list.hide()

        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute('''
            SELECT unit_price FROM products
            WHERE name = ?
        ''', (name,))
        price = cursor.fetchone()
        connection.close()

        if price and price[0] != 0:
            self.input3.setText(str(price[0]))

    def update_totals(self):
        total_sum = 0
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 4)
            if item:
                total_sum += float(item.text())

        self.input4.setText(str(total_sum))
        self.input5.setText(str(total_sum))
        self.update_change()

    def update_change(self):
        try:
            total_sum = float(self.input4.text())
            paid_amount = float(self.input5.text())
            change = paid_amount - total_sum
        except ValueError:
            change = 0

        self.input6.setText(str(change))

    def save_to_database(self):
        products = []
        for row in range(self.table.rowCount()):
            product = {
                "Име": self.table.item(row, 0).text(),
                # "barcode": self.table.item(row, 1).text(),
                "К-во": float(self.table.item(row, 1).text()),
                "Ед. цена": float(self.table.item(row, 2).text()),
                "Обща цена": float(self.table.item(row, 4).text())
            }
            products.append(product)

        total_amount = float(self.input4.text())
        amount_paid = float(self.input5.text())
        change = float(self.input6.text())
        payment_type = self.popup_menu2.currentText()
        cash_register_numbers = ""

        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO documents (products, total_amount, amount_paid, change, payment_type, cash_register_numbers)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (json.dumps(products), total_amount, amount_paid, change, payment_type, cash_register_numbers))
        connection.commit()
        connection.close()

        self.table.setRowCount(0)
        self.input4.clear()
        self.input5.clear()
        self.input6.clear()

        msg = QMessageBox()
        # msg.setIcon(QIcon('add-to-basket.png'))
        msg.setText("Успешна продажба!")
        msg.setWindowTitle("Успешно")
        msg.exec()

    def add_to_table(self):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        input1_text = self.input1.text()
        input2_text = self.input2.text()
        input3_text = self.input3.text()
        popup_text = self.popup_menu1.currentText()

        self.table.setItem(row_position, 0, QTableWidgetItem(input1_text))
        self.table.setItem(row_position, 1, QTableWidgetItem(input2_text))
        self.table.setItem(row_position, 2, QTableWidgetItem(input3_text))
        self.table.setItem(row_position, 3, QTableWidgetItem(popup_text))

        try:
            multiplication_result = float(input2_text) * float(input3_text)
        except ValueError:
            multiplication_result = 0
        self.table.setItem(row_position, 4, QTableWidgetItem(str(multiplication_result)))

        delete_button = QPushButton()
        delete_button.setIcon(QIcon('trash_icon.png'))
        delete_button.clicked.connect(lambda: self.remove_row(row_position))
        self.table.setCellWidget(row_position, 5, delete_button)

        self.input1.clear()
        self.input2.clear()
        self.input3.clear()
        self.popup_menu1.setCurrentIndex(0)

        self.update_totals()

    def remove_row(self, row):
        self.table.removeRow(row)

    def open_cash_register_window(self):
        self.cash_register_window = CashRegisterWindow()
        self.cash_register_window.exec()

    def open_spravki_documents_window(self):
        self.spravki_documents_window = SpravkiDocumentsWindow()
        self.spravki_documents_window.exec()

    def open_spravki_clients_window(self):
        self.spravki_clients_window = SpravkiClientsWindow()
        self.spravki_clients_window.exec()

    def open_spravki_sales_window(self):
        self.spravki_sales_window = SpravkiSalesWindow()
        self.spravki_sales_window.exec()

    def open_settings_window(self):
        self.settings_window = SettingsWindow(self)
        self.settings_window.exec()

    def open_help_window(self):
        self.help_window = HelpWindow()
        self.help_window.exec()

    def open_new_window(self):
        self.new_window = ProductsWindow()
        self.new_window.exec()

    def open_customers_window(self):
        self.customers_window = CustomersWindow()
        self.customers_window.exec()

    def open_documents_window(self):
        self.documents_window = DocumentsWindow()
        self.documents_window.exec()

    def open_invoices_window(self):
        self.invoices_window = InvoicesWindow()
        self.invoices_window.exec()

    def exit_program(self):
        reply = QMessageBox.question(self, 'Exit', 'Are you sure you want to exit?',
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                    QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            QApplication.instance().quit()


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())
#
# if __name__ == "__main__":
#     app = QApplication([])
#
#     main_window = MainWindow()
#     login_window = LoginWindow()
#     login_window.show()
    # if login_window.close():
    #     main_window.show()
    # if login_window.exec() == QDialog.DialogCode.Accepted:
    #     app.exec()