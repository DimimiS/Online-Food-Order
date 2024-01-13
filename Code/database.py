#!/bin/python3
import sqlite3
import bcrypt
import sys


def count(func):
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)

    wrapper.calls = 0
    return wrapper


class Foodies:
    def __init__(self, db_path, sqlfile):
        try:
            with open(db_path, "w"):
                pass
            self.conn = sqlite3.connect(db_path)
            self.sqlfile = sqlfile
            self.salt = bcrypt.gensalt()

        except Exception as e:
            print(e)
            sys.exit()

    def hashing(self, password):
        return bcrypt.hashpw(password.encode(), self.salt)
        # possibly to become str

    def validate(self, password, hashed):
        return bcrypt.checkpw(password.encode(), hashed)

    def insert_into(self, table, values):
        cur = self.conn.cursor()
        cur.execute(f"INSERT INTO {table} VALUES ({values})")
        # keep in mind that the values should be a string and not a tuple!!!!
        self.conn.commit()

    def insert_data(self, table_name, data):
        """data is the list of the values to be inserted into the table"""

        command = f"""INSERT INTO {table_name}({','.join(self.tables[table_name])}) VALUES ({','.join(['?' for i in range(len(data))])})"""
        try:
            # SQLIte function execute gets, will go and replace every ? with the corresponding value in the data list, automatically sanitizing the data.
            self.conn.execute(command, data)
            self.conn.commit()
        except Exception as e:
            print(e)
            print(command)
            print(data)

    def update_data(self, table_name, data, condition):
        """data is the list of the values to be inserted into the table"""

        command = f"""UPDATE {table_name} SET {','.join([f'{self.tables[table_name][i]}=?' for i in range(len(data))])} WHERE {condition}"""
        try:
            # SQLIte function execute gets, will go and replace every ? with the corresponding value in the data list, automatically sanitizing the data.
            self.conn.execute(command, data)
            self.conn.commit()
        except Exception as e:
            print(e)
            print(command)
            print(data)

    def delete_data(self, table_name, condition):
        """data is the list of the values to be inserted into the table"""

        command = f"""DELETE FROM {table_name} WHERE {condition}"""
        try:
            # SQLIte function execute gets, will go and replace every ? with the corresponding value in the data list, automatically sanitizing the data.
            self.conn.execute(command)
            self.conn.commit()
        except Exception as e:
            print(e)
            print(command)
            print(table_name)

    def generate_db(self):
        # creat the database, calling forth the sql script and running it
        self.create_database()

        # fill the database with the data from the csv files
        self.fill_database()

    def create_database(self):
        """Runs the provided sql script to create the database"""

        sql = open(self.sqlfile, "r", encoding="utf-8-sig").read()
        # Sqlite function that executes all the commands in the script
        self.conn.executescript(sql)

        # can be used to get the names of all the tables automatically
        self.table_names = [
            table_name[0]
            for table_name in self.conn.execute(
                'SELECT name FROM sqlite_master WHERE type="table"'
            ).fetchall()
        ]

        # used to get all the columns of every table automatically
        self.tables = {
            table_name: [
                column[1]
                for column in self.conn.execute(f"PRAGMA table_info({table_name})")
            ]
            for table_name in self.table_names
        }

    def fill_database(self):
        self.fill_database_customers()
        self.fill_database_restaurants()
        self.fill_database_categories()
        self.fill_database_dishes()
        self.createMockupOrders()

    def fill_database_customers(self):
        """Fills the database with the data from the csv files"""

        #  -------------------  FILLING THE CUSTOMER TABLE -------------------

        # point to the datapath of the csv
        customer_file = "Data/customer.csv"
        csv_columns = []
        customers = []

        # open the csv file and read it line by line
        with open(customer_file, "r") as file:
            for i, line in enumerate(file):
                if i == 0:
                    # only for the first line keep the column names that are stored
                    csv_columns = line.strip().split(",")
                    continue
                row_values = line.strip().split(",")
                customer = {}
                for j, word in enumerate(row_values):
                    # for every row, split the line by the comma and store the values in a dictionary, with keys as the column names and values the split values of the row
                    # append a dictionary
                    # customer.append({})
                    # to the last appended dictionary add the values based on the keys that have been given
                    customer[csv_columns[j]] = word
                customers.append(customer)

        # for customer in customers : Here I have only added 5 customers
        for i in range(5):
            customer = customers[i]
            # add the fields of password and salt
            customer["password"] = self.hashing(customer["first_name"])
            customer["salt"] = self.salt

            # get the columns of the Customer table automatically instead of hardcoding them
            cols = self.tables["Customer"]
            # create a list of the values of the customer dictionary based on the columns of the Customer table
            self.insert_data("Customer", [customer[column] for column in cols])

        # Deleting the lists to save on memory managing
        del customers
        del customer
        del csv_columns

        #  -------------------  FILLING THE RESTAURANT TABLE -------------------

    def fill_database_restaurants(self):
        # point to the datapath of the csv
        restaurant_file = "Data/restaurants.csv"
        csv_columns = []
        restaurants = []

        # open the csv file and read it line by line
        with open(restaurant_file, "r") as file:
            for i, line in enumerate(file):
                if i == 0:
                    # only for the first line keep the column names that are stored
                    csv_columns = line.strip().split(",")
                    continue
                row_values = line.strip().split(",")
                restaurant = {}
                for j, word in enumerate(row_values):
                    restaurant[csv_columns[j]] = word
                restaurants.append(restaurant)
        for i in range(5):
            restaurant = restaurants[i]
            # get the columns of the restaurant table automatically instead of hardcoding them
            cols = self.tables["Store"]
            # create a list of the values of the customer dictionary based on the columns of the Customer table
            self.insert_data("Store", [restaurant[column] for column in cols])
        del csv_columns
        del restaurants
        del restaurant

    def fill_database_categories(self):
        # point to the datapath of the csv
        category_file = "Data/restaurants.csv"
        csv_columns = []
        categories = []

        # open the csv file and read it line by line
        with open(category_file, "r") as file:
            for i, line in enumerate(file):
                if i == 0:
                    # only for the first line keep the column names that are stored
                    csv_columns = line.strip().split(",")

                    continue
                row_values = line.strip().split(",")
                category = {}
                # for j, word in enumerate(row_values):
                # for every row, split the line by the comma and store the values in a dictionary, with keys as the column names and values the split values of the row
                # append a dictionary
                # category.append({})
                # to the last appended dictionary add the values based on the keys that have been given
                category[csv_columns[-1]] = row_values[-1]
                categories.append(category)
                # category = categories[i]

                # create a list of the values of the customer dictionary based on the columns of the Customer table
                self.insert_data("Category", [category["category"]])

        del csv_columns
        del categories
        del category

    def fill_database_dishes(self):
        # point to the datapath of the csv
        category_file = "Data/dishes.csv"
        csv_columns = []
        dishes = []

        # open the csv file and read it line by line
        with open(category_file, "r") as file:
            for i, line in enumerate(file):
                if i == 0:
                    # only for the first line keep the column names that are stored
                    csv_columns = line.strip().split(",")

                    continue
                row_values = line.strip().split(",")
                dish = {}
                for j, word in enumerate(row_values):
                    dish[csv_columns[j]] = word
                # to the last appended dictionary add the values based on the keys that have been given
                dishes.append(dish)
                # category = categories[i]
                cols = self.tables["Dish"]

                # create a list of the values of the customer dictionary based on the columns of the Customer table
                self.insert_data("Dish", [dish[column] for column in cols])

        del csv_columns
        del dishes
        del dish

    @count
    def createOrder(self, customer_email, restaurant_id, dishes):  # , quantities):
        """Creates an order for the given customer id"""

        order = {}
        # find data of customer in database
        customer = self.conn.execute(
            "SELECT * FROM Customer WHERE email=?", [customer_email]
        ).fetchone()

        # find if the store is open
        store = self.conn.execute(
            "SELECT * FROM Store WHERE storeId=?", [restaurant_id]
        ).fetchone()

        # find if the dish is available
        for dishName in dishes:
            dish = self.conn.execute(
                "SELECT * FROM Dish WHERE dishName=?", [dishName[0]]
            ).fetchone()
            if dish[2] == "no":
                print("{dishName} not available")

        order["orderId"] = int(f"{customer[0]}{self.createOrder.calls}")
        order["comment"] = ""
        order["customerEmail"] = customer_email
        order["deliveryAFM"] = 123456789
        order["orderTime"] = "12:12:12"
        order["orderDate"] = "2020-12-12"
        order["rateTime"] = "12:12:13"
        order["rateText"] = ""
        order["rateScore"] = 5
        order["pickupTime"] = "12:12:12"
        order["exp_deliveryTime"] = "12:12:12"
        order["deliveryTime"] = "00:30:00"
        order["address"] = f"{customer[4]} {customer[5]}"

        # create the order
        # order = [
        #     customer_id,
        #     restaurant_id,
        #     ",".join(dishes),
        #     ",".join([str(quantity) for quantity in quantities]),
        # ]

        cols = self.tables["OrderT"]
        # insert the order into the database
        self.insert_data("OrderT", [order[column] for column in cols])

    def createMockupOrders(self):
        """Creates mockup orders for the database"""

        # get the customer ids
        # customer = (first_element,)
        # email = customer[0]
        customer_emails = [
            customer[0] for customer in self.conn.execute("SELECT email FROM Customer")
        ]
        # get the restaurant ids
        restaurant_ids = [
            restaurant[0]
            for restaurant in self.conn.execute("SELECT storeId FROM Store")
        ]

        # create 5 orders for each customer
        for customer_email, restaurant_id in zip(customer_emails, restaurant_ids):
            # get all dishes from the restaurant
            print(restaurant_id)
            dishes = [
                dish
                for dish in self.conn.execute(
                    "SELECT dishName FROM Dish WHERE storeId=?", [restaurant_id]
                )
            ]
            # create a random order
            self.createOrder(customer_email, restaurant_id, dishes)
            # insert the order into the database
            # self.insert_data("Order", order)

    def check_passwd(self, user_email, user_password):
        """Checks if the password is correct for the given email"""

        query = "SELECT password from Customer where email=?"
        try:
            cursor_password = self.conn.execute(query, [user_email])
            hashed = cursor_password.fetchone()[0]

        except Exception as e:
            print(e)
            print(query)
            print(user_email)

            # self.conn.commit()

        return bcrypt.checkpw(user_password.encode("utf-8"), hashed)

    def createMockupFavourites(self):
        """Creates mockup orders for the database"""

        # get the customer ids
        customer_ids = [
            customer[0] for customer in self.conn.execute("SELECT id FROM Customer")
        ]
        # get the restaurant ids
        restaurant_ids = [
            restaurant[0] for restaurant in self.conn.execute("SELECT id FROM Store")
        ]

        # create 5 orders for each customer
        for customer_id in customer_ids:
            for i in range(5):
                # create a random order
                order = self.createRandomFavourite(customer_id, restaurant_ids)
                # insert the order into the database
                self.insert_data("Favourite", order)

    def createRandomFavourite(self, customer_id, restaurant_ids):
        """Creates a random order for the given customer id"""

        from random import randint

        # create a random order
        order = [
            customer_id,
            restaurant_ids[randint(0, len(restaurant_ids) - 1)],
            randint(1, 5),
        ]
        return order


# def generate(script_path, db_path):
#     with sqlite3.connect(db_path) as conn:
#         with open(script_path, "r") as file:
#             sql = ""
#             for row in file:
#                 sql += row
#             sql = sql.split(";")
#         for query in sql:
#             cur = conn.cursor()
#             cur.execute(query)

if __name__ == "__main__":
    # Datapaths of the files
    sqlfile = "ERD/schema.sql"
    database = "Data/foodies.sqlite"
    init = Foodies(database, sqlfile)
    # generate the database only when running this file, so that it is not generated when importing the database class
    init.generate_db()
