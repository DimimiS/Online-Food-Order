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
        """ data is the list of the values to be inserted into the table"""
        command = f"""INSERT INTO {table_name}({','.join(self.tables[table_name])}) VALUES ({','.join(['?' for i in range(len(data))])})"""
        try: 
            self.conn.execute(command, data)
            self.conn.commit()
        except Exception as e:
            print(e)
            print(command)
            print(data)

    def generate_db(self):
        self.create_database()
        self.fill_database()

    def create_database(self):
        """ Runs the provided sql script to create the database """

        sql = open(self.sqlfile, 'r', encoding='utf-8-sig').read()
        # Sqlite function that executes all the commands in the script 
        self.conn.executescript(sql)

        # can be used to get back the columns of the tables 
        self.table_names = [table_name[0] for table_name in self.conn.execute(
            'SELECT name FROM sqlite_master WHERE type="table"').fetchall()]
        # print(self.table_names)

        self.tables = {table_name: [column[1] for column in self.conn.execute(
            f'PRAGMA table_info({table_name})')] for table_name in self.table_names}
        # print(self.tables)

    def fill_database(self):

        # Filling the Customers  

        customer_file = 'Data/customer.csv'
        csv_columns = []
        customers = []
        with open(customer_file,'r') as file: 
            for i,line in enumerate(file): 
                if i == 0: 
                    csv_columns = line.strip().split(',')
                    continue
                for j,word in enumerate(line.strip().split(',')): 
                    customers.append({})
                    customers[i-1][csv_columns[j]] = word

        # for customer in customers : 
        for i in range(5): 
            customer = customers[i]
            customer['password'] = self.hashing(customer['first_name'])
            customer['salt'] = self.salt
            cols = self.tables['Customer']
            self.insert_data("Customer", [customer[column] for column  in cols ])

        # Deleting the list 
        del customers
        del csv_columns 
        


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
    sqlfile = 'ERD/schema.sql'
    database = 'Data/foodies.sqlite'
    init = Foodies(database, sqlfile)
    init.generate_db()
    