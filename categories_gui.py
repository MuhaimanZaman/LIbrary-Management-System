from tkinter import *
from tkinter import messagebox
from categories import *
from styles import COLORS, FONTS, styled_popup, styled_scrollable_popup, finalize_scrollable, styled_field, primary_button, danger_button, module_header, shelf_button, open_results_table, empty_result_label


def save_category(entries, popup):
    category_id = entries["category_id"].get()
    category_name = entries["category_name"].get()
    description = entries["description"].get()

    success, message = add_category(
        category_id,
        category_name,
        description,
    )

    if success:
        messagebox.showinfo("Category Added", message)
        popup.destroy()
    else:
        messagebox.showerror("Could Not Add Category", message)


def open_add_category_form():
    popup, body, canvas = styled_scrollable_popup(None, "Add New Category", 420, 650)
    popup.grab_set()

    fields = [
        ("CATEGORY_ID", "category_id"),
        ("CATEGORY_NAME", "category_name"),
        ("DESCRIPTION", "description"),
    ]

    entries = {}

    for label_text, key in fields:
        entries[key] = styled_field(body, label_text)

    primary_button(body, "Save", lambda: save_category(entries, popup)).pack(pady=15, fill=X)

    finalize_scrollable(canvas, body)


def read_category(entries, popup, results_frame):
    for widget in results_frame.winfo_children():
        widget.destroy()

    category_name = entries["category_name"].get().strip()

    if not category_name:
        empty_result_label(results_frame, "Enter a category Name to search.").pack(pady=10)
        return

    categories = get_category(category_name)

    if categories is None:
        empty_result_label(results_frame, "Something went wrong while searching. Please try again.").pack(pady=10)
        return

    if not categories:
        empty_result_label(results_frame, "No category found.").pack(pady=10)
        return

    open_results_table(popup, f"Category #{category_name}", categories)


def show_category_form():
    popup, body = styled_popup(None, "Search Category", 380, 220)
    popup.grab_set()
    entry = styled_field(body, "Category Name")
    entries = {"category_name": entry}

    results_frame = Frame(body, bg=COLORS["card_bg"])
    results_frame.pack(fill=X)

    primary_button(
        body, "Search",
        lambda: read_category(entries, popup, results_frame)
    ).pack(pady=15, fill=X)


def remove_category(entries, popup):
    category_id = entries["category_id"].get().strip()

    if not category_id:
        messagebox.showerror("Missing Info", "Category Name is required.")
        return

    confirm = messagebox.askyesno("Confirm Delete", f"Delete category #{category_id}? This cannot be undone.")
    if not confirm:
        return

    success, message = delete_category(category_id)

    if success:
        messagebox.showinfo("Category Deleted", message)
        popup.destroy()
    else:
        messagebox.showerror("Could Not Delete Category", message)


def open_delete_category_form():
    popup, body = styled_popup(None, "Delete Category", 380, 220)
    popup.grab_set()
    entry = styled_field(body, "Category ID")
    entries = {"category_id": entry}

    danger_button(body, "Delete", lambda: remove_category(entries, popup)).pack(pady=15, fill=X)


def make_changes_in_category(entries, popup):
    category_id = entries["category_id"].get().strip()
    category_name = entries["category_name"].get().strip()

    if not category_id:
        messagebox.showerror("Missing Info", "Category ID is required.")
        return

    success, message = update_category(category_id, category_name)

    if success:
        messagebox.showinfo("Category Updated", message)
        popup.destroy()
    else:
        messagebox.showerror("Could Not Update Category", message)


def make_changes_in_category_form():
    popup, body = styled_popup(None, "Update Category", 380, 300)
    popup.grab_set()

    entries = {}
    entries["category_id"] = styled_field(body, "Category ID")
    entries["category_name"] = styled_field(body, "Category Name")

    primary_button(body, "Update", lambda: make_changes_in_category(entries, popup)).pack(pady=15, fill=X)


def show_categories(content_frame):
    shelf_button(content_frame, "Add Category", open_add_category_form, relx=0.25, rely=0.23)
    shelf_button(content_frame, "Search Category", show_category_form, relx=0.75, rely=0.23)
    shelf_button(content_frame, "Update Category", make_changes_in_category_form, relx=0.25, rely=0.60)
    shelf_button(content_frame, "Delete Category", open_delete_category_form, relx=0.75, rely=0.60, danger=True)