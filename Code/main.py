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
        """ Create list of the options that you want want to show"""
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

    def message_wrapper(self, message_list: str) -> str:
        """ Wraps the list of strings in a box for better representation """
        max_length = max([len(message) for message in message_list])
        final_message = ""
        for message in message_list: 
            final_message += f"| {message:<{max_length}} |\n"
            #  " |\n| ".join(message_list) + " |\n"
        final_message = final_message[:-1] # remove the last \n 
        print(f"| {'-'*max_length} |")
        print(final_message)
        print(f"| {'-'*max_length} |\n\n")

        return input(">> ") 


    
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

        # choice = self.message_wrapper(self.logged_menu_options)

        # # get the user option
        # # choice = input(">>> ") 
        # if choice == "1":
        #     self.add_order()
        # elif choice == "2":
        #     self.show_payment_methods()
        # elif choice == "3":
        #     self.show_previous_orders()
        # elif choice == "-1":
        #     return -1
        # else:
        #     print("Invalid option")
        
        options = [self.add_order, self.show_payment_methods, self.show_previous_orders]
        option_names = ["Add order", "Show payment methods", "Show previous orders"]
        self.options_loader(options, option_names)



    def options_loader(self, options: list, options_names: list ) -> None:
        """ Prints the options in a nice format """

        # Creates a list of the options to be displayed 
        option_choice = [ f"Press {i+1} to: {option}" for i, option in enumerate(options_names)]
        option_choice.append("Press -1 to: Exit")
        
        # Starts running the loop 
        while True: 
            # Prints the options and gets the user input
            choice = self.message_wrapper(option_choice)
            if choice == "-1":
                # This is exit 
                break
            elif choice in [str(i) for i in range(1,len(options)+1)]:
                # Runs the commands that were given 
                options[int(choice)-1]()
            else:
                print("Invalid option")

    def main(self) -> None:
        # constantly running the app looking for user option
        # Here I suggest a wrapper that will be runnign while loop and the options 
        # 
        # while True:
        #     self.option = self.message_wrapper(self.initial_menu_options)
        #     # self.option = input(">> ")
        #     if self.option == "1":
        #         self.login()
        #     elif self.option == "2":
        #         self.register()
        #     elif self.option == "-1":
        #         break
        #     else:
        #         print("Invalid option")


        options_to_load = [self.login, self.register]
        options_names = ["Login", "Register"]
        self.options_loader(options_to_load, options_names)

    def add_order(self): 
        pass 

    def show_payment_methods(self): 
        pass

    def show_previous_orders(self):
        pass

    

if __name__ == "__main__":
    database_path="Data/foodies.sqlite" 
    sql_path="ERD/sqlite.sql"
    app = Main(database_path, sql_path)


