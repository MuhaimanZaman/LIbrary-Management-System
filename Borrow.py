from datetime import date, timedelta
from database import connection, cursor
from members import get_member
from books import get_books


def add_borrow_transaction(transaction_id, book_id, member_id, employee_id):
    """Issues a book to a member, after checking:
       1. The book exists and has at least one available copy
       2. The member exists and their membership is active
       Then auto-fills issue_date (today), due_date (issue_date + 7 days),
       sets status to 'borrowed', and decrements the book's available_copies.

       Returns (success: bool, message: str) so the GUI can show the
       right feedback either way."""

    books = get_books(book_id=book_id)
    if not books:
        return False, "Book not found."

    book = books[0]
    if book.get("available_copies", 0) <= 0:
        return False, f"'{book.get('title', 'This book')}' has no available copies right now."

    members = get_member(member_id=member_id)
    if not members:
        return False, "Member not found."

    member = members[0]
    status_value = str(member.get("membership_status", "")).strip().lower()
    if status_value != "active":
        return False, f"Member is {status_value or 'not active'} and cannot borrow books."

    issue_date = date.today()
    due_date = issue_date + timedelta(days=7)
    return_date = None
    borrow_status = "borrowed"

    sql = """
        INSERT INTO borrow_transaction
        (transaction_id, book_id, member_id, employee_id, issue_date, due_date, return_date, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (transaction_id, book_id, member_id, employee_id,
              issue_date, due_date, return_date, borrow_status)

    try:
        cursor.execute(sql, values)
        cursor.execute(
            "UPDATE books SET available_copies = available_copies - 1 WHERE book_id = %s",
            (book_id,)
        )

        connection.commit()
        return True, f"Book issued successfully. Due back on {due_date.strftime('%Y-%m-%d')}."

    except Exception as e:
        connection.rollback()
        return False, f"Error: {e}"