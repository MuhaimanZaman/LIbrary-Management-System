from datetime import date
from database import connection, cursor


def _rows_to_dicts(rows):
    if not rows:
        return []
    if isinstance(rows[0], dict):
        return rows
    columns = [desc[0] for desc in cursor.description]
    return [dict(zip(columns, row)) for row in rows]


def _row_to_dict(row):
    if row is None:
        return None
    if isinstance(row, dict):
        return row
    columns = [desc[0] for desc in cursor.description]
    return dict(zip(columns, row))


def get_currently_borrowed():
    sql = """
        SELECT bt.transaction_id, b.title, m.first_name, m.last_name,
               bt.issue_date, bt.due_date
        FROM borrow_transaction bt
        JOIN books b ON bt.book_id = b.book_id
        JOIN members m ON bt.member_id = m.member_id
        WHERE bt.status = 'borrowed'
        ORDER BY bt.due_date ASC
    """
    try:
        cursor.execute(sql)
        return _rows_to_dicts(cursor.fetchall())
    except Exception as e:
        print("Error:", e)
        return []


def get_overdue_books():
    sql = """
        SELECT bt.transaction_id, b.title, m.first_name, m.last_name,
               bt.due_date,
               DATEDIFF(%s, bt.due_date) AS days_overdue
        FROM borrow_transaction bt
        JOIN books b ON bt.book_id = b.book_id
        JOIN members m ON bt.member_id = m.member_id
        WHERE bt.status = 'borrowed' AND bt.due_date < %s
        ORDER BY days_overdue DESC
    """
    try:
        today = date.today()
        cursor.execute(sql, (today, today))
        return _rows_to_dicts(cursor.fetchall())
    except Exception as e:
        print("Error:", e)
        return []

def get_most_borrowed(limit=10):
    sql = """
        SELECT b.book_id, b.title, COUNT(bt.transaction_id) AS times_borrowed
        FROM borrow_transaction bt
        JOIN books b ON bt.book_id = b.book_id
        GROUP BY b.book_id, b.title
        ORDER BY times_borrowed DESC
        LIMIT %s
    """
    try:
        cursor.execute(sql, (limit,))
        return _rows_to_dicts(cursor.fetchall())
    except Exception as e:
        print("Error:", e)
        return []


def get_books_by_category():
    sql = """
        SELECT c.category_name, COUNT(b.book_id) AS total_titles,
               COALESCE(SUM(b.total_copies), 0) AS total_copies
        FROM categories c
        LEFT JOIN books b ON b.category_id = c.category_id
        GROUP BY c.category_id, c.category_name
        ORDER BY total_titles DESC
    """
    try:
        cursor.execute(sql)
        return _rows_to_dicts(cursor.fetchall())
    except Exception as e:
        print("Error:", e)
        return []


def get_library_statistics():
    stats = {}
    try:
        cursor.execute("SELECT COUNT(*) AS c FROM books")
        stats["total_titles"] = _row_to_dict(cursor.fetchone())["c"]

        cursor.execute("SELECT COALESCE(SUM(total_copies),0) AS c FROM books")
        stats["total_copies"] = _row_to_dict(cursor.fetchone())["c"]

        cursor.execute("SELECT COALESCE(SUM(available_copies),0) AS c FROM books")
        stats["available_copies"] = _row_to_dict(cursor.fetchone())["c"]

        cursor.execute("SELECT COUNT(*) AS c FROM members")
        stats["total_members"] = _row_to_dict(cursor.fetchone())["c"]

        cursor.execute("SELECT COUNT(*) AS c FROM members WHERE membership_status = 'active'")
        stats["active_members"] = _row_to_dict(cursor.fetchone())["c"]

        cursor.execute("SELECT COUNT(*) AS c FROM borrow_transaction WHERE status = 'borrowed'")
        stats["currently_borrowed"] = _row_to_dict(cursor.fetchone())["c"]

        cursor.execute(
            "SELECT COUNT(*) AS c FROM borrow_transaction WHERE status = 'borrowed' AND due_date < %s",
            (date.today(),)
        )
        stats["overdue_count"] = _row_to_dict(cursor.fetchone())["c"]

        cursor.execute("SELECT COALESCE(SUM(amount),0) AS c FROM fines WHERE paid = 0")
        stats["unpaid_fines_total"] = _row_to_dict(cursor.fetchone())["c"]

        return stats
    except Exception as e:
        print("Error:", e)
        return {}


def get_outstanding_fines():
    sql = """
        SELECT f.fine_id, m.first_name, m.last_name, f.amount, f.remarks
        FROM fines f
        JOIN borrow_transaction bt ON f.transaction_id = bt.transaction_id
        JOIN members m ON bt.member_id = m.member_id
        WHERE f.paid = 0
        ORDER BY f.amount DESC
    """
    try:
        cursor.execute(sql)
        return _rows_to_dicts(cursor.fetchall())
    except Exception as e:
        print("Error:", e)
        return []


def get_member_history(member_id):
    sql = """
        SELECT bt.transaction_id, b.title, bt.issue_date, bt.due_date,
               bt.return_date, bt.status
        FROM borrow_transaction bt
        JOIN books b ON bt.book_id = b.book_id
        WHERE bt.member_id = %s
        ORDER BY bt.issue_date DESC
    """
    try:
        cursor.execute(sql, (member_id,))
        return _rows_to_dicts(cursor.fetchall())
    except Exception as e:
        print("Error:", e)
        return []