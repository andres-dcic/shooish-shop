import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent / "shop.db"

def connect():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    # Initialize database only if it doesn't exist
    if DB.exists():
        return

    con = connect()
    con.executescript("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    );

    CREATE TABLE products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        price REAL NOT NULL
    );

    CREATE TABLE orders (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        status TEXT NOT NULL
    );

    INSERT INTO users VALUES
        (1, 'alice', 'alice123', 'customer'),
        (2, 'bob', 'bob123', 'customer'),
        (3, 'admin', 'admin123', 'admin');

    INSERT INTO products VALUES
        (1, 'Kiteboard', 'Training kiteboard', 799.00),
        (2, 'Harness', 'Comfort harness', 149.00),
        (3, 'Helmet', 'Water sports helmet', 59.00);

    INSERT INTO orders VALUES
        (101, 1, 1, 1, 'paid'),
        (102, 2, 2, 2, 'shipped');
    """)
    con.commit()
    con.close()
