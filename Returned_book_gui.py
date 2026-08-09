from tkinter import *
from tkinter import messagebox
from Returned_book import return_book
from styles import COLORS, FONTS, styled_popup, styled_field, primary_button, module_header, shelf_button


def process_return(entries, popup):
    transaction_id = entries["transaction_id"].get().strip()
    remarks = entries["remarks"].get().strip()

    if not transaction_id:
        messagebox.showerror("Missing Info", "Transaction ID is required.")
        return

    success, message = return_book(transaction_id, remarks or None)

    if success:
        messagebox.showinfo("Book Returned", message)
        popup.destroy()
    else:
        messagebox.showerror("Cannot Process Return", message)


def open_return_book_form():
    popup, body = styled_popup(None, "Return Book", 380, 350)
    popup.grab_set()

    entries = {
        "transaction_id": styled_field(body, "Transaction ID"),
        "remarks": styled_field(body, "Remarks (optional)"),
    }

    primary_button(
        body, "Return Book",
        lambda: process_return(entries, popup)
    ).pack(pady=20, fill=X)


def show_return(content_frame):
    shelf_button(
        content_frame, "Return Book",
        open_return_book_form, relx=0.5, rely=0.4
    )