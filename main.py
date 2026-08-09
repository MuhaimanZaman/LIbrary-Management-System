from tkinter import *
from PIL import Image, ImageTk
from books_gui import show_books
from members_gui import show_members
from authors_gui import show_authors
from Borrow_gui import show_borrow
from Returned_book_gui import show_return
from Reports_gui import show_reports
from categories_gui import show_categories
from publishers_gui import show_publishers
from styles import COLORS, FONTS, make_sidebar_button, set_active_sidebar_button, module_header, resource_path

window = Tk()
window.title("Library Management System")
window.geometry("1200x700")
window.resizable(False, False)


image = Image.open(resource_path("library.png"))
image = image.resize((980, 700))
bg_image = ImageTk.PhotoImage(image)


sidebar = Frame(window, bg=COLORS["sidebar_bg"], width=220)
sidebar.pack(side=LEFT, fill=Y)
sidebar.pack_propagate(False)

sidebar_divider = Frame(window, bg=COLORS["accent"], width=5)
sidebar_divider.pack(side=LEFT, fill=Y)

Label(
    sidebar,
    text="📚 LMS",
    font=("Segoe UI", 16, "bold"),
    bg=COLORS["sidebar_bg"],
    fg=COLORS["text_light"],
    pady=25
).pack()

content_frame = Frame(window, bg=COLORS["image_backdrop"])
content_frame.pack(side=RIGHT, fill=BOTH, expand=True)

bg_label = Label(content_frame, image=bg_image, bg=COLORS["image_backdrop"])
bg_label.place(x=0, y=0, relwidth=1, relheight=1)


def clear_content():
    for widget in content_frame.winfo_children():
        if widget != bg_label:
            widget.destroy()


def open_books():
    clear_content()
    set_active_sidebar_button(nav_buttons, btn_books)
    show_books(content_frame)

def open_members():
    clear_content()
    set_active_sidebar_button(nav_buttons, btn_members)
    show_members(content_frame)

def open_authors():
    clear_content()
    set_active_sidebar_button(nav_buttons, btn_authors)
    show_authors(content_frame)

def open_borrow():
    clear_content()
    set_active_sidebar_button(nav_buttons, btn_borrow)
    show_borrow(content_frame)

def open_return():
    clear_content()
    set_active_sidebar_button(nav_buttons, btn_return)
    show_return(content_frame)

def open_reports():
    clear_content()
    set_active_sidebar_button(nav_buttons, btn_reports)
    show_reports(content_frame)

def open_categories():
    clear_content()
    set_active_sidebar_button(nav_buttons, btn_categories)
    show_categories(content_frame)

def open_publishers():
    clear_content()
    set_active_sidebar_button(nav_buttons, btn_publishers)
    show_publishers(content_frame)

def placeholder(name, btn):
    def handler():
        clear_content()
        set_active_sidebar_button(nav_buttons, btn)
        module_header(content_frame, name)
        Label(content_frame, text=f"{name} module coming soon",
              font=FONTS["label"], bg=COLORS["content_bg"], fg=COLORS["text_muted"]).pack()
    return handler

btn_books = make_sidebar_button(sidebar, "Books", lambda: open_books())
btn_books.pack(fill=X)
btn_members = make_sidebar_button(sidebar, "Members", lambda: open_members())
btn_members.pack(fill=X)
btn_authors = make_sidebar_button(sidebar, "Authors", lambda: open_authors())
btn_authors.pack(fill=X)
btn_categories = make_sidebar_button(sidebar, "Categories", lambda: open_categories())
btn_categories.pack(fill=X)
btn_publishers = make_sidebar_button(sidebar, "Publishers", lambda: open_publishers())
btn_publishers.pack(fill=X)
btn_borrow = make_sidebar_button(sidebar, "Borrow", lambda: open_borrow())
btn_borrow.pack(fill=X)
btn_return = make_sidebar_button(sidebar, "Return", lambda: open_return())
btn_return.pack(fill=X)
btn_reports = make_sidebar_button(sidebar, "Reports", lambda: open_reports())
btn_reports.pack(fill=X)

nav_buttons = [btn_books, btn_members, btn_authors, btn_categories,
               btn_publishers, btn_borrow, btn_return, btn_reports]

open_books()
window.mainloop()