from database import connection,cursor

def add_member(member_id,first_name, last_name, gender, date_of_birth,phone,email,address,membership_date,membership_status):
    sql = """INSERT INTO members(member_id, first_name, last_name, gender, date_of_birth,phone, email, address, membership_date,membership_status)
    values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

    values = (member_id,
              first_name,
              last_name,
              gender,
              date_of_birth,
              phone,
              email,
              address,
              membership_date,
              membership_status)
    try:
        cursor.execute(sql,values)
        connection.commit()
        return True, f"Member '{first_name} {last_name}' added successfully."
    except Exception as e:
        connection.rollback()
        return False, f"Could not add member: {e}"


def _rows_to_dicts(rows):
    if not rows:
        return []
    if isinstance(rows[0], dict):
        return rows
    columns = [desc[0] for desc in cursor.description]
    return [dict(zip(columns, row)) for row in rows]


def get_member(member_id=None, first_name=None, last_name=None):
    try:
        if member_id:
            cursor.execute("SELECT * FROM members WHERE member_id = %s", (member_id,))
            return _rows_to_dicts(cursor.fetchall())

        if first_name and last_name:
            cursor.execute(
                "SELECT * FROM members WHERE first_name = %s AND last_name = %s",
                (first_name, last_name)
            )
            rows = cursor.fetchall()
            if rows:
                return _rows_to_dicts(rows)

            cursor.execute(
                "SELECT * FROM members WHERE first_name LIKE %s AND last_name LIKE %s",
                (f"%{first_name}%", f"%{last_name}%")
            )
            return _rows_to_dicts(cursor.fetchall())

        if first_name:
            cursor.execute("SELECT * FROM members WHERE first_name = %s", (first_name,))
            rows = cursor.fetchall()
            if rows:
                return _rows_to_dicts(rows)
            cursor.execute("SELECT * FROM members WHERE first_name LIKE %s", (f"%{first_name}%",))
            return _rows_to_dicts(cursor.fetchall())

        if last_name:
            cursor.execute("SELECT * FROM members WHERE last_name = %s", (last_name,))
            rows = cursor.fetchall()
            if rows:
                return _rows_to_dicts(rows)
            cursor.execute("SELECT * FROM members WHERE last_name LIKE %s", (f"%{last_name}%",))
            return _rows_to_dicts(cursor.fetchall())

        return []
    except Exception as e:
        print("Error:", e)
        return None


def update_members(member_id,new_first_name):
    sql = """
    update members 
    set first_name = %s
    where member_id = %s """

    values = (new_first_name, member_id)
    try:
        cursor.execute(sql,values)
        connection.commit()
        if cursor.rowcount == 0:
            return False, f"No member found with ID {member_id}. Nothing was updated."
        return True, f"Member {member_id} updated successfully."
    except Exception as e:
        connection.rollback()
        return False, f"Could not update member: {e}"

def delete_member(member_id):
    sql = """ Delete From members where member_id = %s"""

    try:
        cursor.execute(sql,(member_id,))
        connection.commit()
        if cursor.rowcount == 0:
            return False, f"No member found with ID {member_id}. Nothing was deleted."
        return True, f"Member {member_id} deleted successfully."
    except Exception as e:
        connection.rollback()
        return False, f"Could not delete member: {e}"