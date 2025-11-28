import tkinter as tk  # Tkinter library for GUI creation
from tkinter import messagebox  # Message boxes for alerts and confirmations
from controller.controller import GreenWaveController  # Controller for business logic (MVC)


class GreenWaveGUI:
    """Main GUI class for the GreenWave Conference Ticketing System"""

    def __init__(self, root):
        """Constructor to initialize the GUI components and controller"""
        self.controller = GreenWaveController()  # Create controller object
        self.root = root  # Reference to the main Tk window
        self.root.title("GreenWave Conference Ticketing System")  # Window title
        self.root.geometry("600x500")  # Window size

        # Main container frame where all widgets are placed
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20)

        # Entry fields for user input
        self.username_entry = tk.Entry(self.frame, width=30)  # Username input
        self.password_entry = tk.Entry(self.frame, width=30, show="*")  # Password input (hidden)
        self.email_entry = tk.Entry(self.frame, width=30)  # Email input

        # Start application with the login screen
        self.create_login_screen()

    # --------------------------------------------------
    # LOGIN & REGISTRATION SCREENS
    # --------------------------------------------------

    def create_login_screen(self):
        """Displays the login screen"""
        self.clear_frame()  # Remove all previous widgets from the frame

        # Username label and input field
        tk.Label(self.frame, text="Username").grid(row=0, column=0)
        self.username_entry.grid(row=0, column=1)

        # Password label and input field
        tk.Label(self.frame, text="Password").grid(row=1, column=0)
        self.password_entry.grid(row=1, column=1)

        # Buttons for user actions
        tk.Button(self.frame, text="Login", command=self.login).grid(row=2, column=0)  # User login
        tk.Button(self.frame, text="Register", command=self.create_register_screen).grid(row=2, column=1)  # Register page
        tk.Button(self.frame, text="Admin Login", command=self.admin_login_screen).grid(row=3, column=0, columnspan=2)

    def create_register_screen(self):
        """Displays the registration screen"""
        self.clear_frame()

        # Username input
        tk.Label(self.frame, text="Username").grid(row=0, column=0)
        self.username_entry.grid(row=0, column=1)

        # Password input
        tk.Label(self.frame, text="Password").grid(row=1, column=0)
        self.password_entry.grid(row=1, column=1)

        # Email input
        tk.Label(self.frame, text="Email").grid(row=2, column=0)
        self.email_entry.grid(row=2, column=1)

        # Buttons for account creation and returning to login
        tk.Button(self.frame, text="Create Account", command=self.register).grid(row=3, column=0, columnspan=2)
        tk.Button(self.frame, text="Back", command=self.create_login_screen).grid(row=4, column=0, columnspan=2)

    # --------------------------------------------------
    # USER DASHBOARD
    # --------------------------------------------------

    def create_dashboard(self):
        """Displays the user dashboard after successful login"""
        self.clear_frame()

        # Welcome message
        tk.Label(self.frame, text=f"Welcome, {self.controller.logged_in.account.username}!").grid(row=0, column=0)

        # Dashboard buttons
        tk.Button(self.frame, text="View Details", command=self.show_details).grid(row=1, column=0)
        tk.Button(self.frame, text="Modify Account", command=self.modify_account_screen).grid(row=2, column=0)
        tk.Button(self.frame, text="Ticket Purchase", command=self.ticket_purchase_screen).grid(row=3, column=0)
        tk.Button(self.frame, text="Upgrade Ticket", command=self.upgrade_ticket_screen).grid(row=4, column=0)
        tk.Button(self.frame, text="Reserve Workshop", command=self.reserve_workshop_screen).grid(row=5, column=0)
        tk.Button(self.frame, text="Delete Account", command=self.delete_account).grid(row=6, column=0)
        tk.Button(self.frame, text="Logout", command=self.logout).grid(row=7, column=0)

    # --------------------------------------------------
    # WORKSHOP RESERVATION
    # --------------------------------------------------

    def reserve_workshop_screen(self):
        """Displays available workshops for reservation"""
        self.clear_frame()

        # Get all workshops from controller
        workshops = self.controller.get_all_workshops()

        # Get exhibitions allowed for the user based on their ticket
        ticket_exhibitions = self.controller.logged_in.pass_ref.ticket_type.access_exhibitions

        tk.Label(self.frame, text="Reserve Workshop").pack()

        self.workshop_vars = []  # Stores selected workshops

        # Display only allowed workshops with available capacity
        for w in workshops:
            if w.exhibition in ticket_exhibitions and w.capacity > 0:
                var = tk.IntVar()
                tk.Checkbutton(
                    self.frame,
                    text=f"{w.title} - Seats Left: {w.capacity}",
                    variable=var
                ).pack(anchor="w")
                self.workshop_vars.append((var, w))

        tk.Button(self.frame, text="Reserve", command=self.reserve_selected_workshops).pack(pady=10)
        tk.Button(self.frame, text="Back", command=self.create_dashboard).pack()

    def reserve_selected_workshops(self):
        """Reserves the selected workshops"""
        selected = [w for var, w in self.workshop_vars if var.get() == 1]

        if not selected:
            messagebox.showwarning("Warning", "Please select at least one workshop")
            return

        try:
            self.controller.reserve_workshops(selected)
            messagebox.showinfo("Success", "Workshop(s) reserved successfully")
            self.create_dashboard()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    # --------------------------------------------------
    # ACCOUNT MODIFICATION
    # --------------------------------------------------

    def modify_account_screen(self):
        """Allows user to update email and password"""
        self.clear_frame()

        tk.Label(self.frame, text="New Email").grid(row=0, column=0)
        new_email = tk.Entry(self.frame)
        new_email.grid(row=0, column=1)

        tk.Label(self.frame, text="New Password").grid(row=1, column=0)
        new_password = tk.Entry(self.frame, show="*")
        new_password.grid(row=1, column=1)

        def save():
            if new_email.get():
                self.controller.logged_in.account.email = new_email.get()
            if new_password.get():
                self.controller.logged_in.account.password = new_password.get()

            self.controller.save_attendees()
            messagebox.showinfo("Success", "Account updated successfully")
            self.create_dashboard()

        tk.Button(self.frame, text="Save", command=save).grid(row=2, column=0, columnspan=2)
        tk.Button(self.frame, text="Back", command=self.create_dashboard).grid(row=3, column=0, columnspan=2)

    # --------------------------------------------------
    # ADMIN FUNCTIONS
    # --------------------------------------------------

    def admin_login_screen(self):
        """Admin login interface"""
        self.clear_frame()

        tk.Label(self.frame, text="Admin Username").grid(row=0, column=0)
        self.username_entry.grid(row=0, column=1)

        tk.Label(self.frame, text="Admin Password").grid(row=1, column=0)
        self.password_entry.grid(row=1, column=1)

        tk.Button(self.frame, text="Login", command=self.admin_login).grid(row=2, column=0, columnspan=2)
        tk.Button(self.frame, text="Back", command=self.create_login_screen).grid(row=3, column=0, columnspan=2)

    def admin_dashboard(self):
        """Dashboard for administrator"""
        self.clear_frame()

        tk.Label(self.frame, text="Admin Dashboard").pack()
        tk.Button(self.frame, text="View Sales Reports", command=self.view_sales).pack()
        tk.Button(self.frame, text="View Workshop Attendance", command=self.view_workshop_capacity).pack()
        tk.Button(self.frame, text="Back", command=self.create_login_screen).pack()

    def admin_login(self):
        """Validates admin credentials"""
        try:
            if self.controller.validate_admin(self.username_entry.get(), self.password_entry.get()):
                self.admin_dashboard()
            else:
                messagebox.showerror("Error", "Invalid admin credentials")
        except:
            messagebox.showerror("Error", "Login failed")

    # --------------------------------------------------
    # TICKET PURCHASE & UPGRADE
    # --------------------------------------------------

    def ticket_purchase_screen(self):
        """Allows users to purchase tickets"""
        self.clear_frame()

        tk.Label(self.frame, text="Choose Ticket Type").pack()

        self.ticket_vars = []
        for ticket in self.controller.ticket_types:
            var = tk.IntVar()
            tk.Radiobutton(self.frame, text=f"{ticket.name} - AED {ticket.price}", variable=var, value=1).pack(anchor="w")
            self.ticket_vars.append((var, ticket))

        self.payment_method = tk.StringVar()
        tk.Label(self.frame, text="Payment Method").pack()
        tk.Radiobutton(self.frame, text="Credit Card", variable=self.payment_method, value="credit").pack(anchor="w")
        tk.Radiobutton(self.frame, text="Debit Card", variable=self.payment_method, value="debit").pack(anchor="w")
        tk.Radiobutton(self.frame, text="Apple Pay", variable=self.payment_method, value="apple").pack(anchor="w")

        tk.Label(self.frame, text="Card Number").pack()
        self.card_entry = tk.Entry(self.frame)
        self.card_entry.pack()

        tk.Button(self.frame, text="Purchase", command=self.purchase_ticket).pack(pady=10)
        tk.Button(self.frame, text="Back", command=self.create_dashboard).pack()

    def purchase_ticket(self):
        """Processes ticket purchase transaction"""
        if not self.card_entry.get().isdigit():
            messagebox.showerror("Error", "Invalid Card Number")
            return

        chosen = None
        for var, ticket in self.ticket_vars:
            if var.get() == 1:
                chosen = ticket
                break

        if not chosen:
            messagebox.showerror("Error", "Please select a ticket")
            return

        self.controller.purchase_ticket(chosen, self.payment_method.get())
        messagebox.showinfo("Success", "Ticket Purchased Successfully")
        self.create_dashboard()

    def upgrade_ticket_screen(self):
        """Allows users to upgrade their ticket"""
        self.clear_frame()

        current = self.controller.logged_in.pass_ref.ticket_type
        tk.Label(self.frame, text=f"Current Ticket: {current.name}").pack()

        self.upgrade_options = []
        for ticket in self.controller.ticket_types:
            if ticket.price > current.price:
                var = tk.IntVar()
                tk.Radiobutton(self.frame, text=ticket.name, variable=var, value=1).pack(anchor="w")
                self.upgrade_options.append((var, ticket))

        tk.Button(self.frame, text="Upgrade", command=self.upgrade_ticket).pack()
        tk.Button(self.frame, text="Back", command=self.create_dashboard).pack()

    def upgrade_ticket(self):
        """Handles ticket upgrade"""
        selected = None
        for var, ticket in self.upgrade_options:
            if var.get() == 1:
                selected = ticket
                break

        if not selected:
            messagebox.showerror("Error", "Select an upgrade")
            return

        self.controller.upgrade_ticket(selected)
        messagebox.showinfo("Success", "Ticket upgraded")
        self.create_dashboard()

    # --------------------------------------------------
    # BASIC USER OPERATIONS
    # --------------------------------------------------

    def login(self):
        """Logs in a user"""
        try:
            self.controller.login(self.username_entry.get(), self.password_entry.get())
            self.create_dashboard()
        except ValueError as e:
            messagebox.showerror("Login Failed", str(e))

    def register(self):
        """Registers a new attendee"""
        try:
            self.controller.create_account(
                self.username_entry.get(),
                self.password_entry.get(),
                self.email_entry.get()
            )
            messagebox.showinfo("Success", "Account created")
            self.create_login_screen()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def show_details(self):
        """Displays logged-in user details"""
        att = self.controller.logged_in
        msg = f"Username: {att.account.username}\nEmail: {att.account.email}"
        messagebox.showinfo("Details", msg)

    def delete_account(self):
        """Deletes the current user account"""
        if messagebox.askyesno("Confirm", "Delete your account?"):
            self.controller.delete_logged_in_account()
            self.create_login_screen()

    def logout(self):
        """Logs out the current user"""
        self.controller.logged_in = None
        self.create_login_screen()

    def clear_frame(self):
        """Clears all widgets in the frame"""
        for widget in self.frame.winfo_children():
            widget.destroy()


# --------------------------------------------------
# PROGRAM ENTRY POINT
# --------------------------------------------------

if __name__ == "__main__":
    root = tk.Tk()  # Create the Tkinter root window
    app = GreenWaveGUI(root)  # Create GUI object
    root.mainloop()  # Start the event loop
