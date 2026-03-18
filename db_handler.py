import sqlite3
import pandas as pd
from datetime import datetime

DB_NAME = "finbot.db"

def init_db():
    """Creates the database automatically."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            item TEXT,
            category TEXT,
            amount REAL
        )
    ''')
    conn.commit()
    conn.close()

def add_transaction(item, category, amount):
    """Saves data to the database."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO transactions (date, item, category, amount) VALUES (?, ?, ?, ?)", 
              (date, item, category, amount))
    conn.commit()
    conn.close()

def get_transactions():
    """Fetches data for the dashboard."""
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql("SELECT * FROM transactions", conn)
    conn.close()
    return df

# Run initialization immediately
init_db()