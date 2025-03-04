import sqlite3
import os

DB_DIR = "database"
DB_PATH = "database/pos_system.db"

def create_database():
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
    # Проверка дали файлът за базата данни съществува
    if not os.path.exists(DB_PATH):
        open(DB_PATH, 'w').close()  # Създаване на празен файл за базата
        print("Създаден е нов файл за базата данни.")
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    # Create products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            barcode TEXT NOT NULL,
            unit_price REAL NOT NULL
        )
    ''')

    # Create customers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            eik TEXT NOT NULL,
            dds TEXT NOT NULL,
            address TEXT NOT NULL,
            mol TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    ''')

    # Create firm table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS firm (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            eik TEXT NOT NULL,
            dds TEXT NOT NULL,
            address TEXT NOT NULL,
            mol TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    ''')

    # Create documents table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY,
            products TEXT NOT NULL,  -- JSON format
            total_amount REAL NOT NULL,
            amount_paid REAL NOT NULL,
            change REAL NOT NULL,
            payment_type TEXT NOT NULL,
            cash_register_numbers TEXT
        )
    ''')

    # Create invoices table with foreign keys referencing customers and firm
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            number INTEGER PRIMARY KEY,
            customer_ref_no INTEGER NOT NULL,
            selling_company_ref_no INTEGER NOT NULL,
            date TEXT NOT NULL,
            products TEXT NOT NULL,  -- JSON format
            total_amount REAL NOT NULL,
            amount_paid REAL NOT NULL,
            change REAL NOT NULL,
            payment_type TEXT NOT NULL,
            FOREIGN KEY (customer_ref_no) REFERENCES customers(id),
            FOREIGN KEY (selling_company_ref_no) REFERENCES firm(id)
        )
    ''')

    connection.commit()
    connection.close()