import pickle                               # Used for saving and loading data persistently
from datetime import date                  # Used to track daily sales report dates
from model.models import *                 # Import all model classes (MVC pattern)

class GreenWaveController:
    """
    This class controls all business logic of the GreenWave system.
    It connects the GUI (View) with the data classes (Model).
    """

    def __init__(self):
        # Load saved system data from pickle files
        self.attendees = self.load_data("attendees.pkl")      # All registered attendees
        self.payments = self.load_data("payments.pkl")        # All payment records
        self.workshops = self.load_data("workshops.pkl")      # All workshops
        self.sales_reports = self.load_data("sales.pkl")     # Daily sales reports

        # Predefined ticket types available in the system
        self.ticket_types = [
            TicketType("Single", 100, ["A"]),                 # Access to Exhibition A only
            TicketType("Double", 150, ["A", "B"]),            # Access to Exhibitions A and B
            TicketType("Full", 200, ["A", "B", "C"])          # Full access to all exhibitions
        ]

        # Stores the currently logged-in user
        self.logged_in = None

        # Create default workshops only if no workshops exist yet
        if not self.workshops:
            self.workshops = [
                Workshop("Solar Energy", "A", 10),            # Workshop in Exhibition A
                Workshop("Electric Vehicles", "B", 10),       # Workshop in Exhibition B
                Workshop("Recycling Tech", "C", 10)           # Workshop in Exhibition C
            ]
            self.save_data("workshops.pkl", self.workshops)  # Save default workshops

    # -------------------------------
    # PICKLE SYSTEM
    # -------------------------------

    def save_data(self, filename, data):
        """
        Saves any Python object to a binary file using pickle.
        """
        with open(filename, "wb") as f:
            pickle.dump(data, f)

    def load_data(self, filename):
        """
        Loads and returns data from a binary pickle file.
        If the file does not exist, an empty list is returned.
        """
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except:
            return []

    # -------------------------------
    # ACCOUNT MANAGEMENT
    # -------------------------------

    def create_account(self, username, password, email):
        """
        Creates a new attendee account.
        Prevents duplicate usernames.
        """
        for a in self.attendees:
            if a.account.username == username:
                raise ValueError("Username already exists")

        acc = Account(username, password, email)      # Create Account object
        self.attendees.append(Attendee(acc))         # Wrap inside Attendee object
        self.save_data("attendees.pkl", self.attendees)

    def login(self, username, password):
        """
        Authenticates user login and sets logged_in attendee.
        """
        for a in self.attendees:
            if a.account.username == username and a.account.password == password:
                self.logged_in = a
                return
        raise ValueError("Invalid login")

    def delete_logged_in_account(self):
        """
        Deletes the currently logged-in user account.
        """
        self.attendees.remove(self.logged_in)
        self.save_data("attendees.pkl", self.attendees)
        self.logged_in = None

    # -------------------------------
    # TICKETS
    # -------------------------------

    def purchase_ticket(self, ticket_type, payment_method):
        """
        Handles ticket purchase process.
        Creates a payment, ticket, and assigns a pass to the attendee.
        """
        payment = Payment(payment_method, ticket_type.price)  # Create payment record
        ticket = Ticket(ticket_type, payment)                 # Create ticket object

        self.logged_in.pass_ref = Pass(ticket)                # Assign pass to user
        self.payments.append(payment)                         # Store payment
        self.save_data("payments.pkl", self.payments)         # Save all payments

        self.update_sales_report(ticket_type.price)           # Update daily sales

    def upgrade_ticket(self, new_ticket_type):
        """
        Upgrades the attendee ticket and only charges the price difference.
        """
        old_price = self.logged_in.pass_ref.ticket_type.price
        diff = new_ticket_type.price - old_price

        self.logged_in.pass_ref.ticket_type = new_ticket_type  # Update ticket type
        self.update_sales_report(diff)                         # Update revenue

    # -------------------------------
    # WORKSHOPS
    # -------------------------------

    def get_all_workshops(self):
        """
        Returns the list of all workshops in the system.
        """
        return self.workshops

    def reserve_workshops(self, selected):
        """
        Reserves selected workshops for the logged-in user.
        Ensures ticket access and capacity limits.
        """
        allowed = self.logged_in.pass_ref.ticket_type.exhibitions

        for w in selected:
            if w.exhibition not in allowed:
                raise ValueError("Workshop not allowed")

            if w.capacity <= 0:
                raise ValueError("Workshop full")

            w.capacity -= 1                                  # Reduce available seats
            self.logged_in.reservations.append(w)            # Save reservation

        self.save_data("workshops.pkl", self.workshops)

    # -------------------------------
    # ADMIN
    # -------------------------------

    def validate_admin(self, u, p):
        """
        Checks if the admin credentials are correct.
        """
        return u == "admin" and p == "admin123"

    def get_sales_reports(self):
        """
        Returns all daily sales reports.
        """
        return self.sales_reports

    def update_sales_report(self, amount):
        """
        Updates today's sales report or creates a new one if it does not exist.
        """
        today = date.today()

        for r in self.sales_reports:
            if r.date == today:
                r.tickets_sold += 1
                r.total_sales += amount
                self.save_data("sales.pkl", self.sales_reports)
                return

        # Create new sales report for today if none exists
        self.sales_reports.append(SalesReport(today, 1, amount))
        self.save_data("sales.pkl", self.sales_reports)
