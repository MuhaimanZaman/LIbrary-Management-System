from database import connection,cursor

def add_category(category_id,category_name,description):
    sql = """INSERT INTO categories(category_id, category_name, description)
    values(%s,%s,%s)"""

    values = (category_id,
              category_name,
              description)
    try:
        cursor.execute(sql,values)
        connection.commit()
        return True, f"Category '{category_name}' added successfully."
    except Exception as e:
        connection.rollback()
        return False, f"Could not add category: {e}"


def get_category(category_name):
    sql = "Select * from categories where category_name = %s"

    try:
        cursor.execute(sql, (category_name,))
        row = cursor.fetchone()

        if row is None:
            return []

        if isinstance(row, dict):
            return [row]

        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row))]
    except Exception as e:
        print("Error:", e)
        return None


def update_category(category_id,new_category_name):
    sql = """
    update categories 
    set category_name = %s
    where category_id = %s """

    values = (new_category_name, category_id)
    try:
        cursor.execute(sql,values)
        connection.commit()
        if cursor.rowcount == 0:
            return False, f"No category found with ID {category_id}. Nothing was updated."
        return True, f"Category {category_id} updated successfully."
    except Exception as e:
        connection.rollback()
        return False, f"Could not update category: {e}"


def delete_category(category_id):
    sql = """ Delete From categories where category_id = %s"""

    try:
        cursor.execute(sql,(category_id,))
        connection.commit()
        if cursor.rowcount == 0:
            return False, f"No category found with ID {category_id}. Nothing was deleted."
        return True, f"Category {category_id} deleted successfully."
    except Exception as e:
        connection.rollback()
        return False, f"Could not delete category: {e}"