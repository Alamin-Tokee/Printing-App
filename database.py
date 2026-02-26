import sqlite3
DB_NAME = "app.db"

def connect():
    return sqlite3.connect(DB_NAME)

def create_table():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def add_user(name, email):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))

    conn.commit()
    conn.close()

def get_users():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, email FROM users")
    users = cursor.fetchall()

    conn.close()
    return users


def delete_user(user_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()
