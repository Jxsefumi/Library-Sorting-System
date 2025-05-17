import mysql.connector

def connect():
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root@123!",
            database="library_db"
        )
        return con
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None