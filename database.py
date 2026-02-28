import sqlite3
DB_NAME = "app.db"

def connect():
    return sqlite3.connect(DB_NAME)

def create_table():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fifo_inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_code VARCHAR(50) NOT NULL,
        item_name VARCHAR(100) NOT NULL,
        item_qty INTEGER NOT NULL,
        material VARCHAR(100),
        batch VARCHAR(50),
        pallet_box VARCHAR(50),
        po_number VARCHAR(50),
        shift VARCHAR(20),
        supplier VARCHAR(100),
        receive_date VARCHAR(20),
        expiry_date VARCHAR(20)
    );
    """)

    conn.commit()
    conn.close()

def add_user(
    item_code, item_name, item_qty, material, batch,
    pallet_box, po_number, shift, supplier,
    receive_date, expiry_date
):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO fifo_inventory (
            item_code, item_name, item_qty, material, batch,
            pallet_box, po_number, shift, supplier,
            receive_date, expiry_date
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        item_code,
        item_name,
        int(item_qty) if item_qty else 0,
        material,
        batch,
        pallet_box,
        po_number,
        shift,
        supplier,
        receive_date,   # expects string "yyyy-MM-dd"
        expiry_date     # expects string "yyyy-MM-dd"
    ))

    conn.commit()
    conn.close()

def get_users():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT id, item_code, item_name, item_qty, material, batch, pallet_box, po_number, shift, supplier, receive_date, expiry_date FROM fifo_inventory")
    users = cursor.fetchall()

    conn.close()
    return users


def delete_user(user_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM fifo_inventory WHERE id=?", (user_id,))
    conn.commit()
    conn.close()
