from PyQt6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog
from PyQt6.QtGui import QPixmap

class NewProductWindow(QDialog):
    def __init__(self, parent=None):
        # ... (предходен код)

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

        layout = QVBoxLayout()
        # ... (други елементи на интерфейса)
        layout.addLayout(image_layout)  # Добавяне на layout-а за снимката и бутона
        # ... (останал код)

    def upload_image(self):
        # Отваряне на диалогов прозорец за избиране на файл
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Изберете снимка", "", "Image Files (*.png *.jpg *.jpeg)", options=options)

        if file_path:
            # Зареждане на снимката и показване в QLabel
            pixmap = QPixmap(file_path)
            pixmap = pixmap.scaled(100, 100)  # Мащабиране на снимката до размера на QLabel
            self.image_label.setPixmap(pixmap)
            self.image_path = file_path  # Запазване на пътя към снимката

    def save_product(self):
        name = self.name_input.text()
        barcode = self.barcode_input.text()
        price = self.price_input.text()
        quantity = self.quantity_input.text()

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
                "dbname=pos_system user=postgres password=your_password")  # Заменете с вашите данни за връзка
            cur = conn.cursor()

            # Изпълнение на SQL заявка за вмъкване на нов продукт
            sql = "INSERT INTO продукти (име, баркод, цена, количество, снимка_път) VALUES (%s, %s, %s, %s, %s)"
            values = (name, barcode, price, quantity, image_path)
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
        self.quantity_input.setValidator(QIntValidator()) # Валидация за количество

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
            sql = "INSERT INTO products (name, barcode, price, quantity, description, image_path) VALUES (%s, %s, %s, %s, %s)"
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


















import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QAction, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox, QWidget, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QIntValidator, QDoubleValidator, QPixmap
import psycopg2

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("POS система")
        self.setGeometry(100, 100, 800, 600)

        menubar = self.menuBar()

        operations_menu = menubar.addMenu("Операции")

        work_with_products_action = QAction("Работа с продукти", self)
        operations_menu.addAction(work_with_products_action)
        work_with_products_action.triggered.connect(self.open_products_window)

        # ... (Други менюта и действия)

        self.products_window = ProductsWindow(self)  # Създаване на инстанция на прозореца за продукти

    def open_products_window(self):
        self.products_window.show()  # Показване на прозореца за продукти

    # ... (Други методи)


class ProductsWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Продукти")

        # Създаване на таблица за продуктите
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(5)  # Задайте броя на колоните според вашите нужди
        self.products_table.setHorizontalHeaderLabels(["ID", "Име", "Баркод", "Цена", "Количество"])  # Задаване на заглавия на колоните
        self.load_products()  # Зареждане на продуктите в таблицата

        # Създаване на бутони
        self.new_button = QPushButton("Нов")
        self.new_button.clicked.connect(self.open_new_product_window)

        self.edit_button = QPushButton("Редактирай")
        self.edit_button.clicked.connect(self.open_edit_product_window)

        # Създаване на поле за търсене
        self.search_input = QLineEdit()
        self.search_input.textChanged.connect(self.search_products)

        # Разположение на елементите
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.new_button)
        button_layout.addWidget(self.edit_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.search_input)
        main_layout.addWidget(self.products_table)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def load_products(self):
        try:
            conn = psycopg2.connect("dbname=pos_system user=postgres password=VA0885281774 host=localhost")  # Заменете с вашите данни за връзка
            cur = conn.cursor()

            sql = "SELECT id, name, barcode, price, quantity FROM products"
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


# ... (NewProductWindow и EditProductWindow класове)
