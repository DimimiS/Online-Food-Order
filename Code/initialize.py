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
        

    def generate_db(self):
        pass 
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
    init = Foodies("foodies.db", "sqlite.sql")
    init.generate_db()
    