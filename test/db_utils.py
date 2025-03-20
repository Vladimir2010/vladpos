from pysqlcipher3 import dbapi2 as sqlite

DB_PATH = "database/pos_syst.db"
DB_PASSWORD = "your_secure_password"  # Change this to your desired password

def get_connection():
    connection = sqlite.connect(DB_PATH)
    connection.execute(f"PRAGMA key = '{DB_PASSWORD}'")
    return connection

def initialize_db():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            operator_name TEXT,
            operator_number TEXT
        )
    ''')
    connection.commit()
    connection.close()