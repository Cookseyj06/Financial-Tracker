import sqlite3

# Use the credentials we confirmed earlier
conn = sqlite3.connect("finance.db", check_same_thread=False)
cursor = conn.cursor()

def create_table():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT,
            amount REAL,
            category TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

def add_expense(name, price, cat):
    
    sql = "INSERT INTO expenses (item_name, amount, category) VALUES (?, ?, ?)"
    cursor.execute(sql, (name, price, cat))
    
    conn.commit()


def view_table():
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    
    table = f"{'ID':<5} | {'Item':<15} | {'Amount':<10} | {'Category'}"
    table = table + "\n" + "-" * 50
    for row in rows:
        # row[0] is id, row[1] is name, row[2] is price, row[3] is category
        
        table = table + f"\n{row[0]:<5} | {row[1]:<15} | ${row[2]:<10} | {row[3]}"
    return table


def delete_row(id):
    sql = "DELETE FROM expenses WHERE ID = ?"
    cursor.execute(sql, (id,))
    conn.commit()
    

def calculate_spending_by_item(name):
    sql = "SELECT * FROM expenses WHERE item_name = ?"
    cursor.execute(sql, (name,))
            
    rows = cursor.fetchall()
    total = 0
    
    for row in rows:
        total += row[2]
    return total
    
    
def calculate_spending_by_category(cat):
    sql = "SELECT * FROM expenses WHERE Category = ?"
    cursor.execute(sql, (cat,))
            
    rows = cursor.fetchall()
    total = 0
    
    for row in rows:
        total += row[2]
    return total


def calculate_total_spending():
    cursor.execute("SELECT * FROM expenses")
            
    rows = cursor.fetchall()
    total = 0
    
    for row in rows:
        total += float(row[2])
    return total

def reset_table():
        cursor.execute("DELETE FROM expenses")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='expenses'")
        conn.commit()

create_table()