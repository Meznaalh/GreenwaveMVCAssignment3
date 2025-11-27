import pickle

# ---------------------------
# Composition: Account is part of Attendee (Attendee cannot exist without it)
# ---------------------------

class Account:
    def __init__(self, username, password, email):
        self.username = username  # string: login name
        self.password = password  # string: password
        self.email = email        # string: email address


# ---------------------------
# Aggregation: Pass is separate from Attendee (can exist independently)
# ---------------------------

class Pass:
    def __init__(self, pass_id, access_level):
        self.pass_id = pass_id               # string: unique ID
        self.access_level = access_level     # list of exhibitions this pass allows
        self.reserved_workshops = []         # list of Workshop objects

    def reserve_workshop(self, workshop):
        if workshop.capacity > 0:
            self.reserved_workshops.append(workshop)
            workshop.capacity -= 1
        else:
            raise Exception("Workshop is full.")


# ---------------------------
# Attendee has Account (composition) and optional Pass (aggregation)
# ---------------------------

class Attendee:
    def __init__(self, account):
        self.account = account          # composition: Account object
        self.attendee_pass = None       # aggregation: Pass object (optional)
        self.tickets = []               # list of Ticket objects
        self.reservations = []          # list of Workshop objects

    def assign_pass(self, attendee_pass):
        self.attendee_pass = attendee_pass

    def reserve_workshop(self, workshop):
        if self.attendee_pass is None:
            raise Exception("No pass assigned.")
        if workshop.exhibition not in self.attendee_pass.access_level:
            raise Exception("Pass does not allow access to this workshop's exhibition.")
        self.attendee_pass.reserve_workshop(workshop)
        self.reservations.append(workshop)


# ---------------------------
# Ticket Types (Single, Double, Full)
# ---------------------------

class TicketType:
    def __init__(self, name, price, access_scope):
        self.name = name                      # string: type name
        self.price = price                    # float: ticket price
        self.access_scope = access_scope      # list: allowed exhibitions


# ---------------------------
# Tickets (purchased by attendee)
# ---------------------------

class Ticket:
    def __init__(self, ticket_type, purchase_date):
        self.ticket_type = ticket_type        # TicketType object
        self.purchase_date = purchase_date    # string: when ticket was bought


# ---------------------------
# Workshops (events to reserve)
# ---------------------------

class Workshop:
    def __init__(self, title, exhibition, capacity):
        self.title = title              # string: workshop name
        self.exhibition = exhibition    # string: which exhibition it belongs to (e.g., 'A', 'B', 'C')
        self.capacity = capacity        # int: number of available seats


# ---------------------------
# Admin (inherits from User base class)
# ---------------------------

class User:
    def __init__(self, user_id, username, email, password):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password


class Administrator(User):
    def __init__(self, user_id, username, email, password):
        super().__init__(user_id, username, email, password)
        self.sales_reports = []  # list of SalesReport objects

    def add_sales_report(self, report):
        self.sales_reports.append(report)


# ---------------------------
# SalesReport (monitors performance)
# ---------------------------

class SalesReport:
    def __init__(self, date, total_sales, tickets_sold):
        self.date = date                  # string: 'YYYY-MM-DD'
        self.total_sales = total_sales    # float: total AED
        self.tickets_sold = tickets_sold  # int: number of tickets


# ---------------------------
# Payment class (basic representation)
# ---------------------------

class Payment:
    def __init__(self, method, amount):
        self.method = method              # e.g., 'Credit Card', 'Cash'
        self.amount = amount              # float


# ---------------------------
# Utility functions for Pickle (Persistence)
# ---------------------------

def save_data(filename, data):
    """Save any Python object to binary file"""
    with open(f"data/{filename}", "wb") as file:
        pickle.dump(data, file)


def load_data(filename):
    """Load Python object from binary file"""
    try:
        with open(f"data/{filename}", "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return []  # if file doesn’t exist, return empty list

