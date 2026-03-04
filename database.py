import sqlite3
DB_NAME = "app.db"

def connect():
    return sqlite3.connect(DB_NAME)

def create_table():
    conn = connect()
    cursor = conn.cursor()

    cursor.executescript("""
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

    CREATE TABLE IF NOT EXISTS scan_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        barcode VARCHAR(100) NOT NULL,
        scan_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
                   
    CREATE TABLE IF NOT EXISTS user_permissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(50) NOT NULL UNIQUE,
        project VARCHAR(50) NOT NULL,
        subproject VARCHAR(50) NOT NULL,
        is_admin BOOLEAN NOT NULL DEFAULT 0,
        is_active BOOLEAN NOT NULL DEFAULT 1
    );
                         
    CREATE TABLE IF NOT EXISTS ecd_mapping (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        wsbt_code VARCHAR(50) NOT NULL UNIQUE,
        product_model VARCHAR(100) NOT NULL,
        product_version VARCHAR(50) NOT NULL,
        insert_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        is_active BOOLEAN NOT NULL DEFAULT 1
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



# For scan history
def add_scan_history(barcode):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO scan_history (barcode) VALUES (?)
    """, (barcode,))

    conn.commit()
    conn.close()

def get_scan_history():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT id, barcode, scan_time FROM scan_history ORDER BY scan_time DESC")
    history = cursor.fetchall()

    conn.close()
    return history


def clear_scan_history():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM scan_history")
    conn.commit()
    conn.close()



# For user permissions
def add_user_permission(username, project, subproject, is_admin=False, is_active=True):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO user_permissions (username, project, subproject, is_admin, is_active) 
        VALUES (?, ?, ?, ?, ?)
    """, (username, project, subproject, int(is_admin), int(is_active)))

    conn.commit()
    conn.close()

def get_user_permissions():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT id, username, project, subproject, is_admin, is_active FROM user_permissions")
    permissions = cursor.fetchall()

    conn.close()
    return permissions 


def get_user_permission_by_id(permission_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT id, username, project, subproject, is_admin, is_active FROM user_permissions WHERE id=?", (permission_id,))
    permission = cursor.fetchone()

    conn.close()
    return permission

def update_user_permission(permission_id, username, project, subproject, is_admin, is_active):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE user_permissions 
        SET username=?, project=?, subproject=?, is_admin=?, is_active=? 
        WHERE id=?
    """, (username, project, subproject, int(is_admin), int(is_active), permission_id))

    conn.commit()
    conn.close()

def delete_user_permission(permission_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user_permissions WHERE id=?", (permission_id,))
    conn.commit()
    conn.close()



# ----------------------- For ECD Mapping -----------------------
def add_ecd_mapping(wsbt_code, product_model, product_version, is_active=True):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO ecd_mapping (wsbt_code, product_model, product_version, is_active) 
        VALUES (?, ?, ?, ?)
    """, (wsbt_code, product_model, product_version, int(is_active)))

    conn.commit()
    conn.close()

def get_ecd_mappings():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT id, wsbt_code, product_model, product_version, insert_time, is_active FROM ecd_mapping")
    mappings = cursor.fetchall()

    conn.close()
    return mappings

def get_ecd_mapping_by_id(mapping_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT id, wsbt_code, product_model, product_version, insert_time, is_active FROM ecd_mapping WHERE id=?", (mapping_id,))
    mapping = cursor.fetchone()

    conn.close()
    return mapping

def update_ecd_mapping(mapping_id, wsbt_code, product_model, product_version, is_active):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE ecd_mapping 
        SET wsbt_code=?, product_model=?, product_version=?, is_active=? 
        WHERE id=?
    """, (wsbt_code, product_model, product_version, int(is_active), mapping_id))

    conn.commit()
    conn.close()

def delete_ecd_mapping(mapping_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ecd_mapping WHERE id=?", (mapping_id,))
    conn.commit()
    conn.close()    

    
