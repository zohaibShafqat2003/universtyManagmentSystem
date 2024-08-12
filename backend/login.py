from database.db_connection import get_db_connection

def authenticate_user(username, password, role):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "SELECT LoginID FROM Login WHERE UserName = %s AND Password = %s AND Role = %s"
    print(f"Executing query: {query} with values: {username}, {password}, {role}")
    cursor.execute(query, (username, password, role))
    result = cursor.fetchone()
    print(f"Query result: {result}")
    cursor.close()
    connection.close()
    return result  # This will return None if authentication fails, otherwise it returns the tuple (LoginID,)


