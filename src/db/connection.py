import sqlite3
from src.config.settings import DB_PATH

def get_connection():
    print(f"📌 Conectando a DB: {DB_PATH.resolve()}")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
