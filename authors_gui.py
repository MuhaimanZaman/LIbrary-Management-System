from tkinter import *
from tkinter import messagebox
from authors import *
from styles import COLORS, FONTS, styled_popup, styled_scrollable_popup, finalize_scrollable, styled_field, primary_button, danger_button, module_header, shelf_button, open_results_table, empty_result_label


def save_author(entries, popup):
    author_id = entries["author_id"].get()
    author_name = entries["author_name"].get()
    country = entries["country"].get()
    birth_date = entries["birth_date"].get()

    success, message = add_author(
        author_id,
        author_name,
        country,
        birth_date,
    )

    if success:
        messagebox.showinfo("Author Added", message)
        popup.destroy()
    else:
        messagebox.showerror("Could Not Add Author", message)


def open_add_author_form():
    popup, body, canvas = styled_scrollable_popup(None, "Add New Author", 420, 650)
    popup.grab_set()

    fields = [
        ("AUTHOR_ID", "author_id"),
        ("AUTHOR_NAME", "author_name"),
        ("COUNTRY", "country"),
        ("BIRTH_DATE", "birth_date")
    ]

    entries = {}

    for label_text, key in fields:
        entries[key] = styled_field(body, label_text)

    primary_button(body, "Save", lambda: save_author(entries, popup)).pack(pady=15, fill=X)

    finalize_scrollable(canvas, body)


def read_author(entries, popup, results_frame):
    for widget in results_frame.winfo_children():
        widget.destroy()

    author_name = entries["author_name"].get().strip()

    if not author_name:
        empty_result_label(results_frame, "Enter an author name to search.").pack(pady=10)
        return

    authors = get_author(author_name)

    if authors is None:
        empty_result_label(results_frame, "Something went wrong while searching. Please try again.").pack(pady=10)
        return

    if not authors:
        empty_result_label(results_frame, "No author found.").pack(pady=10)
        return

    open_results_table(popup, f"Results for '{author_name}'", authors)


def show_author_form():
    popup, body = styled_popup(None, "Search Author", 380, 220)
    popup.grab_set()

    entry = styled_field(body, "Author Name")
    entries = {"author_name": entry}

    results_frame = Frame(body, bg=COLORS["card_bg"])
    results_frame.pack(fill=X)

    primary_button(
        body, "Search",
        lambda: read_author(entries, popup, results_frame)
    ).pack(pady=15, fill=X)


def remove_author(entries, popup):
    author_name = entries["author_name"].get().strip()

    if not author_name:
        messagebox.showerror("Missing Info", "Author Name is required.")
        return

    confirm = messagebox.askyesno("Confirm Delete", f"Delete author '{author_name}'? This cannot be undone.")
    if not confirm:
        return

    success, message = delete_author(author_name)

    if success:
        messagebox.showinfo("Author Deleted", message)
        popup.destroy()
    else:
        messagebox.showerror("Could Not Delete Author", message)


def open_delete_author_form():
    popup, body = styled_popup(None, "Delete Author", 380, 220)
    popup.grab_set()

    entry = styled_field(body, "Author Name")
    entries = {"author_name": entry}

    danger_button(body, "Delete", lambda: remove_author(entries, popup)).pack(pady=15, fill=X)


def make_changes_in_author(entries, popup):
    author_id = entries["author_id"].get().strip()
    author_name = entries["author_name"].get().strip()

    if not author_id:
        messagebox.showerror("Missing Info", "Author ID is required.")
        return

    success, message = update_author(author_id, author_name)

    if success:
        messagebox.showinfo("Author Updated", message)
        popup.destroy()
    else:
        messagebox.showerror("Could Not Update Author", message)


def make_changes_in_author_form():
    popup, body = styled_popup(None, "Update Author", 380, 300)
    popup.grab_set()

    entries = {}
    entries["author_id"] = styled_field(body, "Author ID")
    entries["author_name"] = styled_field(body, "Author Name")

    primary_button(body, "Update", lambda: make_changes_in_author(entries, popup)).pack(pady=15, fill=X)


def show_authors(content_frame):
    shelf_button(content_frame, "Add Author", open_add_author_form, relx=0.25, rely=0.23)
    shelf_button(content_frame, "Search Author", show_author_form, relx=0.75, rely=0.23)
    shelf_button(content_frame, "Update Author", make_changes_in_author_form, relx=0.25, rely=0.60)
    shelf_button(content_frame, "Delete Author", open_delete_author_form, relx=0.75, rely=0.60, danger=True)