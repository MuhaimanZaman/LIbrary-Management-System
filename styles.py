from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import sys
import os


def resource_path(relative_path):
   
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


COLORS = {
    "sidebar_bg": "#1E1E1E",
    "image_backdrop": "#36454F",  
    "sidebar_btn": "#1E1E1E",
    "sidebar_btn_hover": "#2E2E2E",
    "sidebar_btn_active": "#2E86AB",
    "content_bg": "#F5F7FA",
    "card_bg": "#FFFFFF",
    "text_dark": "#1E1E1E",
    "text_light": "#FFFFFF",
    "text_muted": "#6B7280",
    "accent": "#2E86AB",
    "accent_hover": "#256A8A",
    "danger": "#E74C3C",
    "danger_hover": "#C0392B",
    "border": "#D0D5DD",
    "input_bg": "#FFFFFF",
}

FONTS = {
    "heading": ("Segoe UI", 20, "bold"),
    "subheading": ("Segoe UI", 13, "bold"),
    "label": ("Segoe UI", 10),
    "entry": ("Segoe UI", 10),
    "button": ("Segoe UI", 10, "bold"),
    "sidebar_button": ("Segoe UI", 11),
}



def make_sidebar_button(parent, text, command):
    btn = Button(
        parent,
        text=text,
        font=FONTS["sidebar_button"],
        bg=COLORS["sidebar_btn"],
        fg=COLORS["text_light"],
        activebackground=COLORS["sidebar_btn_active"],
        activeforeground=COLORS["text_light"],
        bd=0,
        relief=FLAT,
        anchor="w",
        padx=25,
        pady=12,
        width=18,
        cursor="hand2",
        command=command
    )

    def on_enter(e):
        if btn["bg"] != COLORS["sidebar_btn_active"]:
            btn.config(bg=COLORS["sidebar_btn_hover"])

    def on_leave(e):
        if btn["bg"] != COLORS["sidebar_btn_active"]:
            btn.config(bg=COLORS["sidebar_btn"])

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn


def set_active_sidebar_button(all_buttons, active_btn):
    for b in all_buttons:
        b.config(bg=COLORS["sidebar_btn"])
    active_btn.config(bg=COLORS["sidebar_btn_active"])


def styled_popup(parent, title, width, height):
    popup = Toplevel(parent)
    popup.title(title)
    popup.geometry(f"{width}x{height}")
    popup.resizable(False, False)

    bg_image = Image.open(resource_path("library.png")).resize((width, height))
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = Label(popup, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    Label(
        popup,
        text=title,
        font=FONTS["subheading"],
        bg=SHELF_COLORS["bg"],
        fg=SHELF_COLORS["text"],
        padx=15,
        pady=6
    ).place(relx=0.5, rely=0.05, anchor="n")

    body = Frame(popup, bg=COLORS["card_bg"])
    body.place(relx=0.5, rely=0.28, anchor="n", width=int(width * 0.75))

    return popup, body


def styled_scrollable_popup(parent, title, width, height):
    popup = Toplevel(parent)
    popup.title(title)
    popup.geometry(f"{width}x{height}")
    popup.resizable(False, False)

    bg_image = Image.open(resource_path("library.png")).resize((width, height))
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = Label(popup, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    Label(
        popup,
        text=title,
        font=FONTS["subheading"],
        bg=SHELF_COLORS["bg"],
        fg=SHELF_COLORS["text"],
        padx=15,
        pady=6
    ).place(relx=0.5, rely=0.05, anchor="n")

    panel_width = int(width * 0.75)
    panel_height = int(height * 0.78)

    canvas = Canvas(
        popup,
        width=panel_width,
        height=panel_height,
        bg=COLORS["card_bg"],
        highlightthickness=0
    )
    canvas.place(relx=0.5, rely=0.14, anchor="n")

    scrollbar = Scrollbar(popup, orient=VERTICAL, command=canvas.yview)
    scrollbar.place(relx=0.5, rely=0.14, anchor="n", x=panel_width // 2, height=panel_height)
    canvas.configure(yscrollcommand=scrollbar.set)

    body = Frame(canvas, bg=COLORS["card_bg"])
    canvas.create_window((0, 0), window=body, anchor="nw", width=panel_width)

    def update_scrollregion(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    body.bind("<Configure>", update_scrollregion)

    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", on_mousewheel))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

    return popup, body, canvas
def finalize_scrollable(canvas, body):
   
    body.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))


INDEX_CARD_BG = "#FFFDF7"
INDEX_CARD_FONT_LABEL = ("Georgia", 9, "bold")
INDEX_CARD_FONT_VALUE = ("Georgia", 9)


def record_card(parent, record):

    card = Frame(
        parent,
        bg=INDEX_CARD_BG,
        highlightthickness=1,
        highlightbackground=COLORS["border"]
    )
    card.pack(fill=X, pady=5, padx=2)

    items = record.items() if isinstance(record, dict) else enumerate(record)

    for key, value in items:
        row = Frame(card, bg=INDEX_CARD_BG)
        row.pack(fill=X, padx=10, pady=3)

        Label(
            row, text=f"{key}:", font=INDEX_CARD_FONT_LABEL,
            bg=INDEX_CARD_BG, fg=COLORS["text_dark"], anchor="w", width=16
        ).pack(side=LEFT)

        Label(
            row, text=str(value), font=INDEX_CARD_FONT_VALUE,
            bg=INDEX_CARD_BG, fg=COLORS["text_dark"], anchor="w"
        ).pack(side=LEFT, fill=X, expand=True)

    return card


def empty_result_label(parent, text="No results found."):
    return Label(
        parent, text=text, font=FONTS["label"],
        bg=COLORS["card_bg"], fg=COLORS["text_muted"]
    )



def open_results_table(parent, title, records):

    if isinstance(records, dict):
        records = [records]

    if not records:
        return None

    columns = list(records[0].keys())

    win = Toplevel(parent)
    win.title(title)
    win.geometry("950x350")
    win.configure(bg=COLORS["content_bg"])

    style = ttk.Style(win)
    style.theme_use("clam")
    style.configure(
        "Custom.Treeview",
        background=COLORS["card_bg"],
        fieldbackground=COLORS["card_bg"],
        foreground=COLORS["text_dark"],
        rowheight=34,
        font=FONTS["entry"]
    )
    style.configure(
        "Custom.Treeview.Heading",
        background=COLORS["accent"],
        foreground=COLORS["text_light"],
        font=FONTS["button"],
        relief=FLAT
    )
    style.map("Custom.Treeview", background=[("selected", COLORS["accent_hover"])])
    style.map("Custom.Treeview.Heading", background=[("active", COLORS["accent_hover"])])

    Label(
        win, text=f"{title}  ({len(records)} result{'s' if len(records) != 1 else ''})",
        font=FONTS["subheading"],
        bg=COLORS["content_bg"], fg=COLORS["text_dark"]
    ).pack(pady=(15, 5))

    container = Frame(win, bg=COLORS["content_bg"])
    container.pack(fill=BOTH, expand=True, padx=15, pady=(0, 15))

    tree = ttk.Treeview(
        container, columns=columns, show="headings",
        style="Custom.Treeview"
    )
    for col in columns:
        tree.heading(col, text=str(col).replace("_", " ").upper())
        tree.column(col, width=130, anchor="center")

    vscroll = ttk.Scrollbar(container, orient=VERTICAL, command=tree.yview)
    hscroll = ttk.Scrollbar(container, orient=HORIZONTAL, command=tree.xview)
    tree.configure(yscrollcommand=vscroll.set, xscrollcommand=hscroll.set)

    tree.grid(row=0, column=0, sticky="nsew")
    vscroll.grid(row=0, column=1, sticky="ns")
    hscroll.grid(row=1, column=0, sticky="ew")
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    for record in records:
        tree.insert("", "end", values=[record.get(col, "") for col in columns])

    return win


def styled_field(parent, label_text):
    Label(
        parent,
        text=label_text,
        font=FONTS["label"],
        bg=COLORS["card_bg"],
        fg=COLORS["text_dark"],
        anchor="w"
    ).pack(fill=X, pady=(10, 2))

    entry = Entry(
        parent,
        font=FONTS["entry"],
        bg=COLORS["input_bg"],
        fg=COLORS["text_dark"],
        relief=SOLID,
        bd=1,
        highlightthickness=1,
        highlightbackground=COLORS["border"],
        highlightcolor=COLORS["accent"]
    )
    entry.pack(fill=X, ipady=5)
    return entry


def primary_button(parent, text, command):
    btn = Button(
        parent,
        text=text,
        font=FONTS["button"],
        bg=COLORS["accent"],
        fg=COLORS["text_light"],
        activebackground=COLORS["accent_hover"],
        activeforeground=COLORS["text_light"],
        bd=3,
        relief=RAISED,
        overrelief=RAISED,
        padx=20,
        pady=8,
        cursor="hand2",
        command=command
    )
    btn.bind("<Enter>", lambda e: btn.config(bg=COLORS["accent_hover"]))
    btn.bind("<Leave>", lambda e: btn.config(bg=COLORS["accent"]))
    btn.bind("<ButtonPress-1>", lambda e: btn.config(relief=SUNKEN))
    btn.bind("<ButtonRelease-1>", lambda e: btn.config(relief=RAISED))
    return btn


def danger_button(parent, text, command):
    btn = Button(
        parent,
        text=text,
        font=FONTS["button"],
        bg=COLORS["danger"],
        fg=COLORS["text_light"],
        activebackground=COLORS["danger_hover"],
        activeforeground=COLORS["text_light"],
        bd=3,
        relief=RAISED,
        overrelief=RAISED,
        padx=20,
        pady=8,
        cursor="hand2",
        command=command
    )
    btn.bind("<Enter>", lambda e: btn.config(bg=COLORS["danger_hover"]))
    btn.bind("<Leave>", lambda e: btn.config(bg=COLORS["danger"]))
    btn.bind("<ButtonPress-1>", lambda e: btn.config(relief=SUNKEN))
    btn.bind("<ButtonRelease-1>", lambda e: btn.config(relief=RAISED))
    return btn


def module_header(parent, title):
    Label(
        parent,
        text=title,
        font=FONTS["heading"],
        bg=COLORS["content_bg"],
        fg=COLORS["text_dark"]
    ).pack(pady=(30, 20))

SHELF_COLORS = {
    "bg": "#3E2723",        
    "bg_hover": "#5D4037",
    "text": "#F5E9DA",      
}


def shelf_button(parent, text, command, relx, rely, danger=False):
    bg = COLORS["danger"] if danger else SHELF_COLORS["bg"]
    hover = COLORS["danger_hover"] if danger else SHELF_COLORS["bg_hover"]

    btn = Button(
        parent,
        text=text,
        font=FONTS["button"],
        bg=bg,
        fg=SHELF_COLORS["text"],
        activebackground=hover,
        activeforeground=SHELF_COLORS["text"],
        bd=3,
        relief=RAISED,
        overrelief=RAISED,
        padx=18,
        pady=10,
        cursor="hand2",
        command=command
    )
    btn.bind("<Enter>", lambda e: btn.config(bg=hover))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg))
    btn.bind("<ButtonPress-1>", lambda e: btn.config(relief=SUNKEN))
    btn.bind("<ButtonRelease-1>", lambda e: btn.config(relief=RAISED))
    btn.place(relx=relx, rely=rely, anchor="center")
    return btn