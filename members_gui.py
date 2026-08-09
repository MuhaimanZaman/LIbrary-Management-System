from tkinter import *
from tkinter import messagebox
from members import *
from styles import COLORS, FONTS, styled_popup, styled_scrollable_popup, finalize_scrollable, styled_field, primary_button, danger_button, module_header, shelf_button, open_results_table, empty_result_label


def save_members(entries, popup):
    member_id = entries["member_id"].get()
    first_name = entries["first_name"].get()
    last_name = entries["last_name"].get()
    gender = entries["gender"].get()
    date_of_birth = entries["date_of_birth"].get()
    phone = entries["phone"].get()
    email = entries["email"].get()
    address = entries["address"].get()
    membership_date = entries["membership_date"].get()
    membership_status = entries["membership_status"].get()

    success, message = add_member(
        member_id,
        first_name,
        last_name,
        gender,
        date_of_birth,
        phone,
        email,
        address,
        membership_date,
        membership_status
    )

    if success:
        messagebox.showinfo("Member Added", message)
        popup.destroy()
    else:
        messagebox.showerror("Could Not Add Member", message)


def open_add_members_form():
    popup, body, canvas = styled_scrollable_popup(None, "Add New Member", 420, 650)
    popup.grab_set()

    fields = [
        ("MEMBER_ID", "member_id"),
        ("FIRST_NAME", "first_name"),
        ("LAST_NAME", "last_name"),
        ("GENDER", "gender"),
        ("DATE_OF_BIRTH", "date_of_birth"),
        ("PHONE", "phone"),
        ("EMAIL", "email"),
        ("ADDRESS", "address"),
        ("MEMBERSHIP_DATE", "membership_date"),
        ("MEMBERSHIP_STATUS", "membership_status")
    ]

    entries = {}

    for label_text, key in fields:
        entries[key] = styled_field(body, label_text)

    primary_button(body, "Save", lambda: save_members(entries, popup)).pack(pady=15, fill=X)

    finalize_scrollable(canvas, body)


def read_member(entries, popup, results_frame):
    for widget in results_frame.winfo_children():
        widget.destroy()

    member_id = entries["member_id"].get().strip()
    first_name = entries["first_name"].get().strip()
    last_name = entries["last_name"].get().strip()

    if not member_id and not first_name and not last_name:
        empty_result_label(results_frame, "Enter an ID or a name to search.").pack(pady=10)
        return

    members = get_member(
        member_id=member_id or None,
        first_name=first_name or None,
        last_name=last_name or None
    )

    if members is None:
        empty_result_label(results_frame, "Something went wrong while searching. Please try again.").pack(pady=10)
        return

    if not members:
        empty_result_label(results_frame, "No member found.").pack(pady=10)
        return

    label = member_id or f"{first_name} {last_name}".strip()
    open_results_table(popup, f"Results for '{label}'", members)


def show_member_form():
    popup, body = styled_popup(None, "Search Member", 380, 380)
    popup.grab_set()

    id_entry = styled_field(body, "Member ID (optional)")
    first_entry = styled_field(body, "First Name (optional)")
    last_entry = styled_field(body, "Last Name (optional)")
    entries = {"member_id": id_entry, "first_name": first_entry, "last_name": last_entry}

    results_frame = Frame(body, bg=COLORS["card_bg"])
    results_frame.pack(fill=X)

    primary_button(
        body, "Search",
        lambda: read_member(entries, popup, results_frame)
    ).pack(pady=15, fill=X)


def remove_member(entries, popup):
    member_id = entries["member_id"].get().strip()

    if not member_id:
        messagebox.showerror("Missing Info", "Member ID is required.")
        return

    confirm = messagebox.askyesno("Confirm Delete", f"Delete member #{member_id}? This cannot be undone.")
    if not confirm:
        return

    success, message = delete_member(member_id)

    if success:
        messagebox.showinfo("Member Deleted", message)
        popup.destroy()
    else:
        messagebox.showerror("Could Not Delete Member", message)


def open_delete_member_form():
    popup, body = styled_popup(None, "Delete Member", 380, 220)
    popup.grab_set()

    entry = styled_field(body, "Member ID")
    entries = {"member_id": entry}

    danger_button(body, "Delete", lambda: remove_member(entries, popup)).pack(pady=15, fill=X)


def make_changes_in_member(entries, popup):
    member_id = entries["member_id"].get().strip()
    first_name = entries["first_name"].get().strip()

    if not member_id:
        messagebox.showerror("Missing Info", "Member ID is required.")
        return

    success, message = update_members(member_id, first_name)

    if success:
        messagebox.showinfo("Member Updated", message)
        popup.destroy()
    else:
        messagebox.showerror("Could Not Update Member", message)


def make_changes_in_member_form():
    popup, body = styled_popup(None, "Update Member", 380, 300)
    popup.grab_set()

    entries = {}
    entries["member_id"] = styled_field(body, "Member ID")
    entries["first_name"] = styled_field(body, "First Name")

    primary_button(body, "Update", lambda: make_changes_in_member(entries, popup)).pack(pady=15, fill=X)


def show_members(content_frame):
    shelf_button(content_frame, "Add Member", open_add_members_form, relx=0.25, rely=0.23)
    shelf_button(content_frame, "Search Member", show_member_form, relx=0.75, rely=0.23)
    shelf_button(content_frame, "Update Member", make_changes_in_member_form, relx=0.25, rely=0.60)
    shelf_button(content_frame, "Delete Member", open_delete_member_form, relx=0.75, rely=0.60, danger=True)