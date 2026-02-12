# 🍽️ SmartDine AI

### Intelligent Restaurant Reservation & Dining Management System

SmartDine AI is an AI-powered restaurant management platform that automates reservations, waitlist handling, menu ordering, and customer engagement using an intelligent chatbot and scalable backend architecture.

---

## 🚀 Key Features

🤖 **AI Reservation Chatbot**

* Natural language interaction
* Multi-step conversation flow
* Session memory
* Intent detection

📅 **Smart Table Booking System**

* Date & time-based booking
* Conflict handling
* Booking status management

⏳ **Waitlist Management**

* Automated queue system
* FIFO handling
* Capacity-based promotion
* Auto-notifications

📲 **SMS Notification System**

* Booking confirmation
* Waitlist alerts
* Reminder messages

🧮 **Table Optimization Algorithm**

* Smart table allocation
* Seat utilization optimization
* Dynamic table grouping



## 🧠 System Architecture

```
UI Layer (Web/App/Chatbot)
        ↓
AI Layer (Chatbot Engine)
        ↓
Business Logic Layer
        ↓
Optimization Engine
        ↓
Data Layer (SQLite → PostgreSQL Ready)
        ↓
Notification Layer (SMS)
        ↓
Admin Analytics Layer
```

## 📁 Project Structure

```
backend/
│
├─ main.py
├─ routes.py
├─ chatbot.py
├─ database.py
├─ db_ops.py
├─ ai_engine.py
├─ optimization.py
├─ analytics.py
├─ admin.py
├─ notification.py
├─ models.py
├─ config.py
└─ utils.py
```

## ⚙️ Tech Stack

* **Backend:** FastAPI (Python)
* **Database:** SQLite (WAL mode, concurrency safe)
* **AI Layer:** Rule-based NLP + session management
* **SMS:** API-based SMS gateway
* **Architecture:** Modular microservice-ready design

---

## 🧪 Core Functional Flows

### Reservation Flow

```
User → Chatbot → Name → Phone → Date → Time → People → DB Save → SMS Confirmation
```

### Waitlist Flow

```
User → Chatbot → Name → Phone → People → DB Save → SMS Notification
```

### Menu Order Flow

```
User → Reservation → Menu → Item → Quantity → DB Save → Order Confirmation
```


## 🎯 Vision

SmartDine AI aims to become a complete **AI-powered restaurant automation platform** that:

* Reduces operational workload
* Improves customer experience
* Optimizes resource utilization
* Enhances business intelligence
* Enables data-driven decisions

---


## 📁 Project Structure

