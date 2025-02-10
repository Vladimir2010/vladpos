import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QHBoxLayout, QFileDialog
from PyQt6.QtGui import QIntValidator, QDoubleValidator, QPixmap
import psycopg2
from PyQt6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox
from PyQt6.QtGui import QPixmap
import psycopg2


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.edit_product_window = None
        self.new_product_window = NewProductWindow(self)  # Създаване на инстанция на прозореца
        self.setWindowTitle("POS система")
        self.setGeometry(100, 100, 800, 600)

        # ... (предходен код)

        menubar = self.menuBar()

        operations_menu = menubar.addMenu("Операции")
        # Тук ще добавим действия към меню "Операции"
        # ... (предходен код)
        spravki_menu = operations_menu.addMenu("Справки")
        spravki_menu.addAction("Нова справка")
        spravki_menu.addAction("Редактирай справка")

        new_product_action = QAction("Нов продукт", self)
        operations_menu.addAction(new_product_action)

        edit_product_action = QAction("Редактирай продукт", self)
        operations_menu.addAction(edit_product_action)

        # ... (предходен код)

        new_product_action.triggered.connect(self.open_new_product_window)
        edit_product_action.triggered.connect(self.edit_product)

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
