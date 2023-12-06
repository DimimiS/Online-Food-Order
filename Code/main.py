import input_utils as iu

class Main:
    def __init__(self):
        # constantly running the app looking for user ption
        while True:
            self.option = self.menu()
            if self.option == "1":
                self.login()
            elif self.option == "2":
                self.register()
            elif self.option == "-1":
                break
            else:
                print("Invalid option")

    def menu(self) -> None:
        # print the menu 
        print("Press 1 to: Login")
        print("Press 2 to: Register")
        print("Press -1 to: Exit")

        # get the user option
        return input()
    
    def login(self) -> None:
        # get the user email and password
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        # check if the user is in the database 
        # at the time testing the functionality with just one user
        if email == "admin" and password == "admin":
            self.logged_menu()
        else:
            print("Invalid email or password")

    def register(self) -> None:
        # get the user email and password
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        # check if the user is in the database 
        # if not in the databse, add the user to the database 
        self.logged_menu()

    def logged_menu(self) -> None :
        # print the menu 
        print("Press 1 to: Add a new order")
        print("Press 2 to: Show payment methods")
        print("Press 3 to: Show previous orders")
        print("Press -1 to: Exit")

        # get the user option
        choice = input()
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


if __name__ == "__main__":
    Main()


