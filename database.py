import sqlite3,json,os

DB_NAME = "users.db"


def connect_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def user_exists(username):
    return get_user(username) is not None

def create_db():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            active INTEGER DEFAULT 1
        )
    """)

    conn.commit()
    conn.close()


def add_user(username, hashed_password):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (username, password)
        VALUES (?, ?)
    """, (username, hashed_password))

    conn.commit()
    conn.close()


def get_user(username):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM users
        WHERE username = ?
    """, (username,))

    user = cursor.fetchone()

    conn.close()
    return user

def get_all_users():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()

    return users
def update_password(username, hashed_password):
    conn= connect_db()
    cursor = conn.cursor()

    cursor.execute("""
                   UPDATE users
                   SET password = ?
                   WHERE username = ?
                   """, (hashed_password, username))
    conn.commit()
    conn.close()