# -------------------------------
# MODEL LAYER
# Contains all UML classes
# These classes represent the core data structure of the system
# -------------------------------

class Account:
    """
    Account class stores login credentials and personal details
    for each attendee in the system.
    """

    def __init__(self, username, password, email):
        self.username = username      # Stores the user's login username
        self.password = password      # Stores the user's login password
        self.email = email            # Stores the user's email address


class TicketType:
    """
    TicketType defines the rules of a ticket such as price
    and which exhibitions it grants access to.
    """

    def __init__(self, name, price, exhibitions):
        self.name = name              # Name of the ticket (Single, Double, Full)
        self.price = price            # Ticket price in AED
        self.exhibitions = exhibitions  # List of exhibitions allowed (e.g., ["A", "B"])


class Payment:
    """
    Payment class stores details of how a ticket was paid for.
    """

    def __init__(self, method, amount):
        self.method = method          # Payment method (credit, debit, etc.)
        self.amount = amount          # Amount paid in AED


class Ticket:
    """
    Ticket class represents a purchased ticket created after payment.
    It links a TicketType with its Payment.
    """

    def __init__(self, ticket_type, payment):
        self.ticket_type = ticket_type   # The type of ticket purchased
        self.payment = payment           # The payment record for this ticket


class Pass:
    """
    Pass class is issued to an attendee after buying a ticket.
    It grants access to workshops based on the ticket type.
    """

    def __init__(self, ticket):
        self.ticket_type = ticket.ticket_type  # TicketType linked to this pass
        self.ticket = ticket                   # Reference to the original ticket


class Workshop:
    """
    Workshop class represents a single workshop event
    belonging to an exhibition.
    """

    def __init__(self, title, exhibition, capacity):
        self.title = title              # Name of the workshop
        self.exhibition = exhibition   # Exhibition it belongs to (A, B, or C)
        self.capacity = capacity       # Number of available seats


class Attendee:
    """
    Attendee class represents a registered conference user.
    Each attendee has one Account, may have one Pass,
    and can make workshop reservations.
    """

    def __init__(self, account):
        self.account = account         # Composition: Attendee owns an Account
        self.pass_ref = None           # Reference to the purchased Pass (if any)
        self.reservations = []         # List of reserved Workshop objects


class SalesReport:
    """
    SalesReport stores daily ticket sales statistics
    for the administrator.
    """

    def __init__(self, date, tickets_sold, total_sales):
        self.date = date               # Date of the sales report
        self.tickets_sold = tickets_sold  # Number of tickets sold on that date
        self.total_sales = total_sales    # Total revenue collected on that date
