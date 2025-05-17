from connect import connect

def create():
        con = connect()
        if con is None:
            print("Failed to connect to the database. Exiting...")
            return
        cursor = con.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS library_db")
        print("Database created or already exists.")
        
        cursor.execute("USE library_db")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                author VARCHAR(255) NOT NULL,
                publication_date DATE,
                category VARCHAR(255),
                available BOOLEAN DEFAULT TRUE
            )
        """)
        print("Table 'books' created successfully.")

        cursor.close()
        con.close()

