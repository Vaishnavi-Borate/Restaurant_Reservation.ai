import sqlite3
import threading
import os

DB_NAME = "restaurant.db"
lock = threading.Lock()

def get_db():
    conn = sqlite3.connect(
        DB_NAME,
        check_same_thread=False,
        timeout=60,
        isolation_level=None
    )
    conn.row_factory = sqlite3.Row

    # WAL only if not already WAL
    cur = conn.cursor()
    cur.execute("PRAGMA journal_mode;")
    mode = cur.fetchone()[0]

    if mode.lower() != "wal":
        conn.execute("PRAGMA journal_mode=WAL;")

    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.execute("PRAGMA busy_timeout = 60000;")

    return conn


def init_db():
    with lock:
        conn = sqlite3.connect(DB_NAME, timeout=60)
        cursor = conn.cursor()

        # tables
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            date TEXT,
            time TEXT,
            people INTEGER,
            status TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS waitlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            people INTEGER
        )
        """)


    # orders (linked with reservation)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reservation_id INTEGER,
            item_name TEXT,
            quantity INTEGER,
            time TEXT
        )
        """)


        conn.commit()
        conn.close()
