import tkinter as tk
from tkinter import messagebox
from controller.controller import GreenWaveController

class GreenWaveGUI:
    def __init__(self, root):
        self.controller = GreenWaveController()
        self.root = root
        self.root.title("GreenWave Conference Ticketing System")
        self.root.geometry("600x500")

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20)

        self.username_entry = tk.Entry(self.frame, width=30)
        self.password_entry = tk.Entry(self.frame, width=30, show="*")
        self.email_entry = tk.Entry(self.frame, width=30)

        self.create_login_screen()

    def create_login_screen(self):
        self.clear_frame()
        tk.Label(self.frame, text="Username").grid(row=0, column=0)
        self.username_entry.grid(row=0, column=1)
        tk.Label(self.frame, text="Password").grid(row=1, column=0)
        self.password_entry.grid(row=1, column=1)

        tk.Button(self.frame, text="Login", command=self.login).grid(row=2, column=0)
        tk.Button(self.frame, text="Register", command=self.create_register_screen).grid(row=2, column=1)
        tk.Button(self.frame, text="Admin Login", command=self.admin_login_screen).grid(row=3, column=0, columnspan=2)

    def create_register_screen(self):
        self.clear_frame()
        tk.Label(self.frame, text="Username").grid(row=0, column=0)
        self.username_entry.grid(row=0, column=1)
        tk.Label(self.frame, text="Password").grid(row=1, column=0)
        self.password_entry.grid(row=1, column=1)
        tk.Label(self.frame, text="Email").grid(row=2, column=0)
        self.email_entry.grid(row=2, column=1)

        tk.Button(self.frame, text="Create Account", command=self.register).grid(row=3, column=0, columnspan=2)
        tk.Button(self.frame, text="Back to Login", command=self.create_login_screen).grid(row=4, column=0, columnspan=2)

    def create_dashboard(self):
        self.clear_frame()
        tk.Label(self.frame, text=f"Welcome, {self.controller.logged_in.account.username}!").grid(row=0, column=0)
        tk.Button(self.frame, text="View Details", command=self.show_details).grid(row=1, column=0)
        tk.Button(self.frame, text="Delete Account", command=self.delete_account).grid(row=2, column=0)
        tk.Button(self.frame, text="Ticket Purchase", command=self.ticket_purchase_screen).grid(row=3, column=0)
        tk.Button(self.frame, text="Upgrade Ticket", command=self.upgrade_ticket_screen).grid(row=4, column=0)
        tk.Button(self.frame, text="Logout", command=self.logout).grid(row=5, column=0)

    def cancel_ticket(self):
        try:
            self.controller.cancel_ticket()
            messagebox.showinfo("Canceled", "Your ticket has been canceled.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))


    def reserve_workshop_screen(self):
        self.clear_frame()
        workshops = self.controller.get_all_workshops()
        ticket_exhibitions = self.controller.logged_in.pass_ref.ticket_type.access_exhibitions


        tk.Label(self.frame, text="Reserve Workshop (based on your ticket access):").pack()
        self.workshop_vars = []
        for w in workshops:
            if w.exhibition in ticket_exhibitions and w.capacity > 0:
                var = tk.IntVar()
                cb = tk.Checkbutton(self.frame, text=f"{w.title} (Exhibition {w.exhibition}) - Seats left: {w.capacity}", variable=var)
                cb.pack(anchor='w')
                self.workshop_vars.append((var, w))


        tk.Button(self.frame, text="Reserve", command=self.reserve_selected_workshops).pack(pady=10)
        tk.Button(self.frame, text="Back", command=self.create_dashboard).pack()

    def reserve_selected_workshops(self):
        selected = [w for var, w in self.workshop_vars if var.get() == 1]
        if not selected:
            messagebox.showwarning("Select", "Please select at least one workshop")
            return
        try:
            self.controller.reserve_workshops(selected)
            messagebox.showinfo("Reserved", "Workshops successfully reserved!")
            self.create_dashboard()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    
    def modify_account_screen(self):
        self.clear_frame()
        tk.Label(self.frame, text="New Email").grid(row=0, column=0)
        new_email_entry = tk.Entry(self.frame)
        new_email_entry.grid(row=0, column=1)


        tk.Label(self.frame, text="New Password").grid(row=1, column=0)
        new_pass_entry = tk.Entry(self.frame, show="*")
        new_pass_entry.grid(row=1, column=1)


    def save_changes():
        new_email = new_email_entry.get()
        new_pass = new_pass_entry.get()
        if new_email:
            self.controller.logged_in.account.email = new_email
            if new_pass:
                self.controller.logged_in.account.password = new_pass
            self.controller.save_attendees()
            messagebox.showinfo("Updated", "Account information updated")
            self.create_dashboard()


        tk.Button(self.frame, text="Save", command=save_changes).grid(row=2, column=0, columnspan=2)
        tk.Button(self.frame, text="Back", command=self.create_dashboard).grid(row=3, column=0, columnspan=2)

    def admin_login_screen(self):
        self.clear_frame()
        tk.Label(self.frame, text="Admin Username").grid(row=0, column=0)
        self.username_entry.grid(row=0, column=1)
        tk.Label(self.frame, text="Admin Password").grid(row=1, column=0)
        self.password_entry.grid(row=1, column=1)

        tk.Button(self.frame, text="Login as Admin", command=self.admin_login).grid(row=2, column=0, columnspan=2)
        tk.Button(self.frame, text="Back", command=self.create_login_screen).grid(row=3, column=0, columnspan=2)

    def admin_dashboard(self):
        self.clear_frame()
        tk.Label(self.frame, text="Admin Dashboard").pack()
        tk.Button(self.frame, text="View Sales Reports", command=self.view_sales).pack(pady=5)
        tk.Button(self.frame, text="View Workshop Attendance", command=self.view_workshop_capacity).pack(pady=5)
        tk.Button(self.frame, text="Back", command=self.create_login_screen).pack(pady=5)

    def view_sales(self):
        reports = self.controller.get_sales_reports()
        if not reports:
            messagebox.showinfo("Sales Report", "No reports available.")
            return
        msg = ""
        for report in reports:
            msg += f"Date: {report.date}\nTickets Sold: {report.tickets_sold}\nTotal Sales: AED {report.total_sales}\n\n"
        messagebox.showinfo("Sales Report", msg)

    def view_workshop_capacity(self):
        workshops = self.controller.get_all_workshops()
        msg = ""
        for w in workshops:
            msg += f"{w.title} (Exhibition {w.exhibition}) - Seats left: {w.capacity}\n"
        messagebox.showinfo("Workshop Attendance", msg)

    def admin_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        try:
            if self.controller.validate_admin(username, password):
                self.admin_dashboard()
            else:
                messagebox.showerror("Error", "Invalid admin credentials")
        except:
            messagebox.showerror("Error", "Error during admin login")

    def ticket_purchase_screen(self):
        self.clear_frame()
        tk.Label(self.frame, text="Choose Ticket Type:").pack()
        self.ticket_vars = []
        for ticket in self.controller.ticket_types:
            var = tk.IntVar()
            cb = tk.Radiobutton(self.frame, text=f"{ticket.name} - AED {ticket.price}", variable=var, value=1)
            cb.pack(anchor='w')
            self.ticket_vars.append((var, ticket))


        tk.Label(self.frame, text="Select Payment Method:").pack()
        self.payment_method = tk.StringVar()
        tk.Radiobutton(self.frame, text="Credit Card", variable=self.payment_method, value="credit").pack(anchor='w')
        tk.Radiobutton(self.frame, text="Debit Card", variable=self.payment_method, value="debit").pack(anchor='w')
        tk.Radiobutton(self.frame, text="Apple Pay", variable=self.payment_method, value="apple").pack(anchor='w')


        tk.Label(self.frame, text="Card Number").pack()
        self.card_entry = tk.Entry(self.frame)
        self.card_entry.pack()


        tk.Button(self.frame, text="Purchase", command=self.purchase_ticket).pack(pady=10)
        tk.Button(self.frame, text="Back", command=self.create_dashboard).pack()

    def purchase_ticket(self):
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
        self.controller.purchase_ticket(chosen_ticket, self.payment_method.get())
         messagebox.showinfo("Success", "Ticket purchased successfully")
         self.create_dashboard()

    def upgrade_ticket_screen(self):
        self.clear_frame()
        if not self.controller.logged_in:
            messagebox.showerror("Error", "Please login first")
            return
        current = self.controller.logged_in.pass_ref.ticket_type
        tk.Label(self.frame, text=f"Current Ticket: {current.name}").pack(pady=10)
        tk.Label(self.frame, text="Select upgrade:").pack()

        self.upgrade_options = []
        for ticket in self.controller.ticket_types:
            if ticket.price > current.price:
                var = tk.IntVar()
                tk.Radiobutton(self.frame, text=f"{ticket.name} - AED {ticket.price}", variable=var, value=1).pack(anchor='w')
                self.upgrade_options.append((var, ticket))

        tk.Button(self.frame, text="Upgrade", command=self.upgrade_ticket).pack(pady=10)
        tk.Button(self.frame, text="Back", command=self.create_dashboard).pack()

    def upgrade_ticket(self):
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
        username = self.username_entry.get()
        password = self.password_entry.get()
        try:
            self.controller.login(username, password)
            self.create_dashboard()
        except ValueError as e:
            messagebox.showerror("Login Failed", str(e))

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        email = self.email_entry.get()
        try:
            self.controller.create_account(username, password, email)
            messagebox.showinfo("Success", "Account created! You may now login.")
            self.create_login_screen()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def show_details(self):
        att = self.controller.logged_in
        ticket = att.pass_ref.ticket_type.name if att.pass_ref else "No Ticket"
        msg = f"Username: {att.account.username}\nEmail: {att.account.email}\nTicket: {ticket}"
        messagebox.showinfo("Your Details", msg)

    def delete_account(self):
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete your account?")
        if confirm:
            self.controller.delete_logged_in_account()
            messagebox.showinfo("Deleted", "Your account has been deleted.")
            self.create_login_screen()

    def logout(self):
        self.controller.logged_in = None
        self.create_login_screen()

    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = GreenWaveGUI(root)
    root.mainloop()


