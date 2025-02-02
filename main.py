import tkinter as tk
from tkinter import messagebox
from cash_register import CashRegister
from database import Database
import serial.tools.list_ports


class VladPosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VladPOS - ПОС система")
        self.root.geometry("1800x1000")

        self.cash_register = CashRegister()
        self.database = Database()

        # Заглавие
        self.title_label = tk.Label(self.root, text="VladPOS Система", font=("Helvetica", 16))
        self.title_label.pack(pady=10)

        # Потребителски интерфейс
        self.create_ui()
        self.create_menu()

    def create_menu(self):
        menubar = tk.Menu(self.root)

        # Файл
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Запази", command=self.save_data)
        file_menu.add_separator()
        file_menu.add_command(label="Изход", command=self.exit_app)
        menubar.add_cascade(label="Файл", menu=file_menu)

        # Настройки
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Настройки на касов апарат", command=self.configure_cash_register)
        settings_menu.add_command(label="Настройки на база данни", command=self.configure_database)
        menubar.add_cascade(label="Настройки", menu=settings_menu)

        # Помощ
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Помощ", command=self.show_help)
        help_menu.add_command(label="За програмата", command=self.show_about)
        menubar.add_cascade(label="Помощ", menu=help_menu)

        self.root.config(menu=menubar)

    def configure_cash_register(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Настройки на касов апарат")
        settings_window.geometry("400x200")

        # Етикети
        tk.Label(settings_window, text="Изберете COM порт:").pack(pady=5)
        com_port_var = tk.StringVar(value="COM13")

        # Намиране на наличните COM портове
        ports = [port.device for port in serial.tools.list_ports.comports()]
        com_dropdown = tk.OptionMenu(settings_window, com_port_var, *ports)
        com_dropdown.pack(pady=5)

        tk.Label(settings_window, text="Изберете Baudrate:").pack(pady=5)
        baudrate_var = tk.StringVar(value="115200")

        # Възможни baudrate стойности
        baudrates = ["9600", "19200", "38400", "57600", "115200"]
        baud_dropdown = tk.OptionMenu(settings_window, baudrate_var, *baudrates)
        baud_dropdown.pack(pady=5)

        # Бутон за записване на настройките
        def save_settings():
            selected_com = com_port_var.get()
            selected_baud = baudrate_var.get()
            if selected_com and selected_baud:
                messagebox.showinfo("Запазено", f"Избран порт: {selected_com}\nСкорост: {selected_baud}")
                self.cash_register_com = selected_com
                self.cash_register_baud = selected_baud
            else:
                messagebox.showwarning("Грешка", "Моля, изберете COM порт и Baudrate!")

        tk.Button(settings_window, text="Запази настройки", command=save_settings).pack(pady=10)

    def save_data(self):
        messagebox.showinfo("Запазване", "Данните са запазени успешно!")

    def exit_app(self):
        self.root.quit()

    def configure_database(self):
        messagebox.showinfo("Настройки", "Тук ще има настройки за базата данни.")

    def show_help(self):
        messagebox.showinfo("Помощ", "Инструкции за работа с програмата.")

    def show_about(self):
        messagebox.showinfo("За програмата", "VladPOS - ПОС система, разработена от Владимир.")

    def create_ui(self):
        # Номер на поръчка
        tk.Label(self.root, text="Номер на поръчка:").pack(pady=5)
        self.order_entry = tk.Entry(self.root)
        self.order_entry.pack(pady=5)



        # Сума
        tk.Label(self.root, text="Сума (лв):").pack(pady=5)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.pack(pady=5)

        # COM порт
        tk.Label(self.root, text="COM порт:").pack(pady=5)
        self.com_entry = tk.Entry(self.root)
        self.com_entry.insert(0, "COM1")  # Стойност по подразбиране
        self.com_entry.pack(pady=5)

        # Baudrate
        tk.Label(self.root, text="Baudrate:").pack(pady=5)
        self.baudrate_entry = tk.Entry(self.root)
        self.baudrate_entry.insert(0, "9600")  # Стойност по подразбиране
        self.baudrate_entry.pack(pady=5)

        # Бутон за отпечатване
        self.print_button = tk.Button(self.root, text="Отпечати касова бележка", command=self.print_receipt)
        self.print_button.pack(pady=10)

    def print_receipt(self):
        order_id = self.order_entry.get()
        amount = self.amount_entry.get()
        com_port = self.com_entry.get()
        baudrate = int(self.baudrate_entry.get())

        if not order_id or not amount:
            messagebox.showerror("Грешка", "Моля, попълнете всички полета!")
            return

        # Свързване и печат
        if self.cash_register.connect(com_port, baudrate):
            receipt_data = f"Номер на поръчка: {order_id}\nСума: {amount} лв"
            if self.cash_register.print_receipt(receipt_data):
                messagebox.showinfo("Успех", "Касовата бележка е отпечатана!")
            else:
                messagebox.showerror("Грешка", "Неуспешно отпечатване!")
        else:
            messagebox.showerror("Грешка", "Неуспешна връзка с касовия апарат.")


if __name__ == "__main__":
    root = tk.Tk()
    app = VladPosApp(root)
    root.mainloop()
