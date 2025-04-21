import tkinter as tk
from tkinter import messagebox, Listbox, Toplevel
import datetime
import os

class BillingSoftware:
    def __init__(self, root):
        self.root = root
        self.root.title("Billing Software")
        self.root.geometry("600x600")

        self.customer_name = tk.StringVar(value="")
        self.customer_contact = tk.StringVar(value="")
        self.item_name = tk.StringVar(value="")
        self.item_quantity = tk.StringVar(value="")
        self.item_price = tk.StringVar(value="")
        self.item_discount = tk.StringVar(value="")
        self.bill_items = []
        self.bill_id = ""

        if not os.path.exists("bills"):
            os.mkdir("bills")

        self.display_header()
        self.create_customer_frame()
        self.create_item_frame()
        self.create_buttons()

        self.bill_text = tk.Text(self.root, width=50, height=10)
        self.bill_text.pack(pady=10)

        self.root.bind("<Return>", self.move_to_next_field)

    def display_header(self):
        self.header_frame = tk.Frame(self.root)
        self.header_frame.pack(pady=10)
        tk.Label(self.header_frame, text="Billing Software", font=("Arial", 16)).pack()
        self.time_label = tk.Label(self.header_frame, font=("Arial", 12))
        self.time_label.pack()
        self.update_time()

    def update_time(self):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=f"Date & Time: {current_time}")
        self.root.after(1000, self.update_time)

    def create_customer_frame(self):
        customer_frame = tk.LabelFrame(self.root, text="Customer Details", padx=10, pady=10)
        customer_frame.pack(padx=10, pady=10)

        tk.Label(customer_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(customer_frame, textvariable=self.customer_name).grid(row=0, column=1)

        tk.Label(customer_frame, text="Contact:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(customer_frame, textvariable=self.customer_contact).grid(row=1, column=1)

    def create_item_frame(self):
        item_frame = tk.LabelFrame(self.root, text="Item Details", padx=10, pady=10)
        item_frame.pack(padx=10, pady=10)

        tk.Label(item_frame, text="Item Name:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(item_frame, textvariable=self.item_name).grid(row=0, column=1)

        tk.Label(item_frame, text="Quantity:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(item_frame, textvariable=self.item_quantity).grid(row=1, column=1)

        tk.Label(item_frame, text="Price:").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(item_frame, textvariable=self.item_price).grid(row=2, column=1)

        tk.Label(item_frame, text="Discount (%):").grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(item_frame, textvariable=self.item_discount).grid(row=3, column=1)

        tk.Button(item_frame, text="Add Item", command=self.add_item).grid(row=4, columnspan=2, pady=10)

    def create_buttons(self):
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Generate Bill", command=self.generate_bill).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Print Bill", command=self.print_bill).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="View Bills", command=self.view_bills).pack(side=tk.LEFT, padx=10)

    def move_to_next_field(self, event):
        widget = self.root.focus_get()
        widget.tk_focusNext().focus()
        return "break"

    def add_item(self):
        name = self.item_name.get()
        try:
            quantity = int(self.item_quantity.get()) if self.item_quantity.get() else 0
            price = float(self.item_price.get()) if self.item_price.get() else 0.0
            discount = float(self.item_discount.get()) if self.item_discount.get() else 0.0
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for Quantity, Price, and Discount.")
            return

        if name and quantity > 0 and price > 0:
            net_price = price - (price * (discount / 100))
            total_price = net_price * quantity
            self.bill_items.append((name, quantity, price, discount, total_price))
            self.bill_text.insert(tk.END, f"{name} x {quantity} @ {price} - {discount}% = {total_price:.2f}\n")

            self.item_name.set("")
            self.item_quantity.set("")
            self.item_price.set("")
            self.item_discount.set("")
            self.root.focus_get().tk_focusNext().focus()

    def generate_bill(self):
        total = sum(item[4] for item in self.bill_items)
        self.bill_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        bill_content = f"Bill ID: {self.bill_id}\nCustomer: {self.customer_name.get()} ({self.customer_contact.get()})\n"
        bill_content += "\n".join([f"{item[0]} x {item[1]} = {item[4]:.2f}" for item in self.bill_items])
        bill_content += f"\nTotal: {total:.2f}\n"

        with open(f"bills/{self.bill_id}.txt", "w") as file:
            file.write(bill_content)
        
        messagebox.showinfo("Bill Generated", f"Bill saved as {self.bill_id}.txt")
        self.bill_text.delete(1.0, tk.END)
        self.bill_items.clear()

    def print_bill(self):
        if self.bill_id:
            with open(f"bills/{self.bill_id}.txt", "r") as file:
                content = file.read()
            self.bill_text.insert(tk.END, content)
            self.customer_name.set("")
            self.customer_contact.set("")
            self.item_name.set("")
            self.item_quantity.set("")
            self.item_price.set("")
            self.item_discount.set("")
        else:
            messagebox.showwarning("Warning", "No bill generated yet!")

    def view_bills(self):
        view_window = Toplevel(self.root)
        view_window.title("View Bills")

        listbox = Listbox(view_window, width=50)
        listbox.pack(padx=10, pady=10)

        for bill_file in os.listdir("bills"):
            listbox.insert(tk.END, bill_file)

        def show_bill(event):
            selected = listbox.get(listbox.curselection())
            with open(f"bills/{selected}", "r") as file:
                content = file.read()
            messagebox.showinfo("Bill Details", content)

        listbox.bind("<Double-1>", show_bill)

if __name__ == "__main__":
    root = tk.Tk()
    app = BillingSoftware(root)
    root.mainloop()
