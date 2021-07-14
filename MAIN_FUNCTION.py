from LibraryClass import *

if __name__ == "__main__":
    print("\nHey, Welcome to GG'LIBRARY'MANAGEMENT'SYSTEM.....\n")
    while True:
        choice = input("how may i help you? ")
        choice = choice.lower()
        if "help" in choice  or "intstruct" in choice or "assist" in choice:
            print("hey, you can perform following operations.....\n")
            print("1. Add Book")
            print("2. Delete Book")
            print("3. Update Book")
            print("4. Issue Book")
            print("5. Return Book function when someone return's a Book of library.")
            print("6. Status of Books that are Issued")
            print("7. Show All Books Present in the system.")
            print("8. Exit to end up.")
            print("\nThat's it....\nThank You!!\n")
        elif "exit" in choice or "bye" in choice or "that's it" in choice:
            print("\nThank You!!\nHope you Like it...\n")
            break
        elif "add" in choice or "store" in choice or "load" in choice or "put on" in choice:
            l = Library()
        elif "remove" in choice or "delete" in choice or "erase" in choice:
            print("\nhey, specify book-id to delete that book from the system.....")
            Library.delete_book_from_database(input("Enter Book-ID : "))
        elif ("show" in choice or "gather" in choice or "display" in choice or "extract" in choice or "generate" in choice or ("give" in choice and "details" in choice)) and "all" in choice and "status" not in choice and "availability" not in choice:
            print("\nhere, is the list of all the books present.....\n")
            Library.show_all_books()
        elif ("show" in choice or "gather" in choice or "display" in choice or "extract" in choice or "generate" in choice or ("give" in choice and "details" in choice)) and "book" in choice:
            print("\nhey, to get details about particular book, specify it's id.....")
            Library.gather_particular_book_details(input("Enter Book-ID : "))
        elif "status" in choice or "availability" in choice:
            print("\nhere, is the list of all the status of the books.....\n")
            Library.show_status_of_all_books()
        elif ("update" in choice or "change" in choice or "upgrade" in choice or "amend" in choice or "modify" in choice or "revise" in choice) and ("price" in choice or "cost" in choice or "rate" in choice or "expense" in choice or "fare" in choice):
            print("\nhey, specify book-id whose price you want to change.....")
            Library.update_price(input("Enter Book-ID : "))
        elif ("check" in choice or "show" in choice or "tell" in choice or "gather" in choice) and ("availi" in choice):
            print("\nhey, specify book-id whose availibility you want to check....")
            Library.check_book_availability(input("Enter Book-ID : "))
        elif ("show" in choice or "gather" in choice or "display" in choice or "extract" in choice or "generate" in choice or ("give" in choice and "details" in choice)) and ("id" in choice or "book_id" in choice):
            print("\nhey, specify the title of the book.....")
            Library.get_book_id(input("Enter Book-TITLE : "))
        elif ("get" in choice or "give" in choice or "show" in choice) and ("issued" in choice):
            print("\nhey, welcome.....")
            Library.gather_who_issued_book(input("Enter Book-ID : "))
        elif ("issue" in choice):
            print("\nhey, welcome please specify the book-d you want to issue.....")
            Library.issue_book(input("Enter Book-ID : "))
        elif ("return" in choice or "give back" in choice):
            print("\nhey, welcome please specify the book-id that you want to return.....")
            Library.return_book(input("Enter Book-ID : ")) 
        else:
            print("\nInvalid Functioning.\n") 