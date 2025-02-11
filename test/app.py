import sys
import os
import csv
import codecs
import psycopg2
import platform
import subprocess
import pandas as pd
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtGui import QIntValidator, QDoubleValidator
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
from PyQt6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox, QComboBox, QCheckBox
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog  # За работа с печат
from PyQt6.QtGui import QPainter  # За рисуване върху печатащия документ


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.edit_product_window = None
        self.new_product_window = NewProductWindow(self)  # Създаване на инстанция на прозореца
        self.setWindowTitle("POS система")
        self.setGeometry(100, 100, 1000, 700)
        self.products_window = ProductsWindow(self)
        self.products_table = ProductsWindow(self)# Създаване на инстанция на прозореца за продукти

        menubar = self.menuBar()

        operations_menu = menubar.addMenu("Операции")

        spravki_menu = operations_menu.addMenu("Справки")
        spravki_menu.addAction("Нова справка")
        spravki_menu.addAction("Редактирай справка")

        new_product_action = QAction("Нов продукт", self)
        operations_menu.addAction(new_product_action)

        edit_product_action = QAction("Редактирай продукт", self)
        operations_menu.addAction(edit_product_action)

        work_with_products_action = QAction("Работа с продукти", self)
        operations_menu.addAction(work_with_products_action)
        work_with_products_action.setShortcut("Ctrl+P")  # Задаване на клавишна комбинация Ctrl+P
        work_with_products_action.setStatusTip(
            "Отваря прозореца за управление на продуктите")  # Задаване на подсказка при задържане на мишката върху действието
        work_with_products_action.triggered.connect(self.open_products_window)

        new_product_action.triggered.connect(self.open_new_product_window)
        edit_product_action.triggered.connect(self.edit_product)

        # self.create_products_action()  # Извикване на метода за създаване на действието
        # products_menu = self.menuBar().addMenu("&Продукти")  # Създаване на меню "Продукти"
        # products_menu.addAction(self.products_action)  # Добавяне на действието към менюто




        other_operations_menu = menubar.addMenu("Други Операции:")
        # Тук ще добавим действия към меню "Други Операции"

        payment_menu = menubar.addMenu("Приключи:")
        # Тук ще добавим действия към меню "Приключи"

        documents_menu = menubar.addMenu("Избери документ:")
        # Тук ще добавим действия към меню "Избор на документ"

        settings_menu = menubar.addMenu("Настройки")
        # Тук ще добавим действия към меню "Настройки"

        help_menu = menubar.addMenu("Помощ")
        # Тук ще добавим действия към меню "Помощ"
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(4)  # Задайте броя на колоните според вашите нужди
        self.products_table.setHorizontalHeaderLabels(["Баркод", "Име", "Цена", "Количество"])  # Задаване на заглавия на колоните
        try:
            main_layout = QVBoxLayout()
            main_layout.addWidget(self.products_table)
            self.setLayout(main_layout)

            self.load_products()  # Зареждане на продуктите в таблицата
        except Exception as e:
            print(e)


    def open_products_window(self):
        self.products_window.exec()

    def open_new_product_window(self):
        result = self.new_product_window.exec()  # Показване на прозореца и очакване за резултат
        if result == QDialog.DialogCode.Accepted:  # Проверка дали е натиснат бутонът "Запази"
            print("Продуктът е запазен.")
        else:
            print("Действието е отказано.")

    def edit_product(self, product_id):
        try:
            self.edit_product_window = EditProductWindow(product_id, self)
            result = self.edit_product_window.exec()
            if result == QDialog.DialogCode.Accepted:
                # Обновяване на списъка с продукти
                self.load_products()  # Това е функция, която трябва да бъде дефинирана за зареждане на продуктите от базата данни
        except Exception as e:
            print(f"Грешка при редактиране на продукт: {e}")
            QMessageBox.critical(self, "Грешка", f"Възникна грешка при редактирането на продукта: {e}")
    # Тук ще добавим менюта, бутони и други елементи на интерфейса

    def create_products_action(self):
        self.products_action = QAction("&Продукти", self)  # Създаване на действие с текст "Продукти"
        self.products_action.setShortcut("Ctrl+P")  # Задаване на клавишна комбинация Ctrl+P
        self.products_action.setStatusTip(
            "Отваря прозореца за управление на продуктите")  # Задаване на подсказка при задържане на мишката върху действието
        self.products_action.triggered.connect(
            self.open_products_window)  # Свързване на сигнала triggered (кликване) с метода open_products_window

    def load_products(self):
        try:
            conn = psycopg2.connect(
                "dbname=pos_system user=postgres password=VA0885281774 host=localhost")  # Заменете с вашите данни за връзка
            cur = conn.cursor()

            sql = "SELECT id, name, barcode, price FROM products"  # SQL заявка за извличане на данните за продуктите
            cur.execute(sql)
            products = cur.fetchall()

            self.products_table.setRowCount(0)  # Изчистване на таблицата
            self.products_table.setColumnCount(5)  # Задаване на броя на колоните (id, name, barcode, price, image)
            self.products_table.setHorizontalHeaderLabels(
                ["ID", "Име", "Баркод", "Цена", "Картинка"])  # Задаване на заглавките на колоните

            for product in products:
                row_num = self.products_table.rowCount()
                self.products_table.insertRow(row_num)

                for i, data in enumerate(product):
                    item = QTableWidgetItem(str(data))  # Създаване на елемент от таблицата със стойността на данните
                    self.products_table.setItem(row_num, i, item)  # Добавяне на елемента към съответната клетка

                # Зареждане на картинката на продукта
                image_path = f"images/{product[2]}.jpg"  # Пътят до картинката на продукта (barcode.jpg)
                pixmap = QPixmap(image_path)  # Създаване на QPixmap от картинката
                icon = QIcon(pixmap)  # Създаване на QIcon от QPixmap

                image_item = QTableWidgetItem()  # Създаване на елемент за картинката
                image_item.setIcon(icon)  # Задаване на иконата на елемента
                self.products_table.setItem(row_num, 4,
                                            image_item)  # Добавяне на елемента с картинката към последната колона (image)

            cur.close()
            conn.close()

        except Exception as e:
            print(f"Грешка при зареждане на продукти: {e}")
            QMessageBox.critical(self, "Грешка", f"Възникна грешка при зареждането на продуктите: {e}")


class ProductsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.column_mapping = {
            0: "barcode",
            1: "name",
            2: "price",
            3: "quantity",
        }

        self.setWindowTitle("Продукти")
        self.setGeometry(100, 100, 800, 600)
        # self.setWindowIcoN("")

        # Създаване на таблица за продуктите
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(4)  # Задайте броя на колоните според вашите нужди
        self.products_table.setHorizontalHeaderLabels(["Баркод", "Име", "Цена", "Количество"])  # Задаване на заглавия на колоните
        self.load_products()  # Зареждане на продуктите в таблицата

        # Създаване на бутони
        self.new_button = QPushButton("Нов")
        self.new_button.clicked.connect(self.open_new_product_window)

        self.edit_button = QPushButton("Редактирай")
        self.edit_button.clicked.connect(self.open_edit_product_window)

        # Създаване на бутон "Изтрий"
        self.delete_button = QPushButton("Изтрий")
        self.delete_button.clicked.connect(self.delete_product)

        # Създаване на бутон "Обнови"
        self.refresh_button = QPushButton("Обнови")
        self.refresh_button.clicked.connect(self.load_products)

        self.print_button = QPushButton("Отпечатване")
        self.print_button.clicked.connect(self.print_table)


        # Създаване на поле за търсене
        self.search_input = QLineEdit()
        self.search_input.textChanged.connect(self.search_products)

        # Създаване на падащо меню за критерий за сортиране
        self.sort_criterion_combo = QComboBox()
        self.sort_criterion_combo.addItems(["Име", "Цена", "Количество"])  # Добавяне на възможните критерии
        self.sort_criterion_combo.currentIndexChanged.connect(self.sort_products)  # Свързване на сигнала currentIndexChanged с функцията за сортиране

        # Създаване на падащо меню за посока на сортиране
        self.sort_direction_combo = QComboBox()
        self.sort_direction_combo.addItems(["Възходящо", "Низходящо"])  # Добавяне на възможните посоки
        self.sort_direction_combo.currentIndexChanged.connect(self.sort_products)  # Свързване на сигнала currentIndexChanged с функцията за сортиране

        # Създаване на бутон "Импортиране"
        self.import_button = QPushButton("Импортиране")
        self.import_button.clicked.connect(self.import_from_csv)

        # Създаване на бутон "Изтрий избраните"
        self.delete_selected_button = QPushButton("Изтрий избраните")
        self.delete_selected_button.clicked.connect(self.delete_selected_products)

        # Създаване на полета за филтриране
        self.name_filter_input = QLineEdit()
        self.name_filter_input.textChanged.connect(
            self.filter_products)  # Свързване на сигнала textChanged с функцията за филтриране

        self.barcode_filter_input = QLineEdit()
        self.barcode_filter_input.textChanged.connect(self.filter_products)

        self.price_filter_input = QLineEdit()
        self.price_filter_input.textChanged.connect(self.filter_products)

        self.quantity_filter_input = QLineEdit()
        self.quantity_filter_input.textChanged.connect(self.filter_products)

        # Добавяне на полетата за филтриране към layout-а
        filter_layout = QVBoxLayout()
        filter_layout.addWidget(QLabel("Име:"))
        filter_layout.addWidget(self.name_filter_input)
        filter_layout.addWidget(QLabel("Баркод:"))
        filter_layout.addWidget(self.barcode_filter_input)
        filter_layout.addWidget(QLabel("Цена:"))
        filter_layout.addWidget(self.price_filter_input)
        filter_layout.addWidget(QLabel("Количество:"))
        filter_layout.addWidget(self.quantity_filter_input)

        # Добавяне на падащите менюта към layout-а
        sort_layout = QHBoxLayout()
        sort_layout.addWidget(self.sort_criterion_combo)
        sort_layout.addWidget(self.sort_direction_combo)

        # Създаване на бутон "Експортиране"
        self.export_button = QPushButton("Експортиране")
        self.export_button.clicked.connect(self.export_to_csv)

        # Свързване на сигнала cellDoubleClicked с функцията за редактиране
        self.products_table.cellDoubleClicked.connect(self.edit_selected_product)

        # Разположение на елементите
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.new_button)
        button_layout.addWidget(self.edit_button)
        # Добавяне на бутона "Изтрий" към layout-а
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.refresh_button)
        # Добавяне на бутона "Отпечатване" към layout-а
        button_layout.addWidget(self.print_button)
        button_layout.addWidget(self.export_button)
        # Добавяне на бутона "Импортиране" към layout-а
        button_layout.addWidget(self.import_button)
        # Добавяне на бутона "Изтрий избраните" към layout-а
        button_layout.addWidget(self.delete_selected_button)




        main_layout = QVBoxLayout()
        main_layout.addWidget(self.search_input)
        main_layout.addWidget(self.products_table)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(sort_layout)
        main_layout.addLayout(filter_layout)



        self.setLayout(main_layout)


        self.all_products = []  # Създаване на празен списък за оригиналните данни

    def load_products(self):
        try:
            conn = psycopg2.connect("dbname=pos_system user=postgres password=VA0885281774 host=localhost")  # Заменете с вашите данни за връзка
            cur = conn.cursor()

            sql = "SELECT barcode, name, price, quantity FROM products"
            cur.execute(sql)
            products = cur.fetchall()
            self.all_products = []  # Изчистване на списъка с оригиналните данни

            self.products_table.setRowCount(0) # Изчистване на таблицата
            # self.products_table.insertColumn(0)
            for product in products:
                row_num = self.products_table.rowCount()
                self.products_table.insertRow(row_num)
                # checkbox = QCheckBox()
                # self.products_table.setCellWidget(row_num, 0, checkbox)  # Добавяне на checkbox към първата колона
                product_data = {}  # Речник за съхранение на данните за продукта
                for i, data in enumerate(product):
                    item = QTableWidgetItem(str(data))
                    self.products_table.setItem(row_num, i, item) #i+1
                    product_data[self.column_mapping[i]] = data  # Добавяне на данните в речника

                self.all_products.append(product_data)  # Добавяне на данните за продукта към списъка с оригиналните данни

                # Задаване на подравняване вдясно за елементите от колоните с цена и количество
                item = self.products_table.item(row_num, 0)  # Вземане на елемента от колоната с баркода
                item.setTextAlignment(
                    Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)  # Задаване на подравняване вдясно и вертикално центриране
                item = self.products_table.item(row_num, 2)  # Вземане на елемента от колоната с цена
                item.setTextAlignment(
                    Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)  # Задаване на подравняване вдясно и вертикално центриране

                item = self.products_table.item(row_num, 3)  # Вземане на елемента от колоната с количество
                item.setTextAlignment(
                    Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)  # Задаване на подравняване вдясно и вертикално центриране

            cur.close()
            conn.close()
            self.products_table.setColumnWidth(1, 200)  # Увеличава ширината на втората колона (индекс 1) на 200 пиксела

        except Exception as e:
            print(f"Грешка при зареждане на продукти: {e}")
            QMessageBox.critical(self, "Грешка", f"Възникна грешка при зареждането на продуктите: {e}")

    def open_new_product_window(self):
        self.new_product_window = NewProductWindow(self)
        result = self.new_product_window.exec()
        if result == QDialog.DialogCode.Accepted:
            self.load_products()

    def open_edit_product_window(self):
        selected_rows = self.products_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Грешка", "Моля, изберете продукт за редактиране.")
            return

        product_id = int(selected_rows[0].text())  # Вземане на ID на продукта от избрания ред

        self.edit_product_window = EditProductWindow(product_id, self)
        result = self.edit_product_window.exec()
        if result == QDialog.DialogCode.Accepted:
            self.load_products()

    def search_products(self, text):
        try:
            conn = psycopg2.connect("dbname=pos_system user=postgres password=VA0885281774 host=localhost")  # Заменете с вашите данни за връзка
            cur = conn.cursor()

            sql = "SELECT id, name, barcode, price, quantity FROM products WHERE name ILIKE %s"  # Търсене по име (ILIKE е case-insensitive)
            cur.execute(sql, ('%' + text + '%',))  # Добавяне на wildcard символи (%) за търсене на подstring
            products = cur.fetchall()

            self.products_table.setRowCount(0)  # Изчистване на таблицата
            for product in products:
                row_num = self.products_table.rowCount()
                self.products_table.insertRow(row_num)
                for i, data in enumerate(product):
                    item = QTableWidgetItem(str(data))
                    self.products_table.setItem(row_num, i, item)

            cur.close()
            conn.close()

        except Exception as e:
            print(f"Грешка при търсене на продукти: {e}")
            QMessageBox.critical(self, "Грешка", f"Възникна грешка при търсенето на продуктите: {e}")

    def sort_products(self):
        try:
            conn = psycopg2.connect(
                "dbname=pos_system user=postgres password=VA0885281774 host=localhost")  # Заменете с вашите данни за връзка
            cur = conn.cursor()

            # Вземане на избрания критерий и посока на сортиране
            criterion = self.sort_criterion_combo.currentText()
            direction = self.sort_direction_combo.currentText()

            # Изпълнение на SQL заявка за сортиране на продуктите
            if criterion == "Име":
                sql = "SELECT barcode, name, price, quantity FROM products ORDER BY name "
            elif criterion == "Цена":
                sql = "SELECT barcode, name, price, quantity FROM products ORDER BY price "
            elif criterion == "Количество":
                sql = "SELECT barcode, name, price, quantity FROM products ORDER by quantity "

            if direction == "Низходящо":
                sql += "DESC"

            cur.execute(sql)
            products = cur.fetchall()

            self.products_table.setRowCount(0)  # Изчистване на таблицата
            for product in products:
                row_num = self.products_table.rowCount()
                self.products_table.insertRow(row_num)
                for i, data in enumerate(product):
                    item = QTableWidgetItem(str(data))
                    self.products_table.setItem(row_num, i, item)

            cur.close()
            conn.close()

        except Exception as e:
            print(f"Грешка при сортиране на продукти: {e}")
            QMessageBox.critical(self, "Грешка", f"Възникна грешка при сортирането на продуктите: {e}")

    def filter_products(self):
        try:
            # Вземане на текста от полетата за филтриране
            name_filter = self.name_filter_input.text().lower()
            barcode_filter = self.barcode_filter_input.text().lower()
            price_filter = self.price_filter_input.text()
            quantity_filter = self.quantity_filter_input.text()

            # Филтриране на данните
            filtered_products = []
            for product in self.all_products:
                print(type(product["price"]))
                # Използваме копие на оригиналните данни
                if (name_filter in product["name"].lower() and
                        barcode_filter in product["barcode"].lower() and
                        (not price_filter or str(product["price"]) == price_filter) and
                        (not quantity_filter or str(product["quantity"]) == quantity_filter)):
                    filtered_products.append(product)
                print(product["price"])

            # Обновяване на таблицата
            self.products_table.setRowCount(0)  # Изчистване на таблицата
            for product in filtered_products:
                row_num = self.products_table.rowCount()
                self.products_table.insertRow(row_num)
                for i, (col_name, value) in enumerate(product.items()):
                    item = QTableWidgetItem(str(value))
                    self.products_table.setItem(row_num, i, item)

        except Exception as e:
            print(f"Грешка при филтриране на продукти: {e}")
            QMessageBox.critical(self, "Грешка", f"Възникна грешка при филтрирането на продуктите: {e}")

    def print_table(self):
        try:
            # Създаване на печатащ документ
            printer = QPrinter()

            # Създаване на диалогов прозорец за настройка на печат
            print_dialog = QPrintDialog(printer, self)
            if print_dialog.exec() == QPrintDialog.DialogCode.Accepted:
                # Създаване на painter за рисуване върху печатащия документ
                painter = QPainter(printer)

                # Рисуване на данните от таблицата
                self.products_table.render(painter)

                painter.end()

        except Exception as e:
            print(f"Грешка при отпечатване на таблицата: {e}")
            QMessageBox.critical(self, "Грешка", f"Възникна грешка при отпечатването на таблицата: {e}")

    # def validate_data(self, row_data):
    #     try:
    #         # Проверка за празни полета
    #         if not row_data["name"]:
    #             raise ValueError("Полето 'име' е задължително.")
    #         if not row_data["barcode"]:
    #             raise ValueError("Полето 'баркод' е задължително.")
    #         if not row_data["price"]:
    #             raise ValueError("Полето 'цена' е задължително.")
    #         if not row_data["quantity"]:
    #             raise ValueError("Полето 'количество' е задължително.")
    #
    #         # Проверка за валидни типове данни
    #         float(row_data["price"])  # Проверка дали цената е число
    #         int(row_data["quantity"])  # Проверка дали количеството е цяло число
    #
    #         return True  # Данните са валидни
    #
    #     except ValueError as e:
    #         QMessageBox.warning(self, "Грешка при валидиране", str(e))
    #         return False  # Данните не са валидни

    def import_from_csv(self):
        try:
            # Отваряне на диалогов прозорец за избор на файл
            file_path, _ = QFileDialog.getOpenFileName(self, "Избор на CSV файл", "", "CSV Files (*.csv)")

            if file_path:
                # Четене на данните от CSV файла
                with open(file_path, "r", encoding="utf-8-sig") as csvfile:
                    reader = csv.DictReader(csvfile)  # Използване на DictReader за четене на данни по колони
                    data = list(reader)

                # Добавяне на данните към таблицата
                self.products_table.setRowCount(0)  # Изчистване на таблицата преди добавяне на нови данни
                for row_data in data:
                    row_num = self.products_table.rowCount()
                    self.products_table.insertRow(row_num)
                    for col_name, value in row_data.items():
                        col_index = list(self.column_mapping.keys())[list(self.column_mapping.values()).index(
                            col_name)]  # Намиране на индекса на колоната по име
                        item = QTableWidgetItem(value)
                        self.products_table.setItem(row_num, col_index, item)

                QMessageBox.information(self, "Успех", "Данните са успешно импортирани от CSV файл.")

                # Питаме потребителя дали иска да запази данните в базата данни
                reply = QMessageBox.question(self, "Запазване в база данни", "Желаете ли да запазите импортираните данни в базата данни?",
                                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

                if reply == QMessageBox.StandardButton.Yes:
                    try:
                        conn = psycopg2.connect("dbname=pos_system user=postgres password=VA0885281774 host=localhost")  # Заменете с вашите данни за връзка
                        cur = conn.cursor()

                        # Проверяваме дали записите вече съществуват и добавяме само новите
                        for row_data in data:
                        #     if not self.validate_data(row_data):
                        #         continue  # Преминаваме към следващия запис, ако данните не са валидни
                            # Изграждаме SQL заявка за проверка дали записът вече съществува
                            check_sql = "SELECT id FROM products WHERE barcode = %s"  # Проверяваме по баркод, можете да промените критерия
                            cur.execute(check_sql, (row_data["barcode"],))
                            existing_product = cur.fetchone()

                            if existing_product is None:  # Ако записът не съществува, го добавяме
                                # Изграждаме SQL заявка за добавяне на нов запис
                                insert_sql = "INSERT INTO products (name, barcode, price, quantity) VALUES (%s, %s, %s, %s)"  # Адаптирайте колоните според вашите нужди
                                values = (row_data["name"], row_data["barcode"], row_data["price"], row_data["quantity"])  # Адаптирайте данните според вашите нужди
                                cur.execute(insert_sql, values)

                        conn.commit()
                        cur.close()
                        conn.close()

                        QMessageBox.information(self, "Успех", "Данните са успешно запазени в базата данни.")
                        self.load_products()  # Обновяваме таблицата с продуктите след импортирането и запазването
                    except Exception as e:
                        print(f"Грешка при запазване в базата данни: {e}")
                        conn.rollback()  # Откатваме транзакцията в случай на грешка
                        QMessageBox.critical(self, "Грешка", f"Възникна грешка при запазването на данните в базата данни: {e}")


        except Exception as e:
            print(f"Грешка при импортиране от CSV файл: {e}")
            QMessageBox.critical(self, "Грешка", f"Възникна грешка при импортирането на данните от CSV файл: {e}")

    def export_to_csv(self):
        try:
            # Получаване на данните от таблицата, включително заглавките на колоните
            headers = [self.products_table.horizontalHeaderItem(i).text() for i in
                       range(self.products_table.columnCount())]
            data = []
            for row in range(self.products_table.rowCount()):
                row_data = {}  # Променяме на речник, за да запазим реда на колоните
                for col in range(self.products_table.columnCount()):
                    item = self.products_table.item(row, col)
                    if item is not None:
                        column_name = self.column_mapping[col]  # Вземаме името на колоната от речника
                        row_data[column_name] = item.text()
                    else:
                        column_name = self.column_mapping[col]
                        row_data[column_name] = ""  # Добавяне на празен низ, ако клетката е празна
                data.append(row_data)
                print(data)

            # Отваряне на диалогов прозорец за запазване на файл
            file_path, _ = QFileDialog.getSaveFileName(self, "Запазване на CSV файл", "", "CSV Files (*.csv)")

            if file_path:
                # Запис на данните в CSV файла с UTF-8 кодиране и BOM
                with open(file_path, "w", newline="", encoding="utf-8-sig") as csvfile:
                    fieldnames = list(self.column_mapping.values()) # Вземаме имената на колоните от речника
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=",", quoting=csv.QUOTE_NONNUMERIC)
                    writer.writeheader() # Запис на заглавките на колоните
                    writer.writerows(data)  # Запис на данните

                QMessageBox.information(self, "Успех", "Данните са успешно експортирани в CSV файл.")
                os_name = platform.system()
                # Питаме потребителя дали иска да отвори файла
                reply = QMessageBox.question(self, "Отваряне на файл", "Искате ли да отворите файла?",
                                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

                if reply == QMessageBox.StandardButton.Yes:
                    # Отваряне на файла в зависимост от операционната система
                    if os_name == "Windows":
                        os.startfile(file_path)
                    elif os_name == "Darwin":  # macOS
                        subprocess.Popen(['open', file_path])
                    elif os_name == "Linux":
                        subprocess.Popen(['xdg-open', file_path])
                    else:
                        QMessageBox.warning(self, "Грешка", "Неподдържана операционна система.")

        except Exception as e:
            print(f"Грешка при експортиране в CSV файл: {e}")
            QMessageBox.critical(self, "Грешка", f"Възникна грешка при експортирането на данните в CSV файл: {e}")

    def edit_selected_product(self, row, column):
                try:
                    # Вземане на ID на избрания продукт
                    product_id = int(self.products_table.item(row, 0).text())

                    # Отваряне на прозореца за редактиране на продукт
                    self.edit_product_window = EditProductWindow(product_id, self)
                    result = self.edit_product_window.exec()

                    # Обновяване на таблицата с продуктите, ако потребителят е запазил промените
                    if result == QDialog.DialogCode.Accepted:
                        self.load_products()

                except Exception as e:
                    print(f"Грешка при отваряне на прозореца за редактиране: {e}")
                    QMessageBox.critical(self, "Грешка",
                                         f"Възникна грешка при отварянето на прозореца за редактиране: {e}")

    def delete_product(self):
        selected_items = self.products_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Грешка", "Моля, изберете продукт за изтриване.")
            return

        product_id = int(selected_items[0].text())

        reply = QMessageBox.question(self, "Потвърждение", "Сигурни ли сте, че искате да изтриете този продукт?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            try:
                conn = psycopg2.connect(
                    "dbname=pos_system user=postgres password=VA0885281774 host=localhost")  # Заменете с вашите данни за връзка
                cur = conn.cursor()

                sql = "DELETE FROM products WHERE id = %s"
                cur.execute(sql, (product_id,))

                conn.commit()
                cur.close()
                conn.close()

                self.load_products()  # Обновяване на таблицата с продуктите

                QMessageBox.information(self, "Успех", "Продуктът е успешно изтрит.")

            except Exception as e:
                print(f"Грешка при изтриване на продукт: {e}")
                QMessageBox.critical(self, "Грешка", f"Възникна грешка при изтриването на продукта: {e}")

    def delete_selected_products(self):
        try:
            # Вземане на избраните продукти
            selected_products = []
            for row in range(self.products_table.rowCount()):
                checkbox = self.products_table.cellWidget(row, 0)
                if checkbox.isChecked():
                    product_id = int(self.products_table.item(row, 1).text())  # ID-то е във втората колона (индекс 1)
                    selected_products.append(product_id)

            if not selected_products:
                QMessageBox.warning(self, "Грешка", "Моля, изберете продукти за изтриване.")
                return

            # Показване на диалогов прозорец за потвърждение на изтриването
            reply = QMessageBox.question(self, "Потвърждение",
                                         "Сигурни ли сте, че искате да изтриете избраните продукти?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes:
                try:
                    conn = psycopg2.connect(
                        "dbname=pos_system user=postgres password=VA0885281774 host=localhost")  # Заменете с вашите данни за връзка
                    cur = conn.cursor()

                    # Изтриване на избраните продукти от базата данни
                    for product_id in selected_products:
                        sql = "DELETE FROM products WHERE id = %s"
                        cur.execute(sql, (product_id,))

                    conn.commit()
                    cur.close()
                    conn.close()

                    self.load_products()  # Обновяване на таблицата с продуктите

                    QMessageBox.information(self, "Успех", "Избраните продукти са успешно изтрити.")

                except Exception as e:
                    print(f"Грешка при изтриване на продукти: {e}")
                    QMessageBox.critical(self, "Грешка", f"Възникна грешка при изтриването на продуктите: {e}")

        except Exception as e:
            print(f"Грешка при изтриване на продукти: {e}")
            QMessageBox.critical(self, "Грешка", f"Възникна грешка при изтриването на продуктите: {e}")


class NewProductWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Нов продукт")

        # Създаване на полета за въвеждане на данни
        self.name_label = QLabel("Име:")
        self.name_input = QLineEdit()

        self.barcode_label = QLabel("Баркод:")
        self.barcode_input = QLineEdit()

        self.price_label = QLabel("Цена:")
        self.price_input = QLineEdit()
        self.price_input.setValidator(QDoubleValidator())  # Валидация за цена

        self.quantity_label = QLabel("Количество:")
        self.quantity_input = QLineEdit()
        self.quantity_input.setValidator(QIntValidator())  # Валидация за количество

        # Създаване на полета за въвеждане на описание
        self.description_label = QLabel("Описание:")
        self.description_input = QLineEdit()

        # Създаване на QLabel за показване на снимката
        self.image_label = QLabel()
        self.image_label.setFixedSize(100, 100)  # Задаване на фиксиран размер за QLabel
        self.image_label.setStyleSheet("border: 1px solid black;")  # Добавяне на рамка към QLabel

        # Създаване на бутон за избиране на снимка
        self.upload_button = QPushButton("Качи снимка")
        self.upload_button.clicked.connect(self.upload_image)

        # Разположение на елементите в прозореца
        image_layout = QHBoxLayout()
        image_layout.addWidget(self.image_label)
        image_layout.addWidget(self.upload_button)

        # Създаване на бутон за запазване
        self.save_button = QPushButton("Запази")
        self.save_button.clicked.connect(self.save_product)

        # Създаване на бутон за отказ
        self.cancel_button = QPushButton("Отказ")
        self.cancel_button.clicked.connect(self.close)

        # Разположение на елементите в прозореца
        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.barcode_label)
        layout.addWidget(self.barcode_input)
        layout.addWidget(self.price_label)
        layout.addWidget(self.price_input)
        layout.addWidget(self.quantity_label)
        layout.addWidget(self.quantity_input)
        layout.addWidget(self.description_label)
        layout.addWidget(self.description_input)
        layout.addWidget(self.save_button)
        layout.addWidget(self.cancel_button)
        layout.addLayout(image_layout)  # Добавяне на layout-а за снимката и бутона
        self.setLayout(layout)

    def upload_image(self):
        try:
            # Отваряне на диалогов прозорец за избиране на файл
            # options = QFileDialog.Options()
            file_path, _ = QFileDialog.getOpenFileName(self, "Изберете снимка", "", "Image Files (*.png *.jpg *.jpeg)")

            if file_path:
                # Зареждане на снимката и показване в QLabel
                pixmap = QPixmap(file_path)
                pixmap = pixmap.scaled(100, 100)  # Мащабиране на снимката до размера на QLabel
                self.image_label.setPixmap(pixmap)
                self.image_path = file_path  # Запазване на пътя към снимката
        except Exception as e:
            print(f"Грешка при качване на снимка: {e}")
            QMessageBox.critical(self, "Грешка", f"Възникна грешка при качването на снимката: {e}")

    def save_product(self):
        # Тук ще добавим код за запазване на продукта в базата данни
        name = self.name_input.text()
        barcode = self.barcode_input.text()
        price = self.price_input.text()
        quantity = self.quantity_input.text()
        description = self.description_input.text()

        if not name or not barcode or not price or not quantity:
            QMessageBox.warning(self, "Грешка", "Моля, попълнете всички полета.")
            return

        try:
            price = float(price)
            quantity = int(quantity)
        except ValueError:
            QMessageBox.warning(self, "Грешка", "Невалидни данни за цена или количество.")
            return

        # Запазване на пътя към снимката в базата данни
        if hasattr(self, 'image_path'):
            image_path = self.image_path
        else:
            image_path = None

        try:
            # Свързване с базата данни
            conn = psycopg2.connect(
                "dbname=pos_system user=postgres password=VA0885281774")  # Заменете с вашите данни за връзка
            cur = conn.cursor()

            # Изпълнение на SQL заявка за вмъкване на нов продукт
            sql = "INSERT INTO products (name, barcode, price, quantity, description, image_path) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (name, barcode, price, quantity, description, image_path)
            cur.execute(sql, values)

            # Запис на промените в базата данни
            conn.commit()

            # Затваряне на връзката с базата данни
            cur.close()
            conn.close()

            QMessageBox.information(self, "Успех", "Продуктът е успешно добавен.")
            self.accept()  # Затваря прозореца след успешно запазване

        except Exception as e:
            print(f"Грешка при запазване на продукта: {e}")
            QMessageBox.critical(self, "Грешка", f"Възникна грешка при запазването на продукта: {e}")


class EditProductWindow(QDialog):
    def __init__(self, product_id, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Редактиране на продукт")
        self.product_id = product_id  # Запазване на ID на продукта

        # Създаване на полета за въвеждане на данни
        self.name_label = QLabel("Име:")
        self.name_input = QLineEdit()

        self.barcode_label = QLabel("Баркод:")
        self.barcode_input = QLineEdit()

        self.price_label = QLabel("Цена:")
        self.price_input = QLineEdit()
        self.price_input.setValidator(QDoubleValidator())  # Валидация за цена

        self.quantity_label = QLabel("Количество:")
        self.quantity_input = QLineEdit()
        self.quantity_input.setValidator(QIntValidator()) # Валидация за количество

        # Създаване на полета за въвеждане на описание
        self.description_label = QLabel("Описание:")
        self.description_input = QLineEdit()

        # Създаване на QLabel за показване на снимката
        self.image_label = QLabel()
        self.image_label.setFixedSize(100, 100)
        self.image_label.setStyleSheet("border: 1px solid black;")


        # Създаване на бутон за избиране на снимка
        self.upload_button = QPushButton("Качи снимка")
        self.upload_button.clicked.connect(self.upload_image)

        # Разположение на елементите в прозореца
        image_layout = QHBoxLayout()
        image_layout.addWidget(self.image_label)
        image_layout.addWidget(self.upload_button)


        # Създаване на бутон за запазване
        self.save_button = QPushButton("Запази")
        self.save_button.clicked.connect(self.save_product)

        # Създаване на бутон за отказ
        self.cancel_button = QPushButton("Отказ")
        self.cancel_button.clicked.connect(self.close)

        # Разположение на елементите в прозореца
        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.barcode_label)
        layout.addWidget(self.barcode_input)
        layout.addWidget(self.price_label)
        layout.addWidget(self.price_input)
        layout.addWidget(self.quantity_label)
        layout.addWidget(self.quantity_input)
        layout.addWidget(self.description_label)
        layout.addWidget(self.description_input)
        layout.addWidget(self.save_button)
        layout.addWidget(self.cancel_button)
        layout.addLayout(image_layout)  # Добавяне на layout-а за снимката и бутона
        self.setLayout(layout)
        # Зареждане на информацията за продукта от базата данни
        self.load_product_data()

    def load_product_data(self):
        try:
            conn = psycopg2.connect(
                "dbname=pos_system user=postgres password=VA0885281774")  # Заменете с вашите данни за връзка
            cur = conn.cursor()

            # Изпълнение на SQL заявка за извличане на информация за продукта
            sql = "SELECT name, barcode, price, quantity, description, image_path FROM products WHERE id = %s"
            cur.execute(sql, (self.product_id,))
            product_data = cur.fetchone()

            if product_data:
                name, barcode, price, quantity, description, image_path = product_data

                self.name_input.setText(name)
                self.barcode_input.setText(barcode)
                self.price_input.setText(str(price))
                self.quantity_input.setText(str(quantity))
                self.description_input.setText(description)

                if image_path:
                    pixmap = QPixmap(image_path)
                    pixmap = pixmap.scaled(100, 100)
                    self.image_label.setPixmap(pixmap)
                    self.image_path = image_path
            else:
                QMessageBox.warning(self, "Грешка", "Продуктът не е намерен.")
                self.close()

            cur.close()
            conn.close()

        except Exception as e:
            print(f"Грешка при зареждане на данни за продукта: {e}")
            QMessageBox.critical(self, "Грешка", f"Възникна грешка при зареждането на данните за продукта: {e}")

    def upload_image(self):
        try:
            # Отваряне на диалогов прозорец за избиране на файл
            # options = QFileDialog.Options()
            file_path, _ = QFileDialog.getOpenFileName(self, "Изберете снимка", "", "Image Files (*.png *.jpg *.jpeg)")

            if file_path:
                # Зареждане на снимката и показване в QLabel
                pixmap = QPixmap(file_path)
                pixmap = pixmap.scaled(100, 100)  # Мащабиране на снимката до размера на QLabel
                self.image_label.setPixmap(pixmap)
                self.image_path = file_path  # Запазване на пътя към снимката
        except Exception as e:
            print(f"Грешка при качване на снимка: {e}")
            QMessageBox.critical(self, "Грешка", f"Възникна грешка при качването на снимката: {e}")

    def save_product(self):
        # Тук ще добавим код за запазване на продукта в базата данни
        name = self.name_input.text()
        barcode = self.barcode_input.text()
        price = self.price_input.text()
        quantity = self.quantity_input.text()
        description = self.description_input.text()

        if hasattr(self, 'image_path'):
            image_path = self.image_path
        else:
            image_path = None
        try:
            # Свързване с базата данни
            conn = psycopg2.connect(
                "dbname=pos_system user=postgres password=VA0885281774 host=localhost")  # Заменете с вашите данни за връзка
            cur = conn.cursor()

            # Изпълнение на SQL заявка за актуализиране на информацията за продукта
            sql = "UPDATE products SET name = %s, barcode = %s, price = %s, quantity = %s, description = %s, image_path = %s WHERE id = %s"
            values = (name, barcode, price, quantity, description, image_path, self.product_id)
            cur.execute(sql, values)

            conn.commit()
            cur.close()
            conn.close()

            QMessageBox.information(self, "Успех", "Продуктът е успешно редактиран.")
            self.accept()

        except Exception as e:
            print(f"Грешка при редактиране на продукта: {e}")
            QMessageBox.critical(self, "Грешка", f"Възникна грешка при редактирането на продукта: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
