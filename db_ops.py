from database import get_db, lock

# ✅ Waitlist save
def add_to_waitlist(name, phone, people):
    try:
        with lock:
            conn = get_db()
            cur = conn.cursor()

            cur.execute(
                "INSERT INTO waitlist (name, phone, people) VALUES (?, ?, ?)",
                (name, phone, people)
            )

            conn.commit()
            conn.close()
        return True
    except Exception as e:
        print("WAITLIST ERROR:", repr(e))
        return False


# Save reservation
def save_reservation(name, phone, date, time, people):
    try:
        with lock:
            conn = get_db()
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO reservations (name, phone, date, time, people, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, phone, date, time, people, "BOOKED"))

            res_id = cur.lastrowid   # reservation id

            conn.commit()
            conn.close()
        return res_id
    except Exception as e:
        print("RESERVATION ERROR:", repr(e))
        return None


# Save order linked to reservation
def save_order_with_res(res_id, item, qty):
    try:
        with lock:
            conn = get_db()
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO orders (reservation_id, item_name, quantity, time)
                VALUES (?, ?, ?, datetime('now'))
            """, (res_id, item, qty))

            conn.commit()
            conn.close()
        return True
    except Exception as e:
        print("ORDER ERROR:", repr(e))
        return False

