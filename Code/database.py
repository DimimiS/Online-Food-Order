#!/bin/python3
import sqlite3
import bcrypt
import sys


class Foodies:
    def __init__(self, db_path, sqlfile):
        try:
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
