import tkinter as tk  # Import tkinter library for GUI creation
from tkinter import messagebox  # Import messagebox for pop-up dialogs
from controller.controller import GreenWaveController  # Import controller for business logic

class GreenWaveGUI:
    def __init__(self, root):
        # Initialize the main GUI and controller
        self.controller = GreenWaveController()  # Controller handles data and logic
        self.root = root  # Store reference to the main Tk window
        self.root.title("GreenWave Conference Ticketing System")  # Set window title
        self.root.geometry("600x500")  # Set window size

        # Create a frame to hold widgets
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20)  # Add padding at the top

        # Entry fields for username, password, and email
        self.username_entry = tk.Entry(self.frame, width=30)  # Input for username
        self.password_entry = tk.Entry(self.frame, width=30, show="*")  # Input for password (hidden)
        self.email_entry = tk.Entry(self.frame, width=30)  # Input for email

        # Start the GUI with the login screen
        self.create_login_screen()

    def create_login_screen(self):
        # Create the login interface
        self.clear_frame()  # Remove previous widgets

        # Add username label and entry field
        tk.Label(self.frame, text="Username").grid(row=0, column=0)
        self.username_entry.grid(row=0, column=1)

        # Add password label and entry field
        tk.Label(self.frame, text="Password").grid(row=1, column=0)
        self.password_entry.grid(row=1, column=1)

        # Buttons for login, registration, and admin login
        tk.Button(self.frame, text="Login", command=self.login).grid(row=2, column=0)
        tk.Button(self.frame, text="Register", command=self.create_register_screen).grid(row=2, column=1)
        tk.Button(self.frame, text="Admin Login", command=self.admin_login_screen).grid(row=3, column=0, columnspan=2)

    def create_register_screen(self):
        # Create the registration interface
        self.clear_frame()  # Remove previous widgets

        # Add labels and entry fields for username, password, and email
        tk.Label(self.frame, text="Username").grid(row=0, column=0)
        self.username_entry.grid(row=0, column=1)
        tk.Label(self.frame, text="Password").grid(row=1, column=0)
        self.password_entry.grid(row=1, column=1)
        tk.Label(self.frame, text="Email").grid(row=2, column=0)
        self.email_entry.grid(row=2, column=1)

        # Button to create account
        tk.Button(self.frame, text="Create Account", command=self.register).grid(row=3, column=0, columnspan=2)

        # Button to go back to login screen
        tk.Button(self.frame, text="Back to Login", command=self.create_login_screen).grid(row=4, column=0, columnspan=2)

    def create_dashboard(self):
        # Main user dashboard after login
        self.clear_frame()  # Clear previous widgets

        # Display welcome message with username
        tk.Label(self.frame, text=f"Welcome, {self.controller.logged_in.account.username}!").grid(row=0, column=0)

        # Add buttons for different actions
        tk.Button(self.frame, text="View Details", command=self.show_details).grid(row=1, column=0)
        tk.Button(self.frame, text="Delete Account", command=self.delete_account).grid(row=2, column=0)
        tk.Button(self.frame, text="Ticket Purchase", command=self.ticket_purchase_screen).grid(row=3, column=0)
        tk.Button(self.frame, text="Upgrade Ticket", command=self.upgrade_ticket_screen).grid(row=4, column=0)
        tk.Button(self.frame, text="Logout", command=self.logout).grid(row=5, column=0)

    def cancel_ticket(self):
        # Cancel the user's ticket
        try:
            self.controller.cancel_ticket()  # Call controller to cancel ticket
            messagebox.showinfo("Canceled", "Your ticket has been canceled.")  # Show success message
        except ValueError as e:
            messagebox.showerror("Error", str(e))  # Show error if cancellation fails

    def reserve_workshop_screen(self):
        # Show workshops available for reservation based on user's ticket
        self.clear_frame()  # Clear frame
        workshops = self.controller.get_all_workshops()  # Get list of all workshops
        ticket_exhibitions = self.controller.logged_in.pass_ref.ticket_type.access_exhibitions  # Get exhibitions user has access to

        tk.Label(self.frame, text="Reserve Workshop (based on your ticket access):").pack()

        self.workshop_vars = []  # Store variables for checkboxes
        for w in workshops:
            # Only allow workshops in user's ticket access and with available seats
            if w.exhibition in ticket_exhibitions and w.capacity > 0:
                var = tk.IntVar()  # Create variable for checkbox state
                cb = tk.Checkbutton(
                    self.frame,
                    text=f"{w.title} (Exhibition {w.exhibition}) - Seats left: {w.capacity}",
                    variable=var
                )
                cb.pack(anchor='w')
                self.workshop_vars.append((var, w))  # Store variable and workshop object

        # Buttons to reserve or go back
        tk.Button(self.frame, text="Reserve", command=self.reserve_selected_workshops).pack(pady=10)
        tk.Button(self.frame, text="Back", command=self.create_dashboard).pack()

    def reserve_selected_workshops(self):
        # Reserve workshops that the user selected
        selected = [w for var, w in self.workshop_vars if var.get() == 1]  # List of selected workshops

        if not selected:
            messagebox.showwarning("Select", "Please select at least one workshop")  # Warn if none selected
            return

        try:
            self.controller.reserve_workshops(selected)  # Reserve selected workshops
            messagebox.showinfo("Reserved", "Workshops successfully reserved!")  # Show success
            self.create_dashboard()  # Return to dashboard
        except ValueError as e:
            messagebox.showerror("Error", str(e))  # Show error if reservation fails

    def modify_account_screen(self):
        # Screen to modify user email and password
        self.clear_frame()  # Clear previous widgets

        tk.Label(self.frame, text="New Email").grid(row=0, column=0)
        new_email_entry = tk.Entry(self.frame)
        new_email_entry.grid(row=0, column=1)

        tk.Label(self.frame, text="New Password").grid(row=1, column=0)
        new_pass_entry = tk.Entry(self.frame, show="*")
        new_pass_entry.grid(row=1, column=1)

        # Function to save changes
        def save_changes():
            new_email = new_email_entry.get()  # Get new email
            new_pass = new_pass_entry.get()  # Get new password

            if new_email:
                self.controller.logged_in.account.email = new_email  # Update email
                if new_pass:
                    self.controller.logged_in.account.password = new_pass  # Update password
                self.controller.save_attendees()  # Save changes to storage
                messagebox.showinfo("Updated", "Account information updated")  # Show success
                self.create_dashboard()  # Go back to dashboard

        # Buttons to save changes or go back
        tk.Button(self.frame, text="Save", command=save_changes).grid(row=2, column=0, columnspan=2)
        tk.Button(self.frame, text="Back", command=self.create_dashboard).grid(row=3, column=0, columnspan=2)

    def admin_login_screen(self):
        # Admin login interface
        self.clear_frame()  # Clear previous widgets
        tk.Label(self.frame, text="Admin Username").grid(row=0, column=0)
        self.username_entry.grid(row=0, column=1)
        tk.Label(self.frame, text="Admin Password").grid(row=1, column=0)
        self.password_entry.grid(row=1, column=1)

        # Buttons to login as admin or go back
        tk.Button(self.frame, text="Login as Admin", command=self.admin_login).grid(row=2, column=0, columnspan=2)
        tk.Button(self.frame, text="Back", command=self.create_login_screen).grid(row=3, column=0, columnspan=2)

    def admin_dashboard(self):
        # Admin dashboard for managing the conference
        self.clear_frame()
        tk.Label(self.frame, text="Admin Dashboard").pack()
        tk.Button(self.frame, text="View Sales Reports", command=self.view_sales).pack(pady=5)
        tk.Button(self.frame, text="View Workshop Attendance", command=self.view_workshop_capacity).pack(pady=5)
        tk.Button(self.frame, text="Back", command=self.create_login_screen).pack(pady=5)

    def view_sales(self):
        # Show sales reports
        reports = self.controller.get_sales_reports()
        if not reports:
            messagebox.showinfo("Sales Report", "No reports available.")
            return

        msg = ""
        for report in reports:
            # Format report information
            msg += f"Date: {report.date}\nTickets Sold: {report.tickets_sold}\nTotal Sales: AED {report.total_sales}\n\n"
        messagebox.showinfo("Sales Report", msg)

    def view_workshop_capacity(self):
        # Show remaining capacity for all workshops
        workshops = self.controller.get_all_workshops()
        msg = ""
        for w in workshops:
            msg += f"{w.title} (Exhibition {w.exhibition}) - Seats left: {w.capacity}\n"
        messagebox.showinfo("Workshop Attendance", msg)

    def admin_login(self):
        # Validate admin credentials
        username = self.username_entry.get()
        password = self.password_entry.get()
        try:
            if self.controller.validate_admin(username, password):
                self.admin_dashboard()  # Open admin dashboard if valid
            else:
                messagebox.showerror("Error", "Invalid admin credentials")
        except:
            messagebox.showerror("Error", "Error during admin login")

    def ticket_purchase_screen(self):
        # Interface to purchase tickets
        self.clear_frame()
        tk.Label(self.frame, text="Choose Ticket Type:").pack()

        self.ticket_vars = []  # Store selected ticket
        for ticket in self.controller.ticket_types:
            var = tk.IntVar()
            # Radio button for each ticket type
            cb = tk.Radiobutton(self.frame, text=f"{ticket.name} - AED {ticket.price}", variable=var, value=1)
            cb.pack(anchor='w')
            self.ticket_vars.append((var, ticket))

        # Payment method selection
        tk.Label(self.frame, text="Select Payment Method:").pack()
        self.payment_method = tk.StringVar()
        tk.Radiobutton(self.frame, text="Credit Card", variable=self.payment_method, value="credit").pack(anchor='w')
        tk.Radiobutton(self.frame, text="Debit Card", variable=self.payment_method, value="debit").pack(anchor='w')
        tk.Radiobutton(self.frame, text="Apple Pay", variable=self.payment_method, value="apple").pack(anchor='w')

        # Card number entry
        tk.Label(self.frame, text="Card Number").pack()
        self.card_entry = tk.Entry(self.frame)
        self.card_entry.pack()

        # Buttons to purchase or go back
        tk.Button(self.frame, text="Purchase", command=self.purchase_ticket).pack(pady=10)
        tk.Button(self.frame, text="Back", command=self.create_dashboard).pack()

    def purchase_ticket(self):
        # Handle ticket purchase logic
        if not self.controller.logged_in:
            messagebox.showerror("Error", "Please login first")
            return

        chosen_ticket = None
        for var, ticket in self.ticket_vars:
            if var.get() == 1:
                chosen_ticket = ticket
                break

        if not chosen_ticket:
            messagebox.showerror("Error", "Please select a ticket")
            return

        if not self.card_entry.get().isdigit():
            messagebox.showerror("Error", "Invalid card number")
            return

        # Call controller to process purchase
        self.controller.purchase_ticket(chosen_ticket, self.payment_method.get())
        messagebox.showinfo("Success", "Ticket purchased successfully")
        self.create_dashboard()

    def upgrade_ticket_screen(self):
        # Interface to upgrade ticket
        self.clear_frame()
        if not self.controller.logged_in:
            messagebox.showerror("Error", "Please login first")
            return

        current = self.controller.logged_in.pass_ref.ticket_type
        tk.Label(self.frame, text=f"Current Ticket: {current.name}").pack(pady=10)
        tk.Label(self.frame, text="Select upgrade:").pack()

        self.upgrade_options = []
        for ticket in self.controller.ticket_types:
            # Only show tickets more expensive than current
            if ticket.price > current.price:
                var = tk.IntVar()
                tk.Radiobutton(self.frame, text=f"{ticket.name} - AED {ticket.price}", variable=var, value=1).pack(anchor='w')
                self.upgrade_options.append((var, ticket))

        tk.Button(self.frame, text="Upgrade", command=self.upgrade_ticket).pack(pady=10)
        tk.Button(self.frame, text="Back", command=self.create_dashboard).pack()

    def upgrade_ticket(self):
        # Handle ticket upgrade logic
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

    def login(self):
        # User login function
        username = self.username_entry.get()
        password = self.password_entry.get()
        try:
            self.controller.login(username, password)  # Validate credentials
            self.create_dashboard()  # Go to dashboard if successful
        except ValueError as e:
            messagebox.showerror("Login Failed", str(e))

    def register(self):
        # Create new user account
        username = self.username_entry.get()
        password = self.password_entry.get()
        email = self.email_entry.get()
        try:
            self.controller.create_account(username, password, email)
            messagebox.showinfo("Success", "Account created! You may now login.")
            self.create_login_screen()  # Return to login screen
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def show_details(self):
        # Show user account information
        att = self.controller.logged_in
        ticket = att.pass_ref.ticket_type.name if att.pass_ref else "No Ticket"
        msg = f"Username: {att.account.username}\nEmail: {att.account.email}\nTicket: {ticket}"
        messagebox.showinfo("Your Details", msg)

    def delete_account(self):
        # Delete the logged-in user account
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete your account?")
        if confirm:
            self.controller.delete_logged_in_account()  # Delete account in controller
            messagebox.showinfo("Deleted", "Your account has been deleted.")
            self.create_login_screen()  # Return to login screen

    def logout(self):
        # Logout current user
        self.controller.logged_in = None
        self.create_login_screen()  # Go back to login screen

    def clear_frame(self):
        # Remove all widgets from the frame
        for widget in self.frame.winfo_children():
            widget.destroy()

if __name__ == '__main__':
    # Run the application
    root = tk.Tk()
    app = GreenWaveGUI(root)
    root.mainloop()
