import json
from database import Database
from request import Request

def main(insert_eligible):
    while True:
        print("Enter User Name")
        user_name = input()
        print("Enter Password")
        password = input()

        database = Database(user_name, password)

        if database.initialized:
            break
        else:
            print("Invalid credentials. Please try again.")

    while True:
        print("\nMenu")
        print("1. Insert")
        print("2. Search")
        print("3. Exit")

        choice = input("Enter choice (1, 2, 3): ")

        if choice == '1' and insert_eligible:
            database.insert_table()
        elif choice == '2':
            database.search()
        elif choice == '3':
            print("Exiting program...")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main(True)