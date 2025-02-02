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

        frame_middle = tk.Frame(self.root, bg="#2c3e50")
        frame_middle.pack(expand=True, fill="both")

        self.tree = ttk.Treeview(frame_middle, columns=("Name", "Price", "Quantity", "Total"), show="headings")
        self.tree.heading("Name", text="Име")
        self.tree.heading("Price", text="Цена")
        self.tree.heading("Quantity", text="Количество")
        self.tree.heading("Total", text="Общо")
        self.tree.pack(expand=True, fill="both", padx=20, pady=20)

        frame_bottom = tk.Frame(self.root, bg="#34495e", pady=10)
        frame_bottom.pack(fill="x")

        self.pay_button = ttk.Button(frame_bottom, text="Плащане", command=self.process_payment)
        self.pay_button.pack(pady=5)

    def scan_product(self):
        barcode = self.barcode_entry.get()
        conn = sqlite3.connect("pos_system.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name, price FROM products WHERE barcode = ?", (barcode,))
        product = cursor.fetchone()
        conn.close()

        if product:
            name, price = product
            self.tree.insert("", "end", values=(name, price, 1, price))
        else:
            messagebox.showerror("Грешка", "Продукта не е открито в базата данни.")

    def process_payment(self):
        total = sum(float(self.tree.item(item, "values")[3]) for item in self.tree.get_children())
        self.print_receipt(total)
        messagebox.showinfo("Плащане", f"Общо: {total} лв!")

    def print_receipt(self, amount):
        try:
            with serial.Serial("COM3", baudrate=9600, timeout=1) as ser:
                ser.write(f"Total: {amount}\n".encode())
        except serial.SerialException as e:
            messagebox.showerror("Грешка", f"Грешка при печат: {e}")


if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = POSApp(root)
    root.mainloop()
