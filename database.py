import sqlite3

class Database:
    def __init__(self, db_name="vladpos.db"):
        self.connection = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id TEXT NOT NULL,
                amount REAL NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.connection.commit()

    def save_sale(self, order_id, amount):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO sales (order_id, amount) VALUES (?, ?)", (order_id, amount))
        self.connection.commit()
