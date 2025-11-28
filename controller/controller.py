# controller/controller.py

# Import all model classes from the models file
from model.models import *
import pickle
from datetime import date


class GreenWaveController:
    """
    The controller acts as the central manager of the entire GreenWave system.
    It connects the GUI (View) with the data classes (Model) following MVC.
    """

    def __init__(self):
        """
        Constructor initializes all system data.
        Loads any saved data from pickle files so that the system can
        continue from previous sessions instead of resetting.
        """

        # Load all existing attendees from storage (or empty list)
        self.attendees = self.load_data("attendees.pkl")

        # Load existing tickets from storage
        self.tickets = self.load_data("tickets.pkl")

        # Load existing payments
        self.payments = self.load_data("payments.pkl")

        # Load all workshops created in the system
        self.workshops = self.load_data("workshops.pkl")

        # Predefined ticket types available in the system
        # These represent system-wide ticket rules
        self.ticket_types = [
            TicketType("Single", 100, ["A"]),           # Gives access only to Exhibition A
            TicketType("Double", 150, ["A", "B"]),      # Gives access to A and B
            TicketType("Full", 200, ["A", "B", "C"])    # Full access to all exhibitions
        ]

        # Stores the attendee currently logged in (None = no one logged in)
        self.logged_in = None

        # Stores daily sales reports
        self.sales_reports = []


    # ------------------------------------------------------------
    #                 PICKLE LOAD/SAVE METHODS
    # ------------------------------------------------------------

    def save_data(self, filename, data):
        """
        Saves any Python object to a binary pickle file.
        Used for persistence of attendees, tickets, workshops, etc.
        """
        with open(filename, 'wb') as f:
            pickle.dump(data, f)

    def load_data(self, filename):
        """
        Loads Python objects from a binary pickle file.
        If file doesn't exist or empty, returns an empty list.
        """
        try:
            with open(filename, 'rb') as f:
                return pickle.load(f)
        except (FileNotFoundError, EOFError):
            # Return empty list if no saved data exists yet
            return []


    # ------------------------------------------------------------
    #                     ACCOUNT MANAGEMENT
    # ------------------------------------------------------------

    def create_account(self, username, password, email):
        """
        Creates a new attendee account.
        Checks for duplicate usernames before creating.
        """
        # Check if username already exists
        for att in self.attendees:
            if att.account.username == username:
                raise ValueError("Username already exists")

        # Create new Account and Attendee objects
        new_account = Account(username, password, email)
        new_attendee = Attendee(new_account)

        # Add attendee to list and persist
        self.attendees.append(new_attendee)
        self.save_data("attendees.pkl", self.attendees)

    def login(self, username, password):
        """
        Authenticates a user and stores them as the logged-in attendee.
        """
        for att in self.attendees:
            if att.account.username == username and att.account.password == password:
                self.logged_in = att  # store currently logged user
                return
        raise ValueError("Invalid username or password")

    def delete_account(self, username, password):
        """
        Allows an attendee to delete their entire account.
        """
        for att in self.attendees:
            if att.account.username == username and att.account.password == password:
                self.attendees.remove(att)
                self.save_data("attendees.pkl", self.attendees)
                return
        raise ValueError("Account not found or password mismatch")

    def get_logged_in_attendee(self):
        """Returns currently logged-in attendee object."""
        return self.logged_in

    def logout(self):
        """Logs out the currently authenticated user."""
        self.logged_in = None


    # ------------------------------------------------------------
    #                     TICKET MANAGEMENT
    # ------------------------------------------------------------

    def get_ticket_types(self):
        """Returns the list of all ticket types available."""
        return self.ticket_types

    def purchase_ticket(self, ticket_type):
        """
        Creates a ticket purchase for the logged-in user.
        Includes payment creation + assignment of pass + persistence.
        """

        if not self.logged_in:
            raise ValueError("Not logged in")

        # Create payment object for the ticket
        payment = Payment("card", ticket_type.price)

        # Create the actual ticket object
        new_ticket = Ticket(ticket_type, payment)

        # Store ticket in system
        self.tickets.append(new_ticket)

        # Create a digital pass referencing the ticket
        new_pass = Pass(new_ticket)

        # Assign pass to attendee
        self.logged_in.pass_ref = new_pass

        # Reset reservations because new ticket may change what workshops are allowed
        self.logged_in.reservations = []

        # Store payment
        self.payments.append(payment)

        # Save all affected files
        self.save_data("tickets.pkl", self.tickets)
        self.save_data("attendees.pkl", self.attendees)
        self.save_data("payments.pkl", self.payments)

        # Update revenue reports
        self.update_sales_report(ticket_type.price)

    def cancel_ticket(self):
        """
        Removes attendee’s ticket.
        Note: does NOT delete ticket object from global ticket list.
        """
        if not self.logged_in or not self.logged_in.pass_ref:
            raise ValueError("No ticket to cancel")

        # Remove pass reference only (does not delete history)
        self.logged_in.pass_ref = None
        self.save_data("attendees.pkl", self.attendees)

    def upgrade_ticket(self, new_ticket_type):
        """
        Upgrades a ticket to a higher tier.
        Only the price difference is charged.
        """

        if not self.logged_in:
            raise ValueError("Not logged in")

        current = self.logged_in.pass_ref.ticket_type

        # Must be an actual upgrade
        if new_ticket_type.price <= current.price:
            raise ValueError("Must select a higher tier")

        # Create payment for the price difference only
        payment = Payment("card", new_ticket_type.price - current.price)

        # Track upgrade internally
        new_ticket = Ticket(new_ticket_type, payment)

        # Replace the ticket type inside the existing pass
        self.logged_in.pass_ref.ticket_type = new_ticket_type

        # Record payment
        self.payments.append(payment)

        # Save
        self.save_data("attendees.pkl", self.attendees)
        self.save_data("payments.pkl", self.payments)

        # Update revenue report
        self.update_sales_report(new_ticket_type.price - current.price)


    # ------------------------------------------------------------
    #                     SALES REPORTS
    # ------------------------------------------------------------

    def update_sales_report(self, amount):
        """
        Adds sales revenue to today's sales report.
        Creates a new report if today’s report doesn't exist.
        """

        today = date.today()

        # Check if today's report exists
        for report in self.sales_reports:
           
