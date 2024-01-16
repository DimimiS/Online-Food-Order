from cli_application import Main
from database import Foodies
from pathlib import Path
import datetime


class FoodiesMain(Main):
    def __init__(self, database_path, sql_path):
        # Call the initilizations of the Main Class
        super().__init__()
        # Connect the database
        self.db = Foodies(database_path, sql_path)
        self.db.get_table_info()
        # Set the name
        self.application_name = "Foodies"
        self.menu_presenting = False

    # ------------------ Main Functions ------------------

    def main(self):
        self.main_menu()

    # ------------------ Action Functions ------------------

    def login_action(self, email=None, password=None, clearing=True) -> None:
        if clearing:
            self.clear_screen()

        message = self.message_wrapper(["Login:"])
        print(message)

        # get the user email and password
        if not email:
            email = self.check_input("Enter your email: ")
            if not self.db.email_exists(email):
                self.notification_message = "Email does not exist"
                self.notify()
                choiceToLoginOrRegister = self.check_input(
                    "The mail you entered does not exist. Do you want to try again (0) or register (1) ? "
                )
                if choiceToLoginOrRegister == "0" or choiceToLoginOrRegister == "login":
                    return self.login_action()
                elif (
                    choiceToLoginOrRegister == "1"
                    or choiceToLoginOrRegister == "register"
                ):
                    return self.register_action(False)
                else:
                    return self.main_menu()
            else:
                if not password:
                    password = self.check_input("Enter your password: ")
                    valid = self.db.validate_password(email, password)
                    if valid:
                        self.notification_message = "Logged In Successfully"
                        self.username = self.db.get_user(email)[1]
                        self.user_id = self.db.get_user(email)[0]
                        return self.logged_in_menu()
                    else:
                        self.notification_message = "Invalid email or password"
                        # return self.login_action()

    def register_action(self, clearing=True) -> None:
        if clearing:
            self.clear_screen()
        message = self.message_wrapper(["Register:"])
        print(message)

        # get the user email and password
        email = self.check_input("Enter your email: ")

        # Check if the email is valid. If it exists it will return True
        if email in ["", "\n"]:
            self.notification_message = "Invalid email"
            # print("Invalid email")
            return
        if not self.db.email_exists(email):
            # If the email does not exist, then register the user
            password = self.check_input("Enter your password: ")
            check_password = self.check_input("Confirm your password: ")
            if password == check_password:
                self.db.add_user(email, password)
                # if self.register_info(email):
                self.register_info(email)
                return self.logged_in_menu()
            else:  # if the passwords do not match
                self.notification_message = "Passwords do not match"
                # print("Passwords do not match")

        else:
            self.notification_message = "Email already exists. Please Login"
            # If the email exists, then run the login action but have the email set
            self.login_action(email=email)

    def register_info(self, email=None) -> None:
        # self.notification_message = "Input your relevant information"
        if not email:
            email = self.check_input("Enter your email: ")
        fname = self.check_input("Enter your first name: ")
        lname = self.check_input("Enter your last name: ")
        # phone = self.check_input("Enter your phone number: ")
        address = self.check_input("Enter your address Name Number: ")
        address = address.split()
        address_condition = lambda x: not (
            len(x) == 2 and x[0].isalpha() and x[-1].isdigit()
        )

        if address_condition(address):
            self.notification_message = "Invalid address"
            return
        addressName = address[0].capitalize()
        addressNumber = address[-1]
        floor = self.check_input("Enter your floor: ")
        if not floor.isdigit():
            self.notification_message = "Invalid floor"
            return False

        self.db.update_data(
            table_name="Customer",
            columns=["first_name", "last_name", "address", "address_number", "floor"],
            data=[fname, lname, addressName, addressNumber, floor],
            conditions=[("email", email)],
        )

        return True

    def log_out_action(self) -> None:
        print("\n")
        self.main_menu()

    def search_restaurants(self) -> None:
        # SQL command to get all the stores, future implementation will be able to discern the hours that each is open
        all_restaurants = self.db.select(
            """
            SELECT DISTINCT storeId,name
            FROM Store
            """
        )
        # Turn it into a dictionary for ease of usage
        all_restaurants = {
            restaurant[1]: restaurant[0] for restaurant in all_restaurants
        }

        # Classic way of handling options
        options_names = list(all_restaurants.keys())

        option_title = "Choose a restaurant"

        # Create a list of lambda functions that go to the next menu without needing to pass arguments
        option_functions = []
        for restaurant in options_names:

            def lambda_function(restaurant=restaurant):
                # Globally dictionary for storing information about the order
                self.order_information_d["storeId"] = all_restaurants[restaurant]

                # Next menu option
                self.choose_dish_menu(all_restaurants[restaurant])

            option_functions.append(lambda_function)

        return option_functions, options_names, option_title

    # ----------------------- Menus ------------------------

    def main_menu(self) -> None:
        # constantly running the app looking for user option
        # Here I suggest a wrapper that will be runnign while loop and the options

        option_functions = [
            self.login_action,
            self.register_action,
        ]
        option_names = ["Login", "Register"]
        option_title = "Main Menu"
        self.options_loader(option_functions, option_names, menu_title=option_title)

    def logged_in_menu(self) -> None:
        option_functions = [
            self.search_menu,
            self.order_menu,
            self.register_info,
            self.add_favourite,
            # self.show_previous_orders,
            self.log_out_action,
        ]
        option_names = [
            "Search Menu",
            "Order Menu",
            "Update Registered Information",
            "Add Favourite",
            # "Show previous orders",
            "Log out",
        ]

        option_title = "Logged In "
        if self.username:
            option_title += "as " + f"{self.username}".capitalize()

        self.options_loader(option_functions, option_names, menu_title=option_title)

    def order_menu(self) -> None:
        option_functions = [
            self.add_order,
            self.show_previous_orders,
            # self.add_favourite,
            self.rate_last_order,
            self.logged_in_menu,
        ]
        option_names = [
            # "Search for Restaurants",
            "Add order",
            "Show previous orders",
            # "Add Favourite",
            "Rate Last Order",
            "Exit to User Menu",
        ]

        option_title = "Order Menu"

        self.options_loader(option_functions, option_names, menu_title=option_title)

    def search_menu(self) -> None:
        option_functions = [
            self.search_restaurants_working_hours,
            self.search_dishes,
            self.search_categories,
            self.search_favourites,
            self.show_restaurant_ratings,
            self.logged_in_menu,
        ]
        option_names = [
            "Search for Restaurants",
            "Search for Dishes",
            "Search for Categories",
            "Show Favourites",
            "Show Restaurant Ratings",
            "Exit to User Menu",
        ]

        option_title = "Search Menu"

        self.options_loader(
            option_functions,
            option_names,
            menu_title=option_title,
        )

    # ------------------ Other Functions -------------------

    def search_restaurants_working_hours(self):
        all_restaurants = self.db.select("SELECT storeId,name,workHours FROM Store")
        # all_restaurants = [ [restaurant[0],restaurant[1]] for restaurant in all_restaurants]

        for restaurant in all_restaurants:
            workingHours = self.working_hours_computator(restaurant)
            print(restaurant[0])
            print(workingHours)

        self.check_input("Press Enter to continue")

    def working_hours_computator(self, restaurant):
        workingHours = {}
        for day in restaurant[2].split("] "):
            day += "]"
            day = day.split(": ")
            if day[1] not in ["Kleista", "Anoichto olo to 24oro"]:
                start, end = day[1].strip("[]").split("-")
                # Turn the time from h:m p.m. to military time
                start = datetime.datetime.strptime(start, "%I:%M%p").strftime("%H:%M")
                end = datetime.datetime.strptime(end, "%I:%M%p").strftime("%H:%M")

                workingHours[day[0]] = [start, end]
        return workingHours

    def search_dishes(self):
        all_restaurants = self.db.select(
            """
            SELECT DISTINCT s.storeId,s.name,s.workHours
            FROM Store as s, Includes as i
            WHERE s.storeId = i.storeId and i.dishName = ?
            """,
            [self.check_input("Enter the dish name: ")],
        )
        # all_restaurants = [ [restaurant[0],restaurant[1]] for restaurant in all_restaurants]
        if not all_restaurants:
            self.notification_message = "No restaurants found"
        else:
            for restaurant in all_restaurants:
                workingHours = self.working_hours_computator(restaurant)
                print(restaurant[0])
                print(workingHours)

        self.check_input("Press Enter to continue")

    def search_categories(self):
        all_restaurants = self.db.select(
            """
            SELECT DISTINCT s.storeId,s.name,s.workHours
            FROM Store as s, Includes as i,Belongs as b
            WHERE s.storeId = i.storeId and i.dishName = b.dishName and b.category=?
            """,
            [self.check_input("Enter the category: ")],
        )
        # all_restaurants = [ [restaurant[0],restaurant[1]] for restaurant in all_restaurants]
        if not all_restaurants:
            self.notification_message = "No restaurants found"
        else:
            for restaurant in all_restaurants:
                workingHours = self.working_hours_computator(restaurant)
                print(restaurant[0])
                print(workingHours)

        self.check_input("Press Enter to continue")

    def search_favourites(self):
        all_restaurants = self.db.select(
            """
            SELECT DISTINCT storeId,name,workHours
            FROM Store NATURAL JOIN Favourite
            WHERE email = ?
            """,
            [self.username],
        )
        # all_restaurants = [ [restaurant[0],restaurant[1]] for restaurant in all_restaurants]
        if not all_restaurants:
            self.notification_message = "No restaurants found"
        else:
            for restaurant in all_restaurants:
                workingHours = self.working_hours_computator(restaurant)
                print(restaurant[0])
                print(workingHours)

        self.check_input("Press Enter to continue")

    def add_favourite(self):
        storeId = self.check_input("Enter the storeId: ")
        self.db.insert_data(
            "Favourite",
            [storeId, self.username],
        )
        all_restaurants = self.db.select(
            """
            SELECT DISTINCT storeId,name,workHours
            FROM Store NATURAL JOIN Favourite
            WHERE email = ?
            """,
            [self.username],
        )
        # all_restaurants = [ [restaurant[0],restaurant[1]] for restaurant in all_restaurants]
        if not all_restaurants:
            self.notification_message = "No restaurants found"
        else:
            for restaurant in all_restaurants:
                workingHours = self.working_hours_computator(restaurant)
                print(restaurant[0])
                print(workingHours)

        self.check_input("Press Enter to continue")

    def rate_last_order(self):
        order = self.db.select(
            """SELECT orderId
            From OrderT
            Where accountId = ?""",
            [self.user_id],
        )
        if not order:
            self.notification_message = "No orders found"
            return
        else:
            latest_order = order[::-1][0]
            self.show_order(latest_order[0])
            rateTime = datetime.datetime.now().strftime("%H-%M-%S")
            rateText = self.check_input("Enter your comment for this rating: ")
            rating = self.check_input("Enter your rating Score: ")
            if not rating.isdigit():
                self.notification_message = "Invalid rating"
                return
            else:
                rating = float(rating[:3])
            self.db.update_data(
                table_name="OrderT",
                columns=[
                    "rateTime",
                    "rateText",
                    "rateScore",
                ],
                data=[rateTime, rateText, rating],
                conditions=[("orderId", latest_order[0])],
            )

    def show_restaurant_ratings(self):
        storeId = self.check_input("Enter the storeId: ")
        if not self.check_restaurant(storeId):
            # self.notification_message("Restaurant not found")
            return

        ratings = self.db.select(
            """
            Select AVG(rateScore),COUNT(rateScore)
            FROM OrderT NATURAL JOIN Includes
            WHERE storeId = ? and rateScore is not null            
            """,
            [storeId],
        )
        if not ratings:
            self.notification_message = "No ratings found"
            return
        else:
            ratings = ratings[0]
            message = self.message_wrapper(
                [f"Rating Score: {ratings[0]}", f"Rating Count: {ratings[1]}"]
            )
            print(message)
        self.check_input("Press Enter to continue")

    def choose_restaurant(self):
        option_functions, options_names, option_title = self.search_restaurants()

        # Much needed button
        options_names.append("Return to previous menu")
        # Unfortunately the order is manually implemented, future implementations can be
        option_functions.append(self.order_menu)

        self.options_loader(
            option_functions, options_names, menu_title=option_title, simple=True
        )

    def choose_dish_menu(self, storeId):
        self.menu_presenting = True

        options_functions, options_names, option_title = self.show_dishes(storeId)

        options_names.append("Place order")
        options_functions.append(self.place_order)

        options_names.append("Return to previous menu")
        options_functions.append(self.add_order)

        options_names.append("Return to main menu")
        options_functions.append(self.main_menu)

        self.options_loader(
            options_functions,
            options_names,
            menu_title=option_title,
            simple=True,
            persistent=self.menu_presenting,
        )

    def show_dishes(self, storeId):
        all_dishes = self.db.select(
            """
            SELECT DISTINCT dishName,price
            FROM Dish 
            WHERE storeId = ? and availability='yes'
            """,
            [storeId],
        )

        # Change it to display the prices for each dish as well
        all_dishes = {
            f"{dish[0]}, {dish[1]} €": [dish[0], dish[1]] for dish in all_dishes
        }
        options_names = list(all_dishes.keys())
        option_title = "Choose a dish"

        option_functions = []
        for key in options_names:

            def lambda_function(dish=key):
                self.choose_dish_quantity(all_dishes[dish][0], all_dishes[dish][1])

            option_functions.append(lambda_function)

        return option_functions, options_names, option_title

    def place_order(self):
        # Check if the order is empty
        if not self.order_information_d["orderList"]:
            self.notification_message = "Order is empty"
            return
        # Insert the order
        # Select the last orderId
        # Insert includes

        # Find available Delivery
        # Insert the order
        self.db.insert_data(
            "OrderT",
            [
                self.order_information_d["accountId"],
                datetime.datetime.now().strftime("%Y-%m-%d"),
                datetime.datetime.now().strftime("%H:%M:%S"),
            ],
            columns=["accountId", "orderDate", "orderTime"],
        )

        # Select the last orderId
        orderId = self.db.select(
            "SELECT orderId FROM OrderT ORDER BY orderId DESC LIMIT 1"
        )[0][0]

        # Insert includes
        for dish in self.order_information_d["orderList"]:
            self.db.insert_data(
                "Includes",
                [
                    orderId,
                    self.order_information_d["storeId"],
                    dish["dishName"][0],
                    dish["dishName"][2],
                ],
            )

        # Show the order
        self.show_order(orderId)
        self.check_input("Press Enter to continue")

        return self.logged_in_menu()

    def choose_dish_quantity(self, dishName, price):
        print(self.message_wrapper([f"Choose quantity for {dishName}"]))
        quantity = self.check_input("Enter the quantity: ")

        self.order_information_d["orderList"].append(
            {"dishName": [dishName, price, quantity]}
        )

        order_basket = [
            f"{dish['dishName'][0]} x {dish['dishName'][2]} = {float(dish['dishName'][1])*float(dish['dishName'][2])}"
            for dish in self.order_information_d["orderList"]
        ]

        self.notification_message = order_basket
        self.menu_presenting = True

    def add_order(self):
        # storeId = self.check_input("Enter the storeId: ")
        # if not self.check_restaurant(storeId):
        #     return
        # self.show_restaurant_menu(storeId)
        # self.check_input("Press Enter to continue")
        self.order_information_d = {"orderList": []}

        if self.username:
            self.order_information_d["accountId"] = self.user_id

        storeId = self.choose_restaurant()
        self.order_information_d["storeId"] = storeId
        self.check_input("Press Enter to continue")

    def check_restaurant(self, storeId):
        restaurant = self.db.select(
            "SELECT storeId FROM Store WHERE storeId = ?", [storeId]
        )
        if not restaurant:
            self.notification_message = "Restaurant not found"
            return False
        else:
            return True

    def show_restaurant_menu(self, storeId):
        menu = self.db.select(
            """
            SELECT DISTINCT dishName,price
            FROM Dish NATURAL JOIN Includes
            WHERE storeId = ?
            """,
            [storeId],
        )
        if not menu:
            self.notification_message = "No menu found"
            return
        else:
            print(self.message_wrapper([f"Menu for {storeId}"]))
            dishes = []
            for dish in menu:
                dishes.append(f"Dish {dish[0]}")
                dishes.append(f"Dish {dish[1]}")
            print(self.message_wrapper(dishes), columns=2)

    def show_previous_orders(self):
        orders = self.db.select(
            "SELECT orderId, Customer.accountId from OrderT join Customer on Customer.accountId = OrderT.accountId where Customer.accountId = ?",
            (self.user_id,),
        )
        if not orders:
            self.notification_message = "No orders found"
            return
        else:
            latest_orders = orders[::-1][:3]
            for order in latest_orders:
                self.show_order(order[0])
                self.check_input("Press Enter to continue")

    def show_order(self, orderId):
        orderItems = self.db.select(
            "SELECT * FROM OrderT WHERE orderId = ?", [orderId]
        )[0]

        dishPricesAndQuantities = self.db.select(
            "SELECT dishName,price,quantity,orderID FROM Dish NATURAL JOIN Includes WHERE orderId = ?",
            [orderId],
        )
        cost = sum([x[2] * x[1] for x in dishPricesAndQuantities])

        message = self.message_wrapper(
            [
                f"Order Id: {orderItems[0]}",
                f"Order Date: {orderItems[5]}" if orderItems[5] else "Order Date: None",
                f"Order Time: {orderItems[4]}" if orderItems[4] else "Order Time: None",
                f"Order Total: {cost}" if cost else "Order Total: None",
            ]
        )
        print(message)

        for dish in dishPricesAndQuantities:
            message = self.message_wrapper(
                [
                    f"Dish Name: {dish[0]}",
                    f"Dish Price: {dish[1]}",
                    f"Dish Quantity: {dish[2]}",
                ]
            )
            print(message)
        # self.check_input("Press Enter to continue")


if __name__ == "__main__":
    folder = Path(__file__).parent
    root_folder = Path(folder).parent
    database_path = Path(root_folder, "Data", "foodies.sqlite")
    sql_path = Path(root_folder, "ERD", "sqlite.sql")

    app = FoodiesMain(database_path, sql_path)
    app.main()
