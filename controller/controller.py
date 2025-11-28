# controller/controller.py
from model.models import *
import pickle
from datetime import date

class GreenWaveController:
    def __init__(self):
        self.attendees = self.load_data("attendees.pkl")
        self.tickets = self.load_data("tickets.pkl")
        self.payments = self.load_data("payments.pkl")
        self.workshops = self.load_data("workshops.pkl")
        self.ticket_types = [
            TicketType("Single", 100, ["A"]),
            TicketType("Double", 150, ["A", "B"]),
            TicketType("Full", 200, ["A", "B", "C"])
        ]
        self.logged_in = None
        self.sales_reports = []

    def save_data(self, filename, data):
        with open(filename, 'wb') as f:
            pickle.dump(data, f)

    def load_data(self, filename):
        try:
            with open(filename, 'rb') as f:
                return pickle.load(f)
        except (FileNotFoundError, EOFError):
            return []

    def create_account(self, username, password, email):
        for att in self.attendees:
            if att.account.username == username:
                raise ValueError("Username already exists")
        new_account = Account(username, password, email)
        new_attendee = Attendee(new_account)
        self.attendees.append(new_attendee)
        self.save_data("attendees.pkl", self.attendees)

    def login(self, username, password):
        for att in self.attendees:
            if att.account.username == username and att.account.password == password:
                self.logged_in = att
                return
        raise ValueError("Invalid username or password")

    def delete_account(self, username, password):
        for att in self.attendees:
            if att.account.username == username and att.account.password == password:
                self.attendees.remove(att)
                self.save_data("attendees.pkl", self.attendees)
                return
        raise ValueError("Account not found or password mismatch")

    def get_logged_in_attendee(self):
        return self.logged_in

    def logout(self):
        self.logged_in = None

    def get_ticket_types(self):
        return self.ticket_types

    def purchase_ticket(self, ticket_type):
        if not self.logged_in:
            raise ValueError("Not logged in")
        payment = Payment("card", ticket_type.price)
        new_ticket = Ticket(ticket_type, payment)
        self.tickets.append(new_ticket)
        new_pass = Pass(new_ticket)
        self.logged_in.pass_ref = new_pass
        self.logged_in.reservations = []
        self.payments.append(payment)
        self.save_data("tickets.pkl", self.tickets)
        self.save_data("attendees.pkl", self.attendees)
        self.save_data("payments.pkl", self.payments)
        self.update_sales_report(ticket_type.price)

    def cancel_ticket(self):
        if not self.logged_in or not self.logged_in.pass_ref:
            raise ValueError("No ticket to cancel")
        ticket = self.logged_in.pass_ref.ticket_type
        self.logged_in.pass_ref = None
        self.save_data("attendees.pkl", self.attendees)

    def upgrade_ticket(self, new_ticket_type):
        if not self.logged_in:
            raise ValueError("Not logged in")
        current = self.logged_in.pass_ref.ticket_type
        if new_ticket_type.price <= current.price:
            raise ValueError("Must select a higher tier")
        payment = Payment("card", new_ticket_type.price - current.price)
        new_ticket = Ticket(new_ticket_type, payment)
        self.logged_in.pass_ref.ticket_type = new_ticket_type
        self.payments.append(payment)
        self.save_data("attendees.pkl", self.attendees)
        self.save_data("payments.pkl", self.payments)
        self.update_sales_report(new_ticket_type.price - current.price)

    def update_sales_report(self, amount):
        today = date.today()
        for report in self.sales_reports:
            if report.date == today:
                report.tickets_sold += 1
                report.total_sales += amount
                return
        self.sales_reports.append(SalesReport(today, 1, amount))

    def get_sales_reports(self):
        return self.sales_reports

    def validate_admin(self, username, password):
        return username == "admin" and password == "admin123"

    def get_all_workshops(self):
        return self.workshops

    def reserve_workshop(self, workshop_title):
        if not self.logged_in or not self.logged_in.pass_ref:
            raise ValueError("You must have a ticket")
        for workshop in self.workshops:
            if workshop.title == workshop_title:
                if workshop.exhibition not in self.logged_in.pass_ref.ticket_type.exhibitions:
                    raise ValueError("Not included in your ticket")
                if workshop.capacity <= 0:
                    raise ValueError("Workshop full")
                workshop.capacity -= 1
                reservation = Reservation(workshop_title)
                self.logged_in.reservations.append(reservation)
                self.save_data("workshops.pkl", self.workshops)
                self.save_data("attendees.pkl", self.attendees)
                return
        raise ValueError("Workshop not found")

    def modify_email_password(self, new_email, new_password):
        if not self.logged_in:
            raise ValueError("Not logged in")
        self.logged_in.account.email = new_email
        self.logged_in.account.password = new_password
        self.save_data("attendees.pkl", self.attendees)

    def get_attendee_reservations(self):
        if self.logged_in:
            return self.logged_in.reservations
        return []
