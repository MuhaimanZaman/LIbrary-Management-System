from datetime import date
from database import connection, cursor

FINE_PER_DAY = 100  


def _rows_to_dicts(rows):
    if not rows:
        return []
    if isinstance(rows[0], dict):
        return rows
    columns = [desc[0] for desc in cursor.description]
    return [dict(zip(columns, row)) for row in rows]


def get_borrow_transaction(transaction_id):
    cursor.execute("SELECT * FROM borrow_transaction WHERE transaction_id = %s", (transaction_id,))
    results = _rows_to_dicts(cursor.fetchall())
    return results[0] if results else None

def return_book(transaction_id, remarks=None):

    try:
        transaction = get_borrow_transaction(transaction_id)

        if not transaction:
            return False, "Transaction not found."

        if str(transaction.get("status", "")).strip().lower() == "returned":
            return False, "This book has already been returned."

        book_id = transaction["book_id"]
        due_date = transaction["due_date"]
        return_date = date.today()

        
        if hasattr(due_date, "date"):
            due_date = due_date.date()

        days_late = (return_date - due_date).days
        fine_amount = days_late * FINE_PER_DAY if days_late > 0 else 0

       
        cursor.execute(
            "UPDATE borrow_transaction SET return_date = %s, status = %s WHERE transaction_id = %s",
            (return_date, "returned", transaction_id)
        )

      
        cursor.execute(
            "UPDATE books SET available_copies = available_copies + 1 WHERE book_id = %s",
            (book_id,)
        )

        if fine_amount > 0:
            fine_remarks = remarks or f"Returned {days_late} day{'s' if days_late != 1 else ''} late."
            cursor.execute(
                """INSERT INTO fines (transaction_id, amount, paid, payment_date, remarks)
                   VALUES (%s, %s, %s, %s, %s)""",
                (transaction_id, fine_amount, 0, None, fine_remarks)
            )

        connection.commit()

        if fine_amount > 0:
            return True, f"Book returned. {days_late} day(s) late — fine of {fine_amount:.2f} recorded (unpaid)."
        return True, "Book returned on time. No fine."

    except Exception as e:
        connection.rollback()
        return False, f"Error: {e}"


def get_overdue_transactions():
    try:
        cursor.execute(
            "SELECT * FROM borrow_transaction WHERE status = %s AND due_date < %s",
            ("borrowed", date.today())
        )
        return _rows_to_dicts(cursor.fetchall())
    except Exception as e:
        print("Error:", e)
        return []