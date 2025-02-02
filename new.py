import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import serial


# Database setup
def init_db():
    conn = sqlite3.connect("pos_system.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        barcode TEXT UNIQUE NOT NULL,
                        price REAL NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS sales (
                        id INTEGER PRIMARY KEY,
                        product_id INTEGER,
                        quantity INTEGER,
                        total_price REAL,
                        date TEXT,
                        FOREIGN KEY (product_id) REFERENCES products(id))''')
    conn.commit()
    conn.close()


# POS System GUI
class POSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ВладПос")
        self.root.geometry("800x600")
        self.root.configure(bg="#2c3e50")

        self.create_widgets()
        self.load_products()

    def create_widgets(self):
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 12), padding=5)
        self.style.configure("TLabel", font=("Arial", 14), background="#2c3e50", foreground="white")
        self.style.configure("Treeview", font=("Arial", 12), rowheight=30)

        frame_top = tk.Frame(self.root, bg="#34495e", pady=10)
        frame_top.pack(fill="x")

        self.label = ttk.Label(frame_top, text="Баркод:")
        self.label.pack(side="left", padx=10)

        self.barcode_entry = ttk.Entry(frame_top, font=("Arial", 12))
        self.barcode_entry.pack(side="left", padx=10)

        self.scan_button = ttk.Button(frame_top, text="Сканиране", command=self.scan_product)
        self.scan_button.pack(side="left", padx=10)

        self.add_product_btn = ttk.Button(frame_top, text="Добави продукт", command=self.add_product)
        self.add_product_btn.pack(side="left", padx=10)

        frame_middle = tk.Frame(self.root, bg="#2c3e50")
        frame_middle.pack(expand=True, fill="both")

        self.tree = ttk.Treeview(frame_middle, columns=("Barcode", "Name", "Price"), show="headings")
        self.tree.heading("Barcode", text="Баркод")
        self.tree.heading("Name", text="Име")
        self.tree.heading("Price", text="Цена")
        self.tree.pack(expand=True, fill="both", padx=20, pady=20)

        frame_bottom = tk.Frame(self.root, bg="#34495e", pady=10)
        frame_bottom.pack(fill="x")

        self.pay_button = ttk.Button(frame_bottom, text="Плащане", command=self.process_payment)
        self.pay_button.pack(pady=5)

    def scan_product(self):
        barcode = self.barcode_entry.get()
        if not barcode:
            messagebox.showwarning("Грешка", "Моля, въведете баркод!")
            return
        conn = sqlite3.connect("pos_system.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name, price FROM products WHERE barcode = ?", (barcode,))
        product = cursor.fetchone()
        conn.close()
        if product:
            self.tree.insert("", "end", values=(barcode, product[0], product[1]))
        else:
            messagebox.showerror("Грешка", "Продуктът не е намерен!")

    def add_product(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Добавяне на продукт")

        ttk.Label(add_window, text="Име:").grid(row=0, column=0)
        name_entry = ttk.Entry(add_window)
        name_entry.grid(row=0, column=1)

        ttk.Label(add_window, text="Баркод:").grid(row=1, column=0)
        barcode_entry = ttk.Entry(add_window)
        barcode_entry.grid(row=1, column=1)

        ttk.Label(add_window, text="Цена:").grid(row=2, column=0)
        price_entry = ttk.Entry(add_window)
        price_entry.grid(row=2, column=1)

        def save_product():
            name = name_entry.get()
            barcode = barcode_entry.get()
            price = price_entry.get()
            if not name or not barcode or not price:
                messagebox.showwarning("Грешка", "Всички полета са задължителни!")
                return
            try:
                conn = sqlite3.connect("pos_system.db")
                cursor = conn.cursor()
                cursor.execute("INSERT INTO products (name, barcode, price) VALUES (?, ?, ?)", (name, barcode, price))
                conn.commit()
                conn.close()
                self.load_products()
                add_window.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Грешка", "Баркодът вече съществува!")

        save_button = ttk.Button(add_window, text="Запази", command=save_product)
        save_button.grid(row=3, columnspan=2)

    def load_products(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        conn = sqlite3.connect("pos_system.db")
        cursor = conn.cursor()
        cursor.execute("SELECT barcode, name, price FROM products")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()


if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = POSApp(root)
    root.mainloop()
