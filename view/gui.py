import tkinter as tk                          # Import tkinter library to build the GUI
from tkinter import messagebox              # Import messagebox for popup messages
from controller.controller import GreenWaveController  # Import controller (MVC logic)

class GreenWaveGUI:
    """
    This class represents the graphical user interface (View layer)
    of the GreenWave Conference System.
    It communicates with the Controller to perform actions.
    """

    def __init__(self, root):
        # Create the controller object (connects GUI to Model)
        self.controller = GreenWaveController()

        # Store reference to the main application window
        self.root = root
        self.root.title("GreenWave Conference System")  # Window title
        self.root.geometry("500x500")                   # Window size

        # Main frame that holds all GUI widgets
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        # Tkinter variables used to store user input
        self.username = tk.StringVar()  # Stores entered username
        self.password = tk.StringVar()  # Stores entered password
        self.email = tk.StringVar()     # Stores entered email
        self.payment = tk.StringVar()   # Stores payment method

        # Start the application with the login screen
        self.create_login_screen()

    def clear_frame(self):
        """
        Removes all existing widgets from the frame.
        Used when switching between different screens.
        """
        for w in self.frame.winfo_children():
            w.destroy()

    # ---------------- LOGIN ----------------
    def create_login_screen(self):
        """
        Creates the login screen where users or admins can log in.
        """
        self.clear_frame()

        tk.Label(self.frame, text="Username").pack()
        tk.Entry(self.frame, textvariable=self.username).pack()

        tk.Label(self.frame, text="Password").pack()
        tk.Entry(self.frame, textvariable=self.password, show="*").pack()

        tk.Button(self.frame, text="Login", command=self.login).pack()
        tk.Button(self.frame, text="Register", command=self.create_register_screen).pack()
        tk.Button(self.frame, text="Admin Login", command=self.admin_login_screen).pack()

    # ---------------- REGISTER ----------------
    def create_register_screen(self):
        """
        Screen for creating a new attendee account.
        """
        self.clear_frame()

        tk.Label(self.frame, text="Username").pack()
        tk.Entry(self.frame, textvariable=self.username).pack()

        tk.Label(self.frame, text="Password").pack()
        tk.Entry(self.frame, textvariable=self.password, show="*").pack()

        tk.Label(self.frame, text="Email").pack()
        tk.Entry(self.frame, textvariable=self.email).pack()

        tk.Button(self.frame, text="Create", command=self.register).pack()
        tk.Button(self.frame, text="Back", command=self.create_login_screen).pack()

    # ---------------- DASHBOARD ----------------
    def create_dashboard(self):
        """
        Main dashboard shown after successful attendee login.
        Provides access to all user functionalities.
        """
        self.clear_frame()
        tk.Button(self.frame, text="View Details", command=self.show_details).pack()
        tk.Button(self.frame, text="Purchase Ticket", command=self.purchase_screen).pack()
        tk.Button(self.frame, text="Upgrade Ticket", command=self.upgrade_screen).pack()
        tk.Button(self.frame, text="Reserve Workshop", command=self.reserve_screen).pack()
        tk.Button(self.frame, text="Delete Account", command=self.delete_account).pack()
        tk.Button(self.frame, text="Logout", command=self.logout).pack()

    # ---------------- USER FUNCTIONS ----------------
    def login(self):
        """
        Logs in the user using the controller.
        """
        try:
            self.controller.login(self.username.get(), self.password.get())
            self.create_dashboard()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def register(self):
        """
        Creates a new user account using the controller.
        """
        try:
            self.controller.create_account(
                self.username.get(),
                self.password.get(),
                self.email.get()
            )
            messagebox.showinfo("Success", "Account created")
            self.create_login_screen()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def show_details(self):
        """
        Displays the logged-in attendee's account and ticket information.
        """
        att = self.controller.logged_in
        ticket = att.pass_ref.ticket_type.name if att.pass_ref else "None"
        messagebox.showinfo(
            "Details",
            f"Username: {att.account.username}\nEmail: {att.account.email}\nTicket: {ticket}"
        )

    def delete_account(self):
        """
        Deletes the currently logged-in attendee account.
        """
        self.controller.delete_logged_in_account()
        self.create_login_screen()

    def logout(self):
        """
        Logs out the current user and returns to the login screen.
        """
        self.controller.logged_in = None
        self.create_login_screen()

    # ---------------- PURCHASE ----------------
    def purchase_screen(self):
        """
        Displays all available ticket types and payment input.
        """
        self.clear_frame()
        self.selected_ticket = tk.IntVar()

        for i, t in enumerate(self.controller.ticket_types):
            tk.Radiobutton(
                self.frame,
                text=f"{t.name} | AED {t.price} | Access: {t.exhibitions}",
                variable=self.selected_ticket,
                value=i
            ).pack()

        tk.Label(self.frame, text="Payment Method").pack()
        tk.Entry(self.frame, textvariable=self.payment).pack()

        tk.Button(self.frame, text="Confirm Purchase", command=self.purchase_ticket).pack()
        tk.Button(self.frame, text="Back", command=self.create_dashboard).pack()

    def purchase_ticket(self):
        """
        Confirms ticket purchase and sends the request to controller.
        """
        i = self.selected_ticket.get()
        ticket = self.controller.ticket_types[i]
        self.controller.purchase_ticket(ticket, self.payment.get())
        messagebox.showinfo("Success", "Ticket purchased")
        self.create_dashboard()

    # ---------------- UPGRADE ----------------
    def upgrade_screen(self):
        """
        Displays available ticket upgrades.
        """
        self.clear_frame()
        current_price = self.controller.logged_in.pass_ref.ticket_type.price
        self.upgrade_var = tk.IntVar()

        for i, t in enumerate(self.controller.ticket_types):
            if t.price > current_price:
                tk.Radiobutton(
                    self.frame,
                    text=f"{t.name} | AED {t.price}",
                    variable=self.upgrade_var,
                    value=i
                ).pack()

        tk.Button(self.frame, text="Upgrade", command=self.upgrade_ticket).pack()
        tk.Button(self.frame, text="Back", command=self.create_dashboard).pack()

    def upgrade_ticket(self):
        """
        Upgrades the attendee's current ticket.
        """
        ticket = self.controller.ticket_types[self.upgrade_var.get()]
        self.controller.upgrade_ticket(ticket)
        messagebox.showinfo("Success", "Ticket upgraded")
        self.create_dashboard()

    # ---------------- WORKSHOPS ----------------
    def reserve_screen(self):
        """
        Displays all workshops and allows the user to reserve them.
        """
        self.clear_frame()
        self.work_vars = []

        for w in self.controller.get_all_workshops():
            v = tk.IntVar()
            tk.Checkbutton(
                self.frame,
                text=f"{w.title} | {w.exhibition} | Seats: {w.capacity}",
                variable=v
            ).pack()
            self.work_vars.append((v, w))

        tk.Button(self.frame, text="Reserve", command=self.reserve).pack()
        tk.Button(self.frame, text="Back", command=self.create_dashboard).pack()

    def reserve(self):
        """
        Reserves all selected workshops for the attendee.
        """
        selected = [w for v, w in self.work_vars if v.get()]
        try:
            self.controller.reserve_workshops(selected)
            messagebox.showinfo("Reserved", "Workshops reserved")
            self.create_dashboard()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    # ---------------- ADMIN ----------------
    def admin_login_screen(self):
        """
        Login screen for administrator.
        """
        self.clear_frame()
        tk.Label(self.frame, text="Admin Username").pack()
        tk.Entry(self.frame, textvariable=self.username).pack()

        tk.Label(self.frame, text="Admin Password").pack()
        tk.Entry(self.frame, textvariable=self.password, show="*").pack()

        tk.Button(self.frame, text="Login", command=self.admin_login).pack()

    def admin_login(self):
        """
        Validates admin credentials and opens admin dashboard.
        """
        if self.controller.validate_admin(
            self.username.get(),
            self.password.get()
        ):
            self.admin_dashboard()
        else:
            messagebox.showerror("Error", "Invalid Admin Login")

    def admin_dashboard(self):
        """
        Displays daily ticket sales and revenue for administrators.
        """
        self.clear_frame()
        for r in self.controller.get_sales_reports():
            tk.Label(
                self.frame,
                text=f"{r.date} | Tickets: {r.tickets_sold} | Sales: {r.total_sales}"
            ).pack()
