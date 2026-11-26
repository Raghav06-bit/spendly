import sqlite3

def get_db():
    conn = sqlite3.connect('database/spendly.db')
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
                password TEXT NOT NULL
            );
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            );
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                category_id INTEGER,
                amount REAL NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE SET NULL
            );
        ''')
    conn.close()

def seed_db():
    conn = get_db()
    with conn:
        # Example users (passwords should be hashed in a real app)
        conn.execute("INSERT OR IGNORE INTO users (id, name, email, password) VALUES (?, ?, ?, ?)",
                     (1, 'Alice Smith', 'alice@example.com', 'password123'))
        conn.execute("INSERT OR IGNORE INTO users (id, name, email, password) VALUES (?, ?, ?, ?)",
                     (2, 'Bob Johnson', 'bob@example.com', 'securepass'))

        # Example categories for Alice
        conn.execute("INSERT OR IGNORE INTO categories (id, user_id, name) VALUES (?, ?, ?)",
                     (1, 1, 'Food'))
        conn.execute("INSERT OR IGNORE INTO categories (id, user_id, name) VALUES (?, ?, ?)",
                     (2, 1, 'Transport'))
        conn.execute("INSERT OR IGNORE INTO categories (id, user_id, name) VALUES (?, ?, ?)",
                     (3, 1, 'Bills'))

        # Example expenses for Alice
        conn.execute("INSERT OR IGNORE INTO expenses (id, user_id, category_id, amount, date, description) VALUES (?, ?, ?, ?, ?, ?)",
                     (1, 1, 1, 25.50, '2026-11-20', 'Groceries'))
        conn.execute("INSERT OR IGNORE INTO expenses (id, user_id, category_id, amount, date, description) VALUES (?, ?, ?, ?, ?, ?)",
                     (2, 1, 2, 15.00, '2026-11-21', 'Bus fare'))
        conn.execute("INSERT OR IGNORE INTO expenses (id, user_id, category_id, amount, date, description) VALUES (?, ?, ?, ?, ?, ?)",
                     (3, 1, 3, 75.00, '2026-11-22', 'Electricity bill'))

    conn.close()

if __name__ == '__main__':
    init_db()
    seed_db()
    print("Database initialized and seeded.")
