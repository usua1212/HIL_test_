from notebook_hw.models.cls_contacts import Contact
import csv
import re


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class NoteBook(metaclass=SingletonMeta):
    def __init__(self):
        self.records = []

        try:
            with open('data\\contacts.csv') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    record = Contact(
                        row['first_name'],
                        row['last_name'],
                        row['phone_number'],
                        row['address'],
                        row['date_of_birth']
                    )
                    self.records.append(record)
        except FileNotFoundError:
            print("File 'contacts.csv' not found.")

    def add_record(self):
        first_name = input("Enter first name: ").capitalize()
        last_name = input("Enter last name: ").capitalize()
        while True:
            phone_number = input("Enter phone number (+380xxxxxxxxx): ")
            if re.match(r"^\+380\d{9}$", phone_number):
                break
            else:
                print("Error: Invalid phone number format. Please try again.")

        address = input("Enter address (leave blank if not applicable): ")
        while True:
            date_of_birth = input("Enter date of birth (dd/mm/yyyy): ")
            if re.match(r"^(0[1-9]|[12]\d|3[01])\/(0[1-9]|1[0-2])\/\d{4}$", date_of_birth):
                break
            else:
                print("Error: Invalid date format. Please try again.")
        if not first_name or not last_name or not phone_number:
            print("Error: First name, last name, and phone number are required.")
            return
        record = Contact(first_name, last_name, phone_number, address, date_of_birth)
        self.records.append(record)
        print("Record added successfully.")
        print(record)

    def delete_record(self):
        for i, record in enumerate(self.records):
            print(f"{i + 1}. {record.first_name} {record.last_name} - {record.phone_number}")
        record_num = input("Enter the number of the record to delete: ")
        try:
            record_num = int(record_num)
            if 1 <= record_num <= len(self.records):
                self.records.pop(record_num - 1)
                print("Record deleted successfully.")
            else:
                print("Invalid record number.")
        except ValueError:
            print("Invalid input.")

    def edit_record(self):
        # Виведення списку контактів
        print("Contacts list:")
        for i, record in enumerate(self.records):
            print(f"{i + 1}. {record.first_name} {record.last_name}")
        # Вибір контакту
        choice = input("Choose contact to edit (enter number): ")
        try:
            idx = int(choice) - 1
            if idx < 0 or idx >= len(self.records):
                raise ValueError()
        except ValueError:
            print("Invalid choice.")
            return
        record = self.records[idx]
        # Редагування контакту
        new_first_name = input(
            f"Enter new first name (leave blank if not applicable, current value: {record.first_name}): ")
        new_last_name = input(
            f"Enter new last name (leave blank if not applicable, current value: {record.last_name}): ")
        new_phone_number = input(
            f"Enter new phone number (leave blank if not applicable, current value: {record.phone_number}): ")
        new_address = input(f"Enter new address (leave blank if not applicable, current value: {record.address}): ")
        new_date_of_birth = input(
            f"Enter new date of birth (leave blank if not applicable, current value: {record.date_of_birth}): ")
        if new_first_name:
            record.first_name = new_first_name
        if new_last_name:
            record.last_name = new_last_name
        if new_phone_number:
            record.phone_number = new_phone_number
        if new_address:
            record.address = new_address
        if new_date_of_birth:
            record.date_of_birth = new_date_of_birth
        print("Record updated successfully.")

    def search_by_first_name(self):
        first_name = input("Enter first name: ")
        matching_records = []
        for record in self.records:
            if record.first_name.lower().startswith(first_name.lower()):
                matching_records.append(record)
        if matching_records:
            for record in matching_records:
                print(record)
        else:
            print("No matching records found.")

    def search_by_phone_number(self):
        phone_number = input("Enter phone number to search (+380xxxxxxxxx): ")
        while not re.match(r"^\+380\d{5,9}$", phone_number):
            print("Error: Invalid phone number format. Please try again.")
            phone_number = input("Enter phone number to search (+380xxxxxxxxx): ")
        result = [record for record in self.records if phone_number in record.phone_number]
        if result:
            for record in result:
                print(record)
        else:
            print("No records found.")

    def sort_by_first_name(self):
        self.records.sort(key=lambda x: x.first_name)
        for record in self.records:
            print(record)

    def sort_by_last_name(self):
        self.records.sort(key=lambda x: x.last_name)
        for record in self.records:
            print(record)

    def save_to_file(self):
        with open('data\\contacts.csv', mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['first_name', 'last_name', 'phone_number', 'address', 'date_of_birth'])
            for record in self.records:
                writer.writerow(
                    [record.first_name, record.last_name, record.phone_number, record.address, record.date_of_birth])
        print(f"{len(self.records)} records saved to file.")