import mysql.connector
from database.db_connection import get_db_connection

def fetch_admin_details(admin_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT ad.AdminName, d.DepartmentName, ad.MobileNo, ad.Email
    FROM AdminDetails ad
    JOIN Departments d ON ad.DepartmentID = d.DepartmentID
    WHERE ad.AdminID = %s
    """
    cursor.execute(query, (admin_id,))
    admin_details = cursor.fetchone()
    cursor.close()
    connection.close()
    return admin_details
