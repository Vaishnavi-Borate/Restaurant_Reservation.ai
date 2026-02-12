# backend/services.py
from database import conn, cursor

MAX_TABLES = 10  # assume restaurant has 10 tables per slot

# ---------------------------
# Check table availability
# ---------------------------
def calculate_table_allocation(people):
    """
    Allocate table for given number of people
    (simple placeholder logic)
    """
    return "Standard Table" if people <= 4 else "Large Table"

def tables_available(date, time):
    cursor.execute(
        "SELECT COUNT(*) FROM reservations WHERE date=? AND time=? AND status='CONFIRMED'",
        (date, time)
    )
    booked = cursor.fetchone()[0]
    return booked < MAX_TABLES

def promote_waitlist(date, time):
    cursor.execute(
        "SELECT * FROM waitlist ORDER BY created_at ASC LIMIT 1"
    )
    user = cursor.fetchone()
    if not user:
        return None
    wid, name, phone, people, _ = user
    table_type = calculate_table_allocation(people)
    cursor.execute(
        "INSERT INTO reservations(name, phone, date, time, people, status, table_type) VALUES (?,?,?,?,?,?,?)",
        (name, phone, date, time, people, "CONFIRMED", table_type)
    )
    cursor.execute("DELETE FROM waitlist WHERE id=?", (wid,))
    conn.commit()
    return name
