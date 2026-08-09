from database import connection,cursor

def add_publisher(publisher_id,publisher_name,address,phone,email):
    sql = """INSERT INTO publishers(publisher_id, publisher_name, address, phone, email)
    values(%s,%s,%s,%s,%s)"""

    values = (publisher_id,
              publisher_name,
              address,
              phone,
              email)
    try:
        cursor.execute(sql,values)
        connection.commit()
        return True, f"Publisher '{publisher_name}' added successfully."
    except Exception as e:
        connection.rollback()
        return False, f"Could not add publisher: {e}"


def _rows_to_dicts(rows):
    if not rows:
        return []
    if isinstance(rows[0], dict):
        return rows
    columns = [desc[0] for desc in cursor.description]
    return [dict(zip(columns, row)) for row in rows]


def get_publisher(publisher_name):
    try:
        cursor.execute("SELECT * FROM publishers WHERE publisher_name = %s", (publisher_name,))
        rows = cursor.fetchall()

        if rows:
            return _rows_to_dicts(rows)

        cursor.execute("SELECT * FROM publishers WHERE publisher_name LIKE %s", (f"%{publisher_name}%",))
        rows = cursor.fetchall()
        return _rows_to_dicts(rows)
    except Exception as e:
        print("Error:", e)
        return None


def update_publisher(publisher_id,new_publisher_name):
    sql = """
    update publishers
    set publisher_name = %s
    where publisher_id = %s """

    values = (new_publisher_name, publisher_id)
    try:
        cursor.execute(sql,values)
        connection.commit()
        if cursor.rowcount == 0:
            return False, f"No publisher found with ID {publisher_id}. Nothing was updated."
        return True, f"Publisher {publisher_id} updated successfully."
    except Exception as e:
        connection.rollback()
        return False, f"Could not update publisher: {e}"


def delete_publisher(publisher_name):
    sql = """ Delete From publishers where publisher_name = %s"""

    try:
        cursor.execute(sql,(publisher_name,))
        connection.commit()
        if cursor.rowcount == 0:
            return False, f"No publisher found named '{publisher_name}'. Nothing was deleted."
        return True, f"Publisher '{publisher_name}' deleted successfully."
    except Exception as e:
        connection.rollback()
        return False, f"Could not delete publisher: {e}"