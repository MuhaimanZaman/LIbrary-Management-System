from tkinter import *
from tkinter import messagebox
from books import *
from styles import COLORS, FONTS, styled_popup, styled_scrollable_popup, finalize_scrollable, styled_field, primary_button, danger_button, module_header, shelf_button, open_results_table, empty_result_label


def save_book(entries, popup):
    book_id = entries["book_id"].get()
    title = entries["title"].get()
    author_id = entries["author_id"].get()
    publisher_id = entries["publisher_id"].get()
    category_id = entries["category_id"].get()
    isbn = entries["isbn"].get()
    year = entries["year"].get()
    edition = entries["edition"].get()
    language = entries["language"].get()
    total_copies = entries["total_copies"].get()
    available_copies = entries["available_copies"].get()
    shelf_location = entries["shelf_location"].get()
    price = entries["price"].get()
    date_added = entries["date_added"].get()

    success, message = add_books(
        book_id,
        title,
        author_id,
        publisher_id,
        category_id,
        isbn,
        year,
        edition,
        language,
        total_copies,
        available_copies,
        shelf_location,
        price,
        date_added
    )

    if success:
        messagebox.showinfo("Book Added", message)
        popup.destroy()
    else:
        messagebox.showerror("Could Not Add Book", message)


def open_add_book_form():
    popup, body, canvas = styled_scrollable_popup(None, "Add New Book", 420, 600)
    popup.grab_set()

    fields = [
        ("Book ID", "book_id"),
        ("Title", "title"),
        ("Author ID", "author_id"),
        ("Publisher ID", "publisher_id"),
        ("Category ID", "category_id"),
        ("ISBN", "isbn"),
        ("Year", "year"),
        ("Edition", "edition"),
        ("Language", "language"),
        ("Total Copies", "total_copies"),
        ("Available Copies", "available_copies"),
        ("Shelf Location", "shelf_location"),
        ("Price", "price"),
        ("Date Added", "date_added"),
    ]

    entries = {}

    for label_text, key in fields:
        entries[key] = styled_field(body, label_text)

    primary_button(body, "Save", lambda: save_book(entries, popup)).pack(pady=15, fill=X)

    finalize_scrollable(canvas, body)


def read_book(entries, popup, results_frame):
    for widget in results_frame.winfo_children():
        widget.destroy()

    book_id = entries["book_id"].get().strip()
    title = entries["title"].get().strip()

    if not book_id and not title:
        empty_result_label(results_frame, "Enter an ID or a title to search.").pack(pady=10)
        return

    books = get_books(book_id=book_id or None, title=title or None)

    if books is None:
        empty_result_label(results_frame, "Something went wrong while searching. Please try again.").pack(pady=10)
        return

    if not books:
        empty_result_label(results_frame, "No book found.").pack(pady=10)
        return

    label = book_id if book_id else title
    open_results_table(popup, f"Results for '{label}'", books)


def show_book_form():
    popup, body = styled_popup(None, "Search Book", 380, 300)
    popup.grab_set()

    id_entry = styled_field(body, "Book ID (optional)")
    title_entry = styled_field(body, "Title (optional)")
    entries = {"book_id": id_entry, "title": title_entry}

    results_frame = Frame(body, bg=COLORS["card_bg"])
    results_frame.pack(fill=X)

    primary_button(
        body, "Search",
        lambda: read_book(entries, popup, results_frame)
    ).pack(pady=15, fill=X)


def remove_books(entries, popup):
    book_id = entries["book_id"].get().strip()

    if not book_id:
        messagebox.showerror("Missing Info", "Book ID is required.")
        return

    confirm = messagebox.askyesno("Confirm Delete", f"Delete book #{book_id}? This cannot be undone.")
    if not confirm:
        return

    success, message = delete_book(book_id)

    if success:
        messagebox.showinfo("Book Deleted", message)
        popup.destroy()
    else:
        messagebox.showerror("Could Not Delete Book", message)


def open_delete_book_form():
    popup, body = styled_popup(None, "Delete Book", 380, 220)
    popup.grab_set()

    entry = styled_field(body, "Book ID")
    entries = {"book_id": entry}

    danger_button(body, "Delete", lambda: remove_books(entries, popup)).pack(pady=15, fill=X)


def make_changes_in_books(entries, popup):
    book_id = entries["book_id"].get().strip()
    title = entries["title"].get().strip()

    if not book_id:
        messagebox.showerror("Missing Info", "Book ID is required.")
        return

    success, message = update_book(book_id, title)

    if success:
        messagebox.showinfo("Book Updated", message)
        popup.destroy()
    else:
        messagebox.showerror("Could Not Update Book", message)


def make_changes_in_book_form():
    popup, body = styled_popup(None, "Update Book", 380, 300)
    popup.grab_set()

    entries = {}
    entries["book_id"] = styled_field(body, "Book ID")
    entries["title"] = styled_field(body, "Title")

    primary_button(body, "Update", lambda: make_changes_in_books(entries, popup)).pack(pady=15, fill=X)


def show_books(content_frame):
    shelf_button(content_frame, "Add Book", open_add_book_form, relx=0.25, rely=0.23)
    shelf_button(content_frame, "Search Book", show_book_form, relx=0.75, rely=0.23)
    shelf_button(content_frame, "Update Book", make_changes_in_book_form, relx=0.25, rely=0.60)
    shelf_button(content_frame, "Delete Book", open_delete_book_form, relx=0.75, rely=0.60, danger=True)