from tkinter import *
from tkinter import messagebox
from publishers import *
from styles import COLORS, FONTS, styled_popup, styled_scrollable_popup, finalize_scrollable, styled_field, primary_button, danger_button, module_header, shelf_button, open_results_table, empty_result_label


def save_publisher(entries, popup):
    publisher_id = entries["publisher_id"].get()
    publisher_name = entries["publisher_name"].get()
    address = entries["address"].get()
    phone = entries["phone"].get()
    email = entries["email"].get()

    success, message = add_publisher(
        publisher_id,
        publisher_name,
        address,
        phone,
        email
    )

    if success:
        messagebox.showinfo("Publisher Added", message)
        popup.destroy()
    else:
        messagebox.showerror("Could Not Add Publisher", message)


def open_add_publisher_form():
    popup, body, canvas = styled_scrollable_popup(None, "Add New Publisher", 420, 650)
    popup.grab_set()

    fields = [
        ("PUBLISHER_ID", "publisher_id"),
        ("PUBLISHER_NAME", "publisher_name"),
        ("ADDRESS", "address"),
        ("PHONE", "phone"),
        ("EMAIL", "email"),
    ]

    entries = {}

    for label_text, key in fields:
        entries[key] = styled_field(body, label_text)

    primary_button(body, "Save", lambda: save_publisher(entries, popup)).pack(pady=15, fill=X)

    finalize_scrollable(canvas, body)


def read_publisher(entries, popup, results_frame):
    for widget in results_frame.winfo_children():
        widget.destroy()

    publisher_name = entries["publisher_name"].get().strip()

    if not publisher_name:
        empty_result_label(results_frame, "Enter a publisher name to search.").pack(pady=10)
        return

    publishers = get_publisher(publisher_name)

    if publishers is None:
        empty_result_label(results_frame, "Something went wrong while searching. Please try again.").pack(pady=10)
        return

    if not publishers:
        empty_result_label(results_frame, "No publisher found.").pack(pady=10)
        return

    open_results_table(popup, f"Results for '{publisher_name}'", publishers)


def show_publisher_form():
    popup, body = styled_popup(None, "Search Publisher", 380, 220)
    popup.grab_set()

    entry = styled_field(body, "Publisher Name")
    entries = {"publisher_name": entry}

    results_frame = Frame(body, bg=COLORS["card_bg"])
    results_frame.pack(fill=X)

    primary_button(
        body, "Search",
        lambda: read_publisher(entries, popup, results_frame)
    ).pack(pady=15, fill=X)


def remove_publisher(entries, popup):
    publisher_name = entries["publisher_name"].get().strip()

    if not publisher_name:
        messagebox.showerror("Missing Info", "Publisher Name is required.")
        return

    confirm = messagebox.askyesno("Confirm Delete", f"Delete publisher '{publisher_name}'? This cannot be undone.")
    if not confirm:
        return

    success, message = delete_publisher(publisher_name)

    if success:
        messagebox.showinfo("Publisher Deleted", message)
        popup.destroy()
    else:
        messagebox.showerror("Could Not Delete Publisher", message)


def open_delete_publisher_form():
    popup, body = styled_popup(None, "Delete Publisher", 380, 220)
    popup.grab_set()

    entry = styled_field(body, "Publisher Name")
    entries = {"publisher_name": entry}

    danger_button(body, "Delete", lambda: remove_publisher(entries, popup)).pack(pady=15, fill=X)


def make_changes_in_publisher(entries, popup):
    publisher_id = entries["publisher_id"].get().strip()
    publisher_name = entries["publisher_name"].get().strip()

    if not publisher_id:
        messagebox.showerror("Missing Info", "Publisher ID is required.")
        return

    success, message = update_publisher(publisher_id, publisher_name)

    if success:
        messagebox.showinfo("Publisher Updated", message)
        popup.destroy()
    else:
        messagebox.showerror("Could Not Update Publisher", message)


def make_changes_in_publisher_form():
    popup, body = styled_popup(None, "Update Publisher", 380, 300)
    popup.grab_set()

    entries = {}
    entries["publisher_id"] = styled_field(body, "Publisher Id")
    entries["publisher_name"] = styled_field(body, "Publisher Name")

    primary_button(body, "Update", lambda: make_changes_in_publisher(entries, popup)).pack(pady=15, fill=X)


def show_publishers(content_frame):
    shelf_button(content_frame, "Add Publisher", open_add_publisher_form, relx=0.25, rely=0.23)
    shelf_button(content_frame, "Search Publisher", show_publisher_form, relx=0.75, rely=0.23)
    shelf_button(content_frame, "Update Publisher", make_changes_in_publisher_form, relx=0.25, rely=0.60)
    shelf_button(content_frame, "Delete Publisher", open_delete_publisher_form, relx=0.75, rely=0.60, danger=True)