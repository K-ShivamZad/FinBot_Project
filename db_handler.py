import sqlite3
import pandas as pd
from datetime import datetime
import hashlib
import secrets

DB_NAME = "finbot.db"

def hash_password(password, salt=None):
    """Secures the password using SHA-256 encryption combined with a unique salt."""
    if salt is None:
        salt = secrets.token_hex(16)
    hash_gen = hashlib.sha256((salt + password).encode()).hexdigest()
    return hash_gen, salt

def init_db():
    """Creates the database automatically with User Auth & Indexed tables."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # 1. Create Users Table (Now storing unique salts)
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password_hash TEXT,
            salt TEXT
        )
    ''')
    
    # 2. Create Transactions Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            date TEXT,
            item TEXT,
            category TEXT,
            amount REAL
        )
    ''')
    
    # 3. Create an Index for faster performance as data grows
    c.execute('CREATE INDEX IF NOT EXISTS idx_user_transactions ON transactions (username)')
    
    conn.commit()
    conn.close()

def create_user(username, password):
    """Registers a new user with a uniquely salted password."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        pw_hash, salt = hash_password(password)
        c.execute("INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)", 
                  (username, pw_hash, salt))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False # Username exists
    conn.close()
    return success

def verify_user(username, password):
    """Checks credentials against the database using the stored salt."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT password_hash, salt FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()
    
    if result:
        stored_hash, stored_salt = result
        test_hash, _ = hash_password(password, stored_salt)
        if test_hash == stored_hash:
            return True
    return False

def add_transaction(username, item, category, amount):
    """Saves transaction tied to a specific user."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO transactions (username, date, item, category, amount) VALUES (?, ?, ?, ?, ?)", 
              (username, date, item, category, amount))
    conn.commit()
    conn.close()

def get_transactions(username):
    """Fetches data only for the logged-in user."""
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql("SELECT * FROM transactions WHERE username = ?", conn, params=(username,))
    conn.close()
    return df

# Initialize the database and indexes immediately
init_db()