from tkinter import *
from tkinter import messagebox
from Reports import (
    get_currently_borrowed, get_overdue_books, get_most_borrowed,
    get_books_by_category, get_library_statistics,
    get_outstanding_fines, get_member_history
)
from styles import COLORS, FONTS, styled_popup, styled_field, primary_button, module_header, shelf_button, open_results_table


def show_currently_borrowed():
    data = get_currently_borrowed()
    if not data:
        messagebox.showinfo("Currently Borrowed", "No books are currently borrowed.")
        return
    open_results_table(None, "Currently Borrowed", data)


def show_overdue_books():
    data = get_overdue_books()
    if not data:
        messagebox.showinfo("Overdue Books", "No overdue books right now.")
        return
    open_results_table(None, "Overdue Books", data)


def show_most_borrowed():
    data = get_most_borrowed(limit=10)
    if not data:
        messagebox.showinfo("Most Borrowed", "No borrow history yet.")
        return
    open_results_table(None, "Most Borrowed (Top 10)", data)


def show_books_by_category():
    data = get_books_by_category()
    if not data:
        messagebox.showinfo("Books By Category", "No categories found.")
        return
    open_results_table(None, "Books By Category", data)


def show_library_statistics():
    data = get_library_statistics()
    if not data:
        messagebox.showinfo("Library Statistics", "Could not load statistics.")
        return
    open_results_table(None, "Library Statistics", data)


def show_outstanding_fines():
    data = get_outstanding_fines()
    if not data:
        messagebox.showinfo("Outstanding Fines", "No unpaid fines right now.")
        return
    open_results_table(None, "Outstanding Fines", data)


def open_member_history_form():
    popup, body = styled_popup(None, "Member History", 380, 220)
    popup.grab_set()

    entry = styled_field(body, "Member ID")
    entries = {"member_id": entry}

    def run_lookup():
        member_id = entries["member_id"].get().strip()
        if not member_id:
            messagebox.showerror("Missing Info", "Member ID is required.")
            return

        data = get_member_history(member_id)
        if not data:
            messagebox.showinfo("Member History", "No borrow history found for this member.")
            return

        open_results_table(popup, f"History for Member #{member_id}", data)

    primary_button(body, "View History", run_lookup).pack(pady=15, fill=X)


def show_reports(content_frame):
    shelf_button(content_frame, "Currently Borrowed", show_currently_borrowed, relx=0.25, rely=0.18)
    shelf_button(content_frame, "Overdue Books", show_overdue_books, relx=0.75, rely=0.18, danger=True)
    shelf_button(content_frame, "Most Borrowed", show_most_borrowed, relx=0.25, rely=0.38)
    shelf_button(content_frame, "Books By Category", show_books_by_category, relx=0.75, rely=0.38)
    shelf_button(content_frame, "Library Statistics", show_library_statistics, relx=0.25, rely=0.58)
    shelf_button(content_frame, "Outstanding Fines", show_outstanding_fines, relx=0.75, rely=0.58, danger=True)
    shelf_button(content_frame, "Member History", open_member_history_form, relx=0.5, rely=0.78)