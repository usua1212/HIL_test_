def main():
    notebook = Notebook()
    notebook.load_from_file()

    while True:
        print("1. Add record")
        print("2. Delete record")
        print("3. Edit record")
        print("4. Search by name")
        print("5. Search by phone number")
        print("6. Sort by first name")
        print("7. Sort by last name")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            # TODO: Prompt the user for the record fields and add it to the notebook
        elif choice == "2":
            # TODO: Prompt the user for the index of the record to delete and delete it from the notebook
        elif choice == "3":
            # TODO: Prompt the user for the index of the record to edit and the new record fields, and update it in the notebook
        elif choice == "4":
            # TODO: Prompt the user for the name to search and print the matching records
        elif choice == "5":
            # TODO: Prompt the user for the phone number to search and print the matching records
        elif choice == "6":
            # TODO: Sort the records by first name and print them
        elif choice == "7":
            # TODO: Sort the records by last name and print them
        elif choice == "8":
            notebook.save_to_file()
            break
        else:
            print("Invalid choice")

