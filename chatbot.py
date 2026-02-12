from SMS import send_sms
from dotenv import load_dotenv
from db_ops import add_to_waitlist, save_reservation, save_order_with_res
from database import get_db
import os

load_dotenv()

user_sessions = {}

def chatbot_response(message: str, user_id="web"):
    msg = message.lower().strip()

    if user_id not in user_sessions:
        user_sessions[user_id] = {"step": None, "data": {}}

    session = user_sessions[user_id]

    # ---------------- GREETING ----------------
    if msg in ["hi", "hello", "hey"]:
        return "🤖 Hello 👋 I'm SmartDine AI. You can say: book table, waitlist, menu"

    # ---------------- MENU ----------------
    if msg == "menu":
        session["step"] = "menu_select"
        return """📋 Menu:
1. Pizza
2. Burger
3. Pasta
4. Coffee
5. Paneer Tikka
6. Biriyani

👉 Type item name to order
"""

    # ===============================
    # START RESERVATION FLOW
    # ===============================
    if ("book" in msg or "reserve" in msg) and session["step"] is None:
        session["step"] = "res_name"
        session["data"] = {}
        return "😊 Reservation started!\n👤 Enter your name:"

    # ===============================
    # START WAITLIST FLOW
    # ===============================
    if "waitlist" in msg and session["step"] is None:
        session["step"] = "wait_name"
        session["data"] = {}
        return "⏳ Waitlist started. What's your name?"

    # ==================================================
    # ---------------- RESERVATION STEPS ----------------
    # ==================================================

    if session["step"] == "res_name":
        session["data"]["name"] = message
        session["step"] = "res_phone"
        return "📞 Enter phone number:"

    if session["step"] == "res_phone":
        session["data"]["phone"] = message
        session["step"] = "res_date"
        return "📅 Enter date (YYYY-MM-DD):"

    if session["step"] == "res_date":
        session["data"]["date"] = message
        session["step"] = "res_time"
        return "⏰ Enter time (HH:MM):"

    if session["step"] == "res_time":
        session["data"]["time"] = message
        session["step"] = "res_people"
        return "👥 Number of people:"

    # -------- SAVE RESERVATION --------
    if session["step"] == "res_people":
        try:
            session["data"]["people"] = int(message)
        except:
            return "❌ Enter valid number"

        data = session["data"]

        try:
            conn = get_db()
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO reservations(name, phone, date, time, people, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                data["name"],
                data["phone"],
                data["date"],
                data["time"],
                data["people"],
                "CONFIRMED"
            ))

            res_id = cur.lastrowid
            conn.commit()
            conn.close()

            try:
                send_sms(data["phone"], "🎉 Your table is booked at SmartDine AI 🍽️")
            except:
                pass

            session["data"]["res_id"] = res_id
            session["step"] = "preorder_ask"

            return """✅ Reservation Confirmed 🎉

Would you like to pre-order food? 🍽️
Type: yes / no
"""

        except Exception as e:
            print("Reservation DB Error:", e)
            session["step"] = None
            return "❌ Reservation failed due to server error"

    # -------- PRE-ORDER FLOW --------
    if session["step"] == "preorder_ask":
        if msg == "yes":
            session["step"] = "preorder_item"
            return """📋 Menu:
1. Pizza
2. Burger
3. Pasta
4. Coffee
5. Paneer Tikka
6. Biriyani

👉 Type item name:
"""
        else:
            user_sessions[user_id] = {"step": None, "data": {}}
            return "🎉 Reservation completed successfully without pre-order ❤️"

    if session["step"] == "preorder_item":
        session["data"]["item"] = message
        session["step"] = "preorder_qty"
        return "🔢 Enter quantity:"

    if session["step"] == "preorder_qty":
        try:
            qty = int(message)
        except:
            return "❌ Enter valid quantity"

        data = session["data"]

        # save order
        save_order_with_res(data["name"], data["item"], qty)

        user_sessions[user_id] = {"step": None, "data": {}}

        return f"""🎉 Reservation + Order Successful!

👤 {data['name']}
📞 {data['phone']}
📅 {data['date']} ⏰ {data['time']}
👥 {data['people']} people
🍽 {data['item']} x {qty}

Thank you for choosing SmartDine AI ❤️
"""

    # ==================================================
    # ---------------- WAITLIST STEPS ----------------
    # ==================================================

    if session["step"] == "wait_name":
        session["data"]["name"] = message
        session["step"] = "wait_phone"
        return "📞 Enter phone number:"

    if session["step"] == "wait_phone":
        session["data"]["phone"] = message
        session["step"] = "wait_people"
        return "👥 Number of people?"

    if session["step"] == "wait_people":
        try:
            session["data"]["people"] = int(message)
        except:
            return "❌ Enter valid number"

        data = session["data"]

        success = add_to_waitlist(data["name"], data["phone"], data["people"])

        user_sessions[user_id] = {"step": None, "data": {}}

        if success:
            try:
                send_sms(data["phone"], "⏳ You're added to SmartDine AI waitlist 🍽️")
            except:
                pass

            return f"⏳ {data['name']}, you're added to waitlist successfully!"
        else:
            return "❌ Waitlist failed. Database busy, try again."

    # ==================================================
    # ---------------- MENU ORDER ONLY ----------------
    # ==================================================
    if session["step"] == "menu_select":
        item = message.strip()
        user = session["data"].get("name", "guest")

        success = save_order_with_res(user, item, 1)

        session["step"] = None

        if success:
            return f"✅ {item} order placed successfully! 🍽️"
        else:
            return "❌ Order failed. Try again."

    # ---------------- SMALL TALK ----------------
    if msg in ["ok", "okk", "okay", "done", "thik ahe", "thik"]:
        return "😊 Perfect! Let me know if you need anything else."

    if msg in ["bye", "goodbye", "exit", "close"]:
        return "👋 Bye! Thanks for using SmartDine AI. Have a great day 🍽️✨"

    if msg in ["thank you", "thanks"]:
        return "🙏 You're welcome!"

    # ---------------- DEFAULT ----------------
    return "🤖 You can say: book table / waitlist / menu"
