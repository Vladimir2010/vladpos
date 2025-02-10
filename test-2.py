import tkinter as tk
from tkinter import messagebox
import sqlite3
import serial
import datetime


# Свързване към SQLite база данни
def connect_db():
    conn = sqlite3.connect("vladpos.db")
    return conn.cursor(), conn


# Създаване на таблица за продукти
def create_products_table():
    cur, conn = connect_db()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            barcode TEXT,
            name TEXT,
            price REAL,
            quantity INTEGER
        )
    """)
    conn.commit()
    conn.close()


# Добавяне на нов продукт
def add_product(barcode, name, price, quantity):
    cur, conn = connect_db()
    cur.execute("""
        INSERT INTO products (barcode, name, price, quantity)
        VALUES (?, ?, ?, ?)
    """, (barcode, name, price, quantity))
    conn.commit()
    conn.close()


# Извеждане на продукти
def get_products():
    cur, conn = connect_db()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    conn.close()
    return products


# Опресняване на продуктите
def refresh_products_list():
    products = get_products()
    product_list.delete(0, tk.END)
    for product in products:
        product_list.insert(tk.END,
                            f"Barcode: {product[1]}, Name: {product[2]}, Price: {product[3]}, Quantity: {product[4]}")


# Плащане с карта
def process_card_payment(amount):
    # Интеграция с POS терминал (примерно)
    print(f"Processing card payment of {amount}")
    # Тук ще бъде кодът за изпращане към терминала
    # За сега просто изведете информацията
    messagebox.showinfo("Payment", f"Card payment of {amount} processed successfully")


# Плащане в брой
def process_cash_payment(amount):
    # Платежен процес в брой
    print(f"Cash payment of {amount}")
    messagebox.showinfo("Payment", f"Cash payment of {amount} processed successfully")


# Интерфейс за добавяне на продукти
def add_product_interface():
    add_window = tk.Toplevel(root)
    add_window.title("Add Product")

    tk.Label(add_window, text="Barcode:").pack()
    barcode_entry = tk.Entry(add_window)
    barcode_entry.pack()

    tk.Label(add_window, text="Name:").pack()
    name_entry = tk.Entry(add_window)
    name_entry.pack()

    tk.Label(add_window, text="Price:").pack()
    price_entry = tk.Entry(add_window)
    price_entry.pack()

    tk.Label(add_window, text="Quantity:").pack()
    quantity_entry = tk.Entry(add_window)
    quantity_entry.pack()

    def save_product():
        barcode = barcode_entry.get()
        name = name_entry.get()
        price = float(price_entry.get())
        quantity = int(quantity_entry.get())
        add_product(barcode, name, price, quantity)
        refresh_products_list()
        add_window.destroy()

    tk.Button(add_window, text="Save", command=save_product).pack()


# Стартово меню на ПОС системата
def pos_system():
    global root
    root = tk.Tk()
    root.title("VladPos - POS System")

    tk.Button(root, text="Add Product", command=add_product_interface).pack()
    tk.Button(root, text="Show Products", command=refresh_products_list).pack()

    # Списък с продукти
    global product_list
    product_list = tk.Listbox(root, width=50, height=10)
    product_list.pack()

    # Плащане (тестови бутони за демонстрация)
    tk.Button(root, text="Pay with Card", command=lambda: process_card_payment(50.0)).pack()
    tk.Button(root, text="Pay with Cash", command=lambda: process_cash_payment(50.0)).pack()

    create_products_table()
    root.mainloop()


# Стартиране на приложението
if __name__ == "__main__":
    pos_system()