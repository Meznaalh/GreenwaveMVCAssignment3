# GreenwaveMVCAssignment3

# 🎟️ GreenWave Conference Ticketing & Session Management System

This Python application is built using the **MVC (Model-View-Controller)** architecture with **Tkinter** for GUI and **Pickle** for data persistence. It simulates an event system where users (attendees) can create accounts, buy tickets, reserve workshops, and more. Admins can also monitor ticket sales and workshop attendance.

---

## 📁 Folder Structure
GreenWave/
├── main.py

├── model/

│ └── models.py

├── view/

│ └── gui.py

├── controller/

│ └── controller.py

├── attendees.pkl # Automatically created

├── README.md


---

## 💡 Features

### ✅ Attendee Interface
- Create Account / Login
- Modify or Delete Profile
- Buy or Upgrade Tickets
- Reserve/Cancel Workshops (with validation for capacity & ticket access)

### ✅ Admin Dashboard
- View ticket sales per day
- Monitor workshop capacities
- Upgrade attendee tickets

### ✅ Ticket Purchasing
- Choose from 3 ticket types: Single / Double / Full Access
- View price, features, and access scope
- Integrated payment confirmation

### ✅ Data Persistence
- All data is saved to `.pkl` files using Python's `pickle` module.
- If data files do not exist, they are automatically created.

### ✅ Error Handling
- Uses `try/except` blocks for login, account creation, reservations, etc.
- Specific exceptions like `ValueError` are handled with helpful GUI messages.

---

Testing & Validation

Test files (attendees.pkl, etc.) are generated during runtime.

Try all user flows:

 - Create account → Buy ticket → Reserve workshop → Logout

 - Login → Modify profile → Cancel reservation → Upgrade ticket

 - Admin Login → View reports → Monitor workshop → Logout

Screenshots of working test cases are available in the final report.



