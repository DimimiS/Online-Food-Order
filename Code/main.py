# import Code.database as database
import csv
from database import Foodies
# import input_utils as iu

class Main:
    def __init__(self, database_path, sql_path):
        # create the database
        
        self.db = Foodies(database_path, sql_path)
        self.messages()
        self.main()
        
    def messages(self) -> None:
        self.initial_menu_options = [
            "Press 1 to: Login",
            "Press 2 to: Register",
            "Press -1 to: Exit"
        ]

        self.logged_menu_options = [
            "Press 1 to: Add order",
            "Press 2 to: Show payment methods",
            "Press 3 to: Show previous orders",
            "Press -1 to: Exit"
        ]

    def message_wrapper(self, message_list: str) -> None:
        max_length = max([len(message) for message in message_list])
        final_message = ""
        for message in message_list: 
            final_message += f"| {message:<{max_length}} |\n"
            #  " |\n| ".join(message_list) + " |\n"
        final_message = final_message[:-1] # remove the last \n 
        print(f"| {'-'*max_length} |")
        print(final_message)
        print(f"| {'-'*max_length} |\n\n")



    
    def login(self) -> None:

        print("\n")


        # get the user email and password
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        # check if the user is in the database 
        # at the time testing the functionality with just one user
        if self.db.check_passwd(email, password):
            self.logged_menu()
        else:
            print("Invalid email or password")

    def register(self) -> None:
        
        print("\n")
        
        # get the user email and password
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        # check if the user is in the database 
        # if not in the databse, add the user to the database 
        self.logged_menu()

    def logged_menu(self) -> None :

        print("\nLogged In Successfully\n")

        self.message_wrapper(self.logged_menu_options)

        # get the user option
        choice = input(">>> ") 
        if choice == "1":
            self.add_order()
        elif choice == "2":
            self.show_payment_methods()
        elif choice == "3":
            self.show_previous_orders()
        elif choice == "-1":
            return -1
        else:
            print("Invalid option")

    def main(self) -> None:
    # constantly running the app looking for user ption
        while True:
            self.message_wrapper(self.initial_menu_options)
            self.option = input(">> ")
            if self.option == "1":
                self.login()
            elif self.option == "2":
                self.register()
            elif self.option == "-1":
                break
            else:
                print("Invalid option")


if __name__ == "__main__":
    database_path="Data/foodies.sqlite" 
    sql_path="ERD/sqlite.sql"
    app = Main(database_path, sql_path)


