import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import datetime
import serial
import serial.tools.list_ports
from PIL import Image, ImageTk  # За работа с изображения

class POSSystem:
    def __init__(self, master):
        self.master = master
        master.title("POS Система")

        # База данни
        self.conn = sqlite3.connect('post.db')
        self.cursor = self.conn.cursor()
        self.create_tables()

        # Променливи
        self.cart_items = []
        self.total_price = 0

        # Интерфейс
        self.create_widgets()
        self.create_menu()

    def create_menu(self):
        menubar = tk.Menu(self.master)

        # Файл
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Изход", command=self.exit_app)
        menubar.add_cascade(label="Файл", menu=file_menu)

        # Продукти
        product_menu = tk.Menu(menubar, tearoff=0)
        product_menu.add_command(label="Добави", command=self.add_product)
        product_menu.add_command(label="Редактирай", command=self.edit_product)
        product_menu.add_command(label="Изтрий", command=self.delete_product)
        menubar.add_cascade(label="Продукти", menu=product_menu)

        # Настройки
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Настройки на касов апарат", command=self.configure_cash_register)
        menubar.add_cascade(label="Настройки", menu=settings_menu)

        # Помощ
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Помощ", command=self.show_help)
        help_menu.add_command(label="За програмата", command=self.show_about)
        menubar.add_cascade(label="Помощ", menu=help_menu)

        self.master.config(menu=menubar)

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS продукти (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                име TEXT NOT NULL,
                цена REAL NOT NULL,
                баркод TEXT UNIQUE,
                път_към_изображение TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS продажби (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                дата TEXT NOT NULL,
                час TEXT NOT NULL,
                продукти TEXT NOT NULL,
                обща_сума REAL NOT NULL,
                вид_плащане TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def create_widgets(self):
        # Продуктов панел
        product_frame = ttk.LabelFrame(self.master, text="Продукти")
        product_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.product_canvas = tk.Canvas(product_frame)
        self.product_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar_y = ttk.Scrollbar(product_frame, command=self.product_canvas.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.product_canvas.config(yscrollcommand=scrollbar_y.set)

        scrollbar_x = ttk.Scrollbar(product_frame, command=self.product_canvas.xview, orient=tk.HORIZONTAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.product_canvas.config(xscrollcommand=scrollbar_x.set)

        self.product_canvas.config(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        self.load_products()

        # Кошница
        cart_frame = ttk.LabelFrame(self.master, text="Кошница")
        cart_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.cart_list = tk.Listbox(cart_frame, width=40)
        self.cart_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(cart_frame, command=self.cart_list.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.cart_list.config(yscrollcommand=scrollbar.set)

        # Баркод
        barcode_frame = ttk.LabelFrame(self.master, text="Баркод")
        barcode_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.barcode_entry = ttk.Entry(barcode_frame)
        self.barcode_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        self.barcode_entry.bind("<Return>", self.add_product_by_barcode)

        # Бутони
        button_frame = ttk.Frame(self.master)
        button_frame.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        pay_cash_button = ttk.Button(button_frame, text="Плащане в брой", command=lambda: self.pay("cash"))
        pay_cash_button.pack(side=tk.LEFT, padx=5)

        pay_card_button = ttk.Button(button_frame, text="Плащане с карта", command=lambda: self.pay("card"))
        pay_card_button.pack(side=tk.LEFT, padx=5)

        # Обща сума
        self.total_label = ttk.Label(self.master, text="Обща сума: 0.00 лв.")
        self.total_label.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

    def load_products(self):
        self.cursor.execute("SELECT име, цена, път_към_изображение FROM продукти")
        products = self.cursor.fetchall()
        self.product_canvas.delete("product")  # Изтриване на старите продукти от canvas-а

        x = 10
        y = 10
        for product in products:
            try:
                image = Image.open(product[2])  # Отворете изображението от пътя в базата данни
                image = image.resize((50, 50), Image.LANCZOS)  # Променете размера на изображението
                photo = ImageTk.PhotoImage(image)

                product_button = tk.Button(self.product_canvas, image=photo, compound=tk.TOP,
                                          text=f"{product[0]} - {product[1]:.2f} лв.", wraplength=80,
                                          command=lambda p=product: self.add_to_cart(p))  # Предаване на product
                product_button.image = photo  # Запазете препратка към PhotoImage, за да не бъде изтрито от garbage collector-а
                product_button.bind("<Double-Button-1>", lambda event, p=product: self.add_to_cart(p))  # Двойно кликване

                self.product_canvas.create_window(x, y, window=product_button, tags="product")

                x += 100  # Разстояние между бутоните по хоризонтала
                if x > self.product_canvas.winfo_width() - 100:  # Нов ред, ако продуктите не се побират
                    x = 10
                    y += 100  # Разстояние между бутоните по вертикала
            except FileNotFoundError:
                print(f"Грешка: Изображението за продукт '{product[0]}' не е намерено!")
            except Exception as e:
                print(f"Грешка при зареждане на изображението за продукт '{product[0]}': {e}")

        self.product_canvas.config(scrollregion=self.product_canvas.bbox)


        def add_product(self):
            def save_product():
                name = name_entry.get()
                price = price_entry.get()
                barcode = barcode_entry.get()
                image_path = self.product_image_path  # Пътят към избраното изображение

                if not name:
                    messagebox.showwarning("Грешка", "Моля, въведете име на продукта!")
                    return

                try:
                    price = float(price)
                    if price <= 0:
                        raise ValueError
                except ValueError:
                    messagebox.showwarning("Грешка", "Невалидна цена! Моля, въведете положително число.")
                    return

                if barcode:
                    self.cursor.execute("SELECT * FROM продукти WHERE баркод=?", (barcode,))
                    if self.cursor.fetchone():
                        messagebox.showwarning("Грешка", "Баркодът вече съществува! Моля, въведете друг баркод.")
                        return

                if name and price:
                    try:
                        price = float(price)
                        self.cursor.execute(
                            "INSERT INTO продукти (име, цена, баркод, път_към_изображение) VALUES (?, ?, ?, ?)",
                            (name, price, barcode, image_path))  # Запазваме и пътя към изображението
                        self.conn.commit()
                        self.load_products()
                        add_window.destroy()
                    except ValueError:
                        messagebox.showwarning("Грешка", "Невалидна цена!")
                else:
                    messagebox.showwarning("Грешка", "Моля, попълнете всички полета!")

            add_window = tk.Toplevel(self.master)
            add_window.title("Добавяне на продукт")

            name_label = ttk.Label(add_window, text="Име:")
            name_label.grid(row=0, column=0, padx=5, pady=5)
            name_entry = ttk.Entry(add_window)
            name_entry.grid(row=0, column=1, padx=5, pady=5)

            price_label = ttk.Label(add_window, text="Цена:")
            price_label.grid(row=1, column=0, padx=5, pady=5)
            price_entry = ttk.Entry(add_window)
            price_entry.grid(row=1, column=1, padx=5, pady=5)

            barcode_label = ttk.Label(add_window, text="Баркод:")
            barcode_label.grid(row=2, column=0, padx=5, pady=5)
            barcode_entry = ttk.Entry(add_window)
            barcode_entry.grid(row=2, column=1, padx=5, pady=5)

            # Добавяне на бутон за избор на изображение
            image_button = ttk.Button(add_window, text="Изберете изображение", command=self.choose_product_image)
            image_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

            save_button = ttk.Button(add_window, text="Запази", command=save_product)
            save_button.grid(row=4, column=0, columnspan=2, padx=5, pady=10)

            self.product_image_path = None  # Път към избраното изображение (ще се попълни от choose_product_image)

        def choose_product_image(self):
            file_path = filedialog.askopenfilename(
                title="Изберете изображение на продукт",
                filetypes=(("Image files", "*.jpg;*.jpeg;*.png;*.gif"), ("All files", "*.*"))
            )
            if file_path:
                self.product_image_path = file_path
                print(f"Избрано изображение: {file_path}")  # Печатане на пътя за проверка

        def edit_product(self):
            selected_product = self.product_list.curselection()
            if selected_product:
                product_name = self.product_list.get(selected_product)
                product_name = product_name.split(" - ")[0]

                self.cursor.execute("SELECT * FROM продукти WHERE име=?", (product_name,))
                product = self.cursor.fetchone()

                def update_product():
                    name = name_entry.get()
                    price = price_entry.get()
                    barcode = barcode_entry.get()
                    image_path = self.product_image_path  # Пътят към избраното изображение

                    if not name:
                        messagebox.showwarning("Грешка", "Моля, въведете име на продукта!")
                        return

                    try:
                        price = float(price)
                        if price <= 0:
                            raise ValueError
                    except ValueError:
                        messagebox.showwarning("Грешка", "Невалидна цена! Моля, въведете положително число.")
                        return

                    if barcode:
                        self.cursor.execute("SELECT * FROM продукти WHERE баркод=?", (barcode,))
                        existing_product = self.cursor.fetchone()
                        if existing_product and existing_product[0] != product[
                            0]:  # Проверка дали баркодът вече съществува за друг продукт
                            messagebox.showwarning("Грешка",
                                                   "Баркодът вече съществува за друг продукт! Моля, въведете друг баркод.")
                            return

                    if name and price:
                        try:
                            price = float(price)
                            self.cursor.execute(
                                "UPDATE продукти SET име=?, цена=?, баркод=?, път_към_изображение=? WHERE id=?",
                                (name, price, barcode, image_path, product[0]))  # Обновяваме и пътя към изображението
                            self.conn.commit()
                            self.load_products()
                            edit_window.destroy()
                        except ValueError:
                            messagebox.showwarning("Грешка", "Невалидна цена!")
                    else:
                        messagebox.showwarning("Грешка", "Моля, попълнете всички полета!")

                edit_window = tk.Toplevel(self.master)
                edit_window.title("Редактиране на продукт")

                name_label = ttk.Label(edit_window, text="Име:")
                name_label.grid(row=0, column=0, padx=5, pady=5)
                name_entry = ttk.Entry(edit_window)
                name_entry.insert(0, product[1])
                name_entry.grid(row=0, column=1, padx=5, pady=5)

                price_label = ttk.Label(edit_window, text="Цена:")
                price_label.grid(row=1, column=0, padx=5, pady=5)
                price_entry = ttk.Entry(edit_window)
                price_entry.insert(0, product[2])
                price_entry.grid(row=1, column=1, padx=5, pady=5)

                barcode_label = ttk.Label(edit_window, text="Баркод:")
                barcode_label.grid(row=2, column=0, padx=5, pady=5)
                barcode_entry = ttk.Entry(edit_window)
                barcode_entry.insert(0, product[3])
                barcode_entry.grid(row=2, column=1, padx=5, pady=5)

                # Показване на текущото изображение (ако има)
                if product[4]:
                    try:
                        image = Image.open(product[4])
                        image = image.resize((100, 100), Image.LANCZOS)  # Променете размера според нуждите
                        photo = ImageTk.PhotoImage(image)
                        image_label = ttk.Label(edit_window, image=photo)
                        image_label.image = photo  # Запазете препратката
                        image_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
                    except FileNotFoundError:
                        print("Грешка: Изображението не е намерено!")
                    except Exception as e:
                        print(f"Грешка при зареждане на изображението: {e}")

                    # Добавяне на бутон