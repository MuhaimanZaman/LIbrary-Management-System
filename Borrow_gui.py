from tkinter import *
from tkinter import messagebox
from Borrow import add_borrow_transaction
from styles import COLORS, FONTS, styled_popup, styled_field, primary_button, module_header, shelf_button


def issue_book(entries, popup):
    transaction_id = entries["transaction_id"].get().strip()
    book_id = entries["book_id"].get().strip()
    member_id = entries["member_id"].get().strip()
    employee_id = entries["employee_id"].get().strip()

    if not all([transaction_id, book_id, member_id, employee_id]):
        messagebox.showerror("Missing Info", "All fields are required.")
        return

    success, message = add_borrow_transaction(transaction_id, book_id, member_id, employee_id)

    if success:
        messagebox.showinfo("Book Issued", message)
        popup.destroy()
    else:
        messagebox.showerror("Cannot Issue Book", message)


def open_issue_book_form():
    popup, body = styled_popup(None, "Issue / Borrow Book", 400, 600)
    popup.grab_set()

    entries = {
        "transaction_id": styled_field(body, "Transaction ID"),
        "book_id": styled_field(body, "Book ID"),
        "member_id": styled_field(body, "Member ID"),
        "employee_id": styled_field(body, "Employee ID"),
    }

    primary_button(
        body, "Issue Book",
        lambda: issue_book(entries, popup)
    ).pack(pady=20, fill=X)


def show_borrow(content_frame):
    shelf_button(
        content_frame, "Issue Book",
        open_issue_book_form, relx=0.5, rely=0.4
    )