#!/bin/python3
import sqlite3
from pathlib import Path
import bcrypt
import sys
import random
import datetime


def count(func):
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)

    wrapper.calls = 0
    return wrapper


class Foodies:
    def __init__(self, db_path, sqlfile):
        try:
            self.conn = sqlite3.connect(db_path)
            self.sqlfile = sqlfile
            self.salt = bcrypt.gensalt()

        except Exception as e:
            print(e)
            self.troubleshooting()
            sys.exit()
        self.folder = Path(__file__).parent
        self.root_folder = Path(self.folder).parent

    def troubleshooting(self):
        return input("Press enter to continue...")

    def hashing(self, password):
        return bcrypt.hashpw(password.encode(), self.salt)
        # possibly to become str

    def validate(self, password, hashed):
        return bcrypt.checkpw(password.encode(), hashed)

    def insert_data(self, table_name, data, columns=None):
        """data is the list of the values to be inserted into the table"""
        command = f"""INSERT INTO {table_name} """
        if columns:
            command += f"""({','.join(columns)})"""
        else:
            command += f"""({','.join(self.tables[table_name])})"""
        command += f""" VALUES ({','.join(['?' for i in range(len(data))])})"""

        try:
            # SQLIte function execute gets, will go and replace every ? with the corresponding value in the data list, automatically sanitizing the data.
            self.conn.execute(command, data)
            self.conn.commit()
        except Exception as e:
            print(e)
            print(command)
            print(data)
            self.troubleshooting()

    def update_data(self, table_name, data, conditions=None, columns=None):
        """Updates"""

        command = f"""UPDATE {table_name} SET """
        if not columns:
            columns = self.tables[table_name]

        command += f"""{','.join([f"{column} = ?" for column in columns])}"""

        command += f""" WHERE {' AND '.join([f"{condition[0]} = ?" for condition in conditions])}"""
        data.extend([condition[1] for condition in conditions])

        try:
            # SQLIte function execute gets, will go and replace every ? with the corresponding value in the data list, automatically sanitizing the data.
            self.conn.execute(command, data)
            self.conn.commit()
        except Exception as e:
            print(e)
            print(command)
            print(data)
            self.troubleshooting()

    def generate_db(self):
        # creat the database, calling forth the sql script and running it
        self.create_database()

        # fill the database with the data from the csv files
        self.fill_database()

    def opening_csv(self, file):
        """Opens the csv file and returns the columns and the data"""

        csv_columns = []
        data = []

        # open the csv file and read it line by line
        with open(file, "r") as file:
            for i, line in enumerate(file):
                if i == 0:
                    # only for the first line keep the column names that are stored
                    csv_columns = line.strip().split(",")
                    continue
                row_values = line.strip().split(",")
                rows_dictionary = {
                    column: word for column, word in zip(csv_columns, row_values)
                }
                data.append(rows_dictionary)

        return csv_columns, data

    def get_table_info(self):
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

    def create_database(self):
        """Runs the provided sql script to create the database"""

        sql = open(self.sqlfile, "r", encoding="utf-8-sig").read()
        # Sqlite function that executes all the commands in the script
        self.conn.executescript(sql)

        # can be used to get the names of all the tables automatically
        self.get_table_info()

    # ------------ Fillings --------------------------

    def fill_database(self):
        self.fill_database_customers()
        self.fill_database_restaurants()
        self.fill_database_categories()
        self.fill_database_deliveries()
        self.fill_database_dishes_and_belongs()
        # TODO
        self.fill_database_favourite()
        # # self.fill_database_changes()
        self.fill_database_OrderT()

    def fill_database_customers(self):
        """Fills the database with the data from the csv files"""

        #  -------------------  FILLING THE CUSTOMER TABLE -------------------

        customer_file = Path(self.root_folder, "Data", "customer.csv")

        csv_columns, customers = self.opening_csv(customer_file)

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
        del csv_columns

        #  -------------------  FILLING THE RESTAURANT TABLE -------------------

    def fill_database_restaurants(self):
        # point to the datapath of the csv
        restaurant_file = Path(self.root_folder, "Data", "restaurants.csv")
        csv_columns, restaurants = self.opening_csv(restaurant_file)

        for i in range(6):
            restaurant = restaurants[i]
            # get the columns of the restaurant table automatically instead of hardcoding them
            cols = self.tables["Store"]
            # create a list of the values of the customer dictionary based on the columns of the Customer table
            self.insert_data("Store", [restaurant[column] for column in cols])
        # del csv_columns
        # del restaurants
        del restaurant
        self.restaurants = restaurants
        self.restaurant_cols = csv_columns

    def fill_database_categories(self):
        csv_columns = self.restaurant_cols[-1]
        categories = set(restaurant[csv_columns] for restaurant in self.restaurants)
        for category in categories:
            self.insert_data("Category", [category])

        del self.restaurant_cols
        del self.restaurants
        del csv_columns
        del categories

    def fill_database_deliveries(self):
        # point to the datapath of the csv
        delivery_file = Path(self.root_folder, "Data", "deliveries.csv")
        csv_columns, deliveries = self.opening_csv(delivery_file)

        for delivery in deliveries:
            self.insert_data(
                "Delivery", [delivery[column] for column in self.tables["Delivery"]]
            )

        del csv_columns
        del deliveries

    def fill_database_dishes_and_belongs(self):
        # point to the datapath of the csv
        category_file = Path(self.root_folder, "Data", "dishes.csv")
        csv_columns, dishes = self.opening_csv(category_file)

        restaurants = self.select("SELECT storeId FROM Store")
        # open the csv file and read it line by line

        for dish in dishes:
            self.insert_data(
                "Belongs", [dish[column] for column in self.tables["Belongs"]]
            )

            dish["storeId"] = random.choice(restaurants)[0]
            self.insert_data("Dish", [dish[column] for column in self.tables["Dish"]])

        # Clean ram
        del csv_columns
        del dishes

    def fill_database_favourite(self):
        # find data of customer in database

        customers = self.select("SELECT * FROM Customer")[:5]
        # only 5 customers

        # find if the store is open
        stores = self.select("SELECT * FROM Store")[:6]

        for customer, store in zip(customers, stores):
            self.insert_data("Favourite", [store[0], customer[3]])

    def fill_database_OrderT(self):
        customer_id_list = self.select("SELECT accountId FROM Customer")
        customer_id_list = [customer[0] for customer in customer_id_list]

        # get the restaurant ids
        restaurant_ids = self.select("SELECT storeId FROM Store")
        restaurant_ids = [restaurant[0] for restaurant in restaurant_ids]

        self.restaurant_ids_used = []

        available_deliveries = self.select(
            "SELECT AFM FROM Delivery where availability = ?", ["true"]
        )
        available_deliveries = [delivery[0] for delivery in available_deliveries]

        for i in range(100):
            customer_id = random.choice(customer_id_list)
            restaurant_id = random.choice(restaurant_ids)

            dishes = self.select(
                "SELECT dishName FROM Dish WHERE storeId=?", [restaurant_id]
            )
            dishes = set(dish[0] for dish in dishes)
            dishes = list(dishes)

            order = self.createOrder(customer_id, restaurant_id, available_deliveries)

            # print(order)
            # insert the order into the database
            cols = self.tables["OrderT"]
            self.insert_data(
                "OrderT",
                [order[column] for column in cols if column in order],
                [column for column in cols if column in order],
            )

            # insert the dishes into the database
            order["orderId"] = self.conn.execute(
                "SELECT last_insert_rowid()"
            ).fetchone()[0]
            order["dishName"] = random.choice(dishes)
            order["quantity"] = random.randint(1, 5)

            self.insert_data(
                "Includes",
                [
                    order[column]
                    for column in self.tables["Includes"]
                    if column in order
                ],
                [column for column in self.tables["Includes"] if column in order],
            )

    #  -------------- Functions ---------------------------

    def createOrder(self, customer_id, restaurant_id, available_deliveries):
        order = {}
        order["accountId"] = customer_id
        order["storeId"] = restaurant_id

        order["deliveryAFM"] = random.choice(available_deliveries)
        # Here it should prob turn the delivery into not available but anywyayyys

        # Some random time in the day
        order["orderTime"] = datetime.time(
            random.randint(0, 23), random.randint(0, 59), random.randint(0, 59)
        )
        order["orderTime"] = order["orderTime"].strftime("%H:%M:%S")
        order["orderDate"] = datetime.date(
            2020, random.randint(1, 12), random.randint(1, 28)
        )
        order["orderDate"] = order["orderDate"].strftime("%Y-%m-%d")

        return order

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
            self.troubleshooting()
            # self.conn.commit()

        return bcrypt.checkpw(user_password.encode("utf-8"), hashed)

    def check_user(self, email):
        # check if the user is in the database
        # at the time testing the functionality with just one user
        query = "SELECT first_name FROM Customer WHERE email=?"
        try:
            cursor = self.conn.execute(query, [email])
            user = cursor.fetchone()
            if user:
                user = user[0]
            return user

        except Exception as e:
            print(e)
            print(query)
            print(email)
            self.troubleshooting()
            return None

    def add_user(self, user_email, user_password):
        """Adds a user to the database"""

        # hash the password
        hashed = self.hashing(user_password)

        # add the user to the database
        self.insert_data(
            "Customer", [user_email, hashed, self.salt], ["email", "password", "salt"]
        )

    def email_exists(self, user_email):
        """Checks database to see if email exists"""

        query = "SELECT first_name FROM Customer WHERE email=?"

        try:
            cursor = self.conn.execute(query, [user_email])
            user = cursor.fetchone()
            if user:
                return True
        except Exception as e:
            print(e)
            print(query)
            print(user_email)
            self.troubleshooting()
            sys.exit()
        return False

    def validate_password(self, user_mail, password):
        query = "SELECT password FROM Customer WHERE email=?"
        try:
            cursor = self.conn.execute(query, [user_mail])
            database_pass = cursor.fetchone()[0]
            return self.validate(password, database_pass)
        except Exception as e:
            print(e)
            print(query)
            print(user_mail)
            self.troubleshooting()

        return False

    def get_user(self, user_email):
        """Returns the user data"""

        query = "SELECT * FROM Customer WHERE email=?"
        try:
            cursor = self.conn.execute(query, [user_email])
            user = cursor.fetchone()
            return user
        except Exception as e:
            print(e)
            print(query)
            print(user_email)
            self.troubleshooting()
        return None

    def select(self, command, data=None):
        """Executes the given command and returns the results"""

        try:
            if data:
                cursor = self.conn.execute(command, data)
            else:
                cursor = self.conn.execute(command)
            return cursor.fetchall()
        except Exception as e:
            print(e)
            print(command)
            self.troubleshooting()
        return None


if __name__ == "__main__":
    # Datapaths of the files
    folder = Path(__file__).parent
    root_folder = Path(folder).parent
    database = Path(root_folder, "Data", "foodies.sqlite")
    sqlfile = Path(root_folder, "ERD", "schema.sql")
    init = Foodies(database, sqlfile)
    # generate the database only when running this file, so that it is not generated when importing the database class
    init.generate_db()
