from notebook_hw.models.helpers import NoteBook

if __name__ == '__main__':
    note_book = NoteBook()

    while True:
        print("1. Add record")
        print("2. Delete record")
        print("3. Edit record")
        print("4. Search by first name")
        print("5. Search by phone number")
        print("6. Sort by first name")
        print("7. Sort by last name")
        print("8. Exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            note_book.add_record()
        elif choice == '2':
            note_book.delete_record()
        elif choice == '3':
            note_book.edit_record()
        elif choice == '4':
            note_book.search_by_first_name()
        elif choice == '5':
            note_book.search_by_phone_number()
        elif choice == '6':
            note_book.sort_by_first_name()
        elif choice == '7':
            note_book.sort_by_last_name()
        elif choice == '8':
            note_book.save_to_file()
            break
        else:
            print("Invalid choice. Please choose a number between 1 and 8.")
