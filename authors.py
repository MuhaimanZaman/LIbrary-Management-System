from database import connection,cursor

def add_author(author_id, author_name, country, birth_date):
    sql = """INSERT INTO authors(author_id, author_name, country,birth_date)
    values(%s,%s,%s,%s)"""

    values = (author_id,
              author_name,
              country,
              birth_date)
    try:
        cursor.execute(sql,values)
        connection.commit()
        return True, f"Author '{author_name}' added successfully."
    except Exception as e:
        connection.rollback()
        return False, f"Could not add author: {e}"


def _rows_to_dicts(rows):
    if not rows:
        return []
    if isinstance(rows[0], dict):
        return rows
    columns = [desc[0] for desc in cursor.description]
    return [dict(zip(columns, row)) for row in rows]


def get_author(author_name):
    sql = "Select * from authors where author_name = %s"

    try:
        cursor.execute(sql, (author_name,))
        rows = cursor.fetchall()
        return _rows_to_dicts(rows)
    except Exception as e:
        print("Error:", e)
        return None


def update_author(author_id,new_author_name):
    sql = """
    update authors 
    set author_name = %s
    where author_id = %s """

    values = (new_author_name, author_id)
    try:
        cursor.execute(sql,values)
        connection.commit()
        if cursor.rowcount == 0:
            return False, f"No author found with ID {author_id}. Nothing was updated."
        return True, f"Author {author_id} updated successfully."
    except Exception as e:
        connection.rollback()
        return False, f"Could not update author: {e}"


def delete_author(author_name):
    sql = """ Delete From authors where author_id = %s"""

    try:
        cursor.execute(sql,(author_name,))
        connection.commit()
        if cursor.rowcount == 0:
            return False, f"No author found named '{author_name}'. Nothing was deleted."
        return True, f"Author '{author_name}' deleted successfully."
    except Exception as e:
        connection.rollback()
        return False, f"Could not delete author: {e}"