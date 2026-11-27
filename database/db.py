import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash


def get_db():
    conn = sqlite3.connect('spendly.db')
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn


def init_db():
    conn = get_db()
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now'))
            );
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            );
        ''')
    conn.close()


def seed_db():
    conn = get_db()
    cursor = conn.cursor()

    # Check if users table already has data
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    with conn:
        # Insert demo user with hashed password
        password_hash = generate_password_hash('demo123')
        cursor.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            ('Demo User', 'demo@spendly.com', password_hash)
        )
        user_id = cursor.lastrowid

        # Categories to use
        categories = ['Food', 'Transport', 'Bills', 'Health', 'Entertainment', 'Shopping', 'Other']

        # Current month for dates (YYYY-MM-DD format)
        current_month = datetime.now().strftime('%Y-%m')

        # 8 sample expenses covering all 7 categories + one extra
        expenses = [
            (user_id, 45.50, 'Food', f'{current_month}-02', 'Groceries at supermarket'),
            (user_id, 22.00, 'Transport', f'{current_month}-05', 'Bus pass'),
            (user_id, 120.00, 'Bills', f'{current_month}-08', 'Electricity bill'),
            (user_id, 35.00, 'Health', f'{current_month}-10', 'Pharmacy'),
            (user_id, 55.00, 'Entertainment', f'{current_month}-12', 'Movie tickets'),
            (user_id, 89.99, 'Shopping', f'{current_month}-15', 'New shoes'),
            (user_id, 15.00, 'Other', f'{current_month}-18', 'Miscellaneous'),
            (user_id, 30.00, 'Food', f'{current_month}-22', 'Restaurant dinner'),
        ]

        for exp in expenses:
            cursor.execute(
                "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
                exp
            )

    conn.close()


if __name__ == '__main__':
    init_db()
    seed_db()
    print("Database initialized and seeded.")