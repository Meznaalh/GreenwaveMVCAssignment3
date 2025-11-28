# --------------------------------------------------
# GUI MODULE FOR GREENWAVE CONFERENCE SYSTEM
# This file represents the VIEW layer in the MVC architecture.
# It handles all user interaction using Tkinter.
# --------------------------------------------------

import tkinter as tk                      # Tkinter library for GUI creation
from tkinter import messagebox            # Message boxes for alerts and confirmations
from controller.controller import GreenWaveController   # Controller (business logic layer)


class GreenWaveGUI:
    """Main GUI class for the GreenWave Conference Ticketing System"""

    def __init__(self, root):
        """
        Constructor that initializes the main window and controller.
        This method runs only once when the application starts.
        """
        self.controller = GreenWaveController()   # Create controller object (MVC connection)
        self.root = root                          # Reference to the main Tkinter window
        self.root.title("GreenWave Conference Ticketing System")   # Window title
        self.root.geometry("600x500")             # Window size

        # Main container frame that holds all widgets
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20)

        # Load login screen when program starts
        self.create_login_screen()

    # --------------------------------------------------
    # UTILITY FUNCTION
    # --------------------------------------------------

    def clear_frame(self):
        """
        Removes all widgets from the current frame.
        This allows screen switching inside the same window.
        """
        for widget in self.frame.winfo_children():
            widget.destroy()

    # --------------------------------------------------
    # LOGIN & REGISTRATION SCREENS
    # --------------------------------------------------

    def create_login_screen(self):
        """Displays the user login screen"""
        self.clear_frame()

        # Username input
        tk.Label(self.frame, text="Username").grid(row=0, column=0)
        self.username_entry = tk.Entry(self.frame, width=30)
        self.username_entry.grid(row=0, column=1)

        # Password input (hidden)
        tk.Label(self.frame, text="Password").grid(row=1, column=0)
        self.password_entry = tk.Entry(self.frame, width=30, show="*")
        self.password_entry.grid(row=1, column=1)

        # Buttons for navigation
        tk.Button(self.frame, text="Login", command=self.login).grid(row=2, column=0)
        tk.Button(self.frame, text="Register", command=self.create_register_screen).grid(row=2, column=1)
        tk.Button(self.frame, text="Admin Login", command=self.admin_login_screen).grid(
            row=3, column=0, columnspan=2)

    def create_register_screen(self):
        """Displays the account registration screen"""
        self.clear_frame()

        tk.Label(self.frame, text="Username").grid(row=0, column=0)
        self.username_entry = tk.Entry(self.frame, width=30)
        self.username_entry.grid(row=0, column=1)

        tk.Label(self.frame, text="Password").grid(row=1, column=0)
        self.password_entry = tk.Entry(self.frame, width=30, show="*")
        self.password_entry.grid(row=1, column=1)

        tk.Label(self.frame, text="Email").grid(row=2, column=0)
        self.email_entry = tk.Entry(self.frame, width=30)
        self.email_entry.grid(row=2, column=1)

        tk.Button(self.frame, text="Create Account", command=self.register).grid(
            row=3, column=0, columnspan=2)
        tk.Button(self.frame, text="Back to Login", command=self.create_login_screen).grid(
            row=4, column=0, columnspan=2)

    # --------------------------------------------------
    # USER DASHBOARD
    # --------------------------------------------------

    def create_dashboard(self):
        """Displays the dashboard for a logged-in user"""
        self.clear_frame()

        tk.Label(self.frame,
                 text=f"Welcome, {self.controller.logged_in.account.username}!"
                 ).grid(row=0, column=0)

        tk.Button(self.frame, text="View Details", command=self.show_details).grid(row=1, column=0)
        tk.Button(self.frame, text="Modify Account", command=self.modify_account_screen).grid(row=2, column=0)
        tk.Button(self.frame, text="Ticket Purchase", command=self.ticket_purchase_screen).grid(row=3, column=0)
        tk.Button(self.frame, text="Upgrade Ticket", command=self.upgrade_ticket_screen).grid(row=4, column=0)
        tk.Button(self.frame, text="Delete Account", command=self.delete_account).grid(row=5, column=0)
        tk.Button(self.frame, text="Logout", command=self.logout).grid(row=6, column=0)

    # --------------------------------------------------
    # ACCOUNT OPERATIONS
    # --------------------------------------------------

    def show_details(self):
        """Displays logged-in attendee details"""
        att = self.controller.logged_in
        ticket = att.pass_ref.ticket_type.name if att.pass_ref else "No Ticket"
        message = (
            f"Username: {att.account.username}\n"
            f"Email: {att.account.email}\n"
            f"Ticket: {ticket}"
        )
        messagebox.showinfo("Your Details", message)

    def modify_account_screen(self):
        """Allows the user to update email and password"""
        self.clear_frame()

        tk.Label(self.frame, text="New Email").grid(row=0, column=0)
        new_email = tk.Entry(self.frame)
        new_email.grid(row=0, column=1)

        tk.Label(self.frame, text="New Password").grid(row=1, column=0)
        new_pass = tk.Entry(self.frame, show="*")
        new_pass.grid(row=1, column=1)

        def save():
            """Save modified account details"""
            if new_email.get():
                self.controller.logged_in.account.email = new_email.get()
            if new_pass.get():
                self.controller.logged_in.account.password = new_pass.get()

            self.controller.save_attendees()   # Persist changes using Pickle
            messagebox.showinfo("Success", "Account updated successfully")
            self.create_dashboard()

        tk.Button(self.frame, text="Save", command=save).grid(row=2, column=0, columnspan=2)
        tk.Button(self.frame, text="Back", command=self.create_dashboard).grid(row=3, column=0, columnspan=2)

    def delete_account(self):
        """Deletes the currently logged-in user account"""
        if messagebox.askyesno("Confirm", "Are you sure you want to delete your account?"):
            self.controller.delete_logged_in_account()
            messagebox.showinfo("Deleted", "Account deleted successfully")
            self.create_login_screen()

    def logout(self):
        """Logs the user out and returns to login screen"""
        self.controller.logged_in = None
        self.create_login_screen()

    # --------------------------------------------------
    # LOGIN & REGISTRATION LOGIC
    # --------------------------------------------------

    def login(self):
        """Validates user login credentials through the controller"""
        try:
            self.controller.login(
                self.username_entry.get(),
                self.password_entry.get()
            )
            self.create_dashboard()
        except ValueError as e:
            messagebox.showerror("Login Failed", str(e))

    def register(self):
        """Registers a new attendee account"""
        try:
            self.controller.create_account(
                self.username_entry.get(),
                self.password_entry.get(),
                self.email_entry.get()
            )
            messagebox.showinfo("Success", "Account created successfully!")
            self.create_login_screen()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    # --------------------------------------------------
    # TICKET MANAGEMENT
    # --------------------------------------------------

    def ticket_purchase_screen(self):
        """Displays ticket purchasing interface"""
        self.clear_frame()
        tk.Label(self.frame, text="Choose Ticket Type").pack()

        self.ticket_vars = []
        for ticket in self.controller.ticket_types:
            var = tk.IntVar()
            tk.Radiobutton(
                self.frame,
                text=f"{ticket.name} - AED {ticket.price}",
                variable=var,
                value=1
            ).pack(anchor="w")
            self.ticket_vars.append((var, ticket))

        # Payment selection
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
        messagebox.showinfo("Success", "Ticket purchased successfully")
        self.create_dashboard()

    def upgrade_ticket_screen(self):
        """Allows a user to upgrade their ticket"""
        self.clear_frame()

        current = self.controller.logged_in.pass_ref.ticket_type
        tk.Label(self.frame, text=f"Current Ticket: {current.name}").pack()

        self.upgrade_options = []
        for ticket in self.controller.ticket_types:
            if ticket.price > current.price:
                var = tk.IntVar()
                tk.Radiobutton(
                    self.frame,
                    text=f"{ticket.name} - AED {ticket.price}",
                    variable=var,
                    value=1
                ).pack(anchor="w")
                self.upgrade_options.append((var, ticket))

        tk.Button(self.frame, text="Upgrade", command=self.upgrade_ticket).pack(pady=10)
        tk.Button(self.frame, text="Back", command=self.create_dashboard).pack()

    def upgrade_ticket(self):
        """Processes ticket upgrade"""
        selected = None
        for var, ticket in self.upgrade_options:
            if var.get() == 1:
                selected = ticket
                break

        if not selected:
            messagebox.showerror("Error", "Please select an upgrade")
            return

        self.controller.upgrade_ticket(selected)
        messagebox.showinfo("Success", "Ticket upgraded successfully")
        self.create_dashboard()

    # --------------------------------------------------
    # ADMIN MODULE (TEMP DISABLED FOR STABILITY)
    # --------------------------------------------------

    def admin_login_screen(self):
        """Admin functions temporarily disabled for testing"""
        messagebox.showinfo("Info", "Admin module will be activated after controller completion.")
