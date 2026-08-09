from database import connection,cursor

def add_books(book_id,title,author_id,publisher_id,category_id,isbn,publication_year,edition,language,total_copies,available_copies,shelf_location,price,date_added):
    sql = """
    INSERT INTO books(book_id,title,author_id,publisher_id,category_id,isbn,publication_year,edition,language,total_copies,available_copies,shelf_location,price,date_added)
    values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    values = (book_id,
              title,
              author_id,
              publisher_id,
              category_id,
              isbn,
              publication_year,
              edition,
              language,
              total_copies,
              available_copies,
              shelf_location,
              price,
              date_added)
    
    try:
        cursor.execute(sql,values)
        connection.commit()
        return True, f"Book '{title}' added successfully."
    except Exception as e:
        connection.rollback()
        return False, f"Could not add book: {e}"


def get_books(book_id=None, title=None):
    try:
        if book_id:
            cursor.execute("SELECT * FROM books WHERE book_id = %s", (book_id,))
            rows = cursor.fetchall()
            return _rows_to_dicts(rows)

        if title:
            cursor.execute("SELECT * FROM books WHERE title = %s", (title,))
            rows = cursor.fetchall()

            if rows:
                return _rows_to_dicts(rows)

        
            cursor.execute("SELECT * FROM books WHERE title LIKE %s", (f"%{title}%",))
            rows = cursor.fetchall()
            return _rows_to_dicts(rows)

        return []
    except Exception as e:
        print("Error:", e)
        return None


def _rows_to_dicts(rows):
    if not rows:
        return []
    if isinstance(rows[0], dict):
        return rows
    columns = [desc[0] for desc in cursor.description]
    return [dict(zip(columns, row)) for row in rows]
    

def update_book(book_id,new_title):
    sql = """
    update books 
    set title = %s
    where book_id = %s """

    values = (new_title, book_id)
    try:
        cursor.execute(sql,values)
        connection.commit()
        if cursor.rowcount == 0:
            return False, f"No book found with ID {book_id}. Nothing was updated."
        return True, f"Book {book_id} updated successfully."
    except Exception as e:
        connection.rollback()
        return False, f"Could not update book: {e}"



def delete_book(book_id):
    sql = """ Delete From books where book_id=%s"""

    try:
        cursor.execute(sql,(book_id,))
        connection.commit()
        if cursor.rowcount == 0:
            return False, f"No book found with ID {book_id}. Nothing was deleted."
        return True, f"Book {book_id} deleted successfully."
    except Exception as e:
        connection.rollback()
        return False, f"Could not delete book: {e}"