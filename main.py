from connect import connect

    # responsible for sorting the books
def showBooks(cursor, sort_order=None, sort_by=None):
    query = "SELECT * FROM books"
    if sort_by:
        if sort_by == "author":
            query += " ORDER BY author"
        elif sort_by == "category":
            query += " ORDER BY category"
        else:
            query += " ORDER BY name"
        
        if sort_order:
            query += f" {sort_order}"
    
    cursor.execute(query)
    books = cursor.fetchall()

    if books: #checks if the books are available or not
        print("\nBooks in the Library:")
        for book in books:
            availability = "Available" if book[5] else "Borrowed"
            print(f"{book[0]}. {book[1]} by {book[2]} | {book[3]} | {book[4]} | {availability}")
    else:
        print("No books found in the library.")

def insertBook(cursor, con, name, author, publication_date, category): #responsible for inserting books into the MySQL
    cursor.execute("INSERT INTO books (name, author, publication_date, category, available) VALUES (%s, %s, %s, %s, TRUE)",
                   (name, author, publication_date, category))
    con.commit()

def deleteBook(cursor, con, book_id): #pretty much what the define is called
    cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
    con.commit()

def borrowBook(cursor, con, book_id): #should I really explain?
    cursor.execute("UPDATE books SET available = FALSE WHERE id = %s", (book_id,))
    con.commit()

def returnBook(cursor, con, book_id): #Mein gott, das ist verständlich!
    cursor.execute("UPDATE books SET available = TRUE WHERE id = %s", (book_id,))
    con.commit()

def main(): #YAY we got here, basically here where the magic begins *wink wink
    print("\033[1mWelcome to Library Sorting System\033[0m".center(100, "="))
    
    # user_name = input("Enter your name: ") // I commented these lines of codes, Weil ich zu faul bin, das zu machen. 
    # user_id = user_name + "_ID" // the purpose of this should show the name of the person who borrows the book, aber ich bin kein Deutscher.
    #German efficiency basically does not exist in this file of abomination.
    #Viel Glück bein Lesen!

    con = connect() #this part connects this abomination to the database(MySQL in this case yay? or nay?)
    if con is None:
        print("Failed to connect to the database. Exiting...")
        return
    cursor = con.cursor()

    while True: #I think you can understand this? I mean who wouldn't?
        print("\nWhat do you want to do?")
        print("1. Insert")
        print("2. Delete")
        print("3. Sort")
        print("4. Show")
        print("5. Read")
        action = input("Choose an action: ")

        if action == "1": #basically ask a bunch of questions, then calls the insertBook function to *wink wink
            name = input("What is the name of the book: ")
            if not name.strip():
                print("Invalid input: Name cannot be blank")
                continue
            author = input("Who is the Author: ")
            if not author.strip():
                print("Invalid input: Author cannot be blank")
                continue
            publication_date = input("Publication date (YYYY-MM-DD): ")
            category = input("What is the subject of the book? you can input a category that does not exist from the choices. (Science, Math, History, Language, Programming, Fiction): ")
            #IHHHH
            if category not in ["Science", "Math", "History", "Language", "Programming", "Fiction"]:
                print("Custom category entered.")
            
            insertBook(cursor, con, name, author, publication_date, category)
            print("Book inserted successfully.") #sumakses siya eh, pero nag step by the step naman siya before mag success
        
        elif action == "2": #this deletes the past.
                        #napaka OA naman ^
            book_id = int(input("Enter the book ID you want to delete: "))
            cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
            book = cursor.fetchone()
            if book:
                confirmation = input(f"Are you sure you want to delete '{book[1]}'? (Yes/No): ")
                if confirmation.lower() == "yes":
                    deleteBook(cursor, con, book_id)
                    print(f"Book '{book[1]}' deleted successfully.")
                else:
                    print("Delete action cancelled.")
            else:
                print("Book not found.")

        elif action == "3": #I mean you can literally see what it does based on the print
            print("\nHow do you want to sort the books?")
            print("1. By Name")
            print("2. By Author")
            print("3. By Category")
            sort_choice = input("Choose sorting option: ")

            #I think therefore yes
            while True:
                sort_order = input("Do you want ascending (ASC) or descending (DESC) order? ").strip().upper()
                if sort_order in {"ASC", "DESC"}:
                    break
                print("Invalid sort order. Please enter either 'ASC' or 'DESC'.")

            if sort_choice == "1":
                showBooks(cursor, sort_order, "name")
            elif sort_choice == "2":
                showBooks(cursor, sort_order, "author")
            elif sort_choice == "3":
                showBooks(cursor, sort_order, "category")
            else:
                print("Invalid choice.") #dang, imagine not being an option/choice
        
        elif action == "4":
            showBooks(cursor) #ilabas niyo ang libro! 
        
        elif action == "5": 
            book_id = int(input("Which book would you like to read? Enter book ID: "))
            cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
            book = cursor.fetchone()
            if book:
                print(f"\nReading Book: {book[1]}") 
                print(f"Author: {book[2]}")
                print(f"Publication Date: {book[3]}")
                print(f"Category: {book[4]}")

                action = input("Would you like to Borrow, Return, or Close the book? (B/R/C): ").lower()
                if action == "b":
                    if book[5] == 0:
                        print(f"The book '{book[1]}' is already borrowed and not available.")
                        #I mean you can literally see if the book has already been borrowed, so why keep trying? 
                        #there's no magic here.
                    else:
                        borrowBook(cursor, con, book_id)
                        print(f"The book '{book[1]}' is now borrowed.")
                        #I hope you don't steal the book, I mean I literally removed the name function because I am too lazy
                        #to input it again in the SQL because why not?
                elif action == "r":
                    if book[5] == 1:
                        print(f"The book '{book[1]}' is already available and cannot be returned.")
                        #Ich weiß nicht, was sprechen
                    else:
                        returnBook(cursor, con, book_id)
                        print(f"The book '{book[1]}' has been returned.")
                elif action == "c":
                    print("Closing the book reading.")
            else:
                print("The book you have chosen is currently not in our system.")
                #did you really check if the book exist in the system???
        else:
            print("Invalid choice. Please choose a valid action.")
            #I think you should remake this and add your own action!
        
        while True:
            continue_action = input("Do you want to continue? (Y/N): ").strip().upper()
            if continue_action == "Y":
                break
            elif continue_action == "N":
                cursor.close()
                con.close()
                print("Goodbye!")
                return
            else:
                print("Invalid input. Please enter 'Y' for Yes or 'N' for No.")


if __name__ == "__main__":
    main()