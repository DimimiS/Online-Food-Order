import sqlite3
import bcrypt
from pathlib import Path


class USER:
    def __init__(self, file=None):
        self.conn = None
        if file:
            self.conn = sqlite3.connect(file)

    def check_user(self, email):
        # check if the user is in the database
        # at the time testing the functionality with just one user
        query = "SELECT first_name FROM Customer WHERE email=?"
        try:
            cursor = self.conn.execute(query, [email])

        except Exception as e:
            print(e)
            print(query)
            print(email)
            return None
        user = cursor.fetchone()[0]
        return user

    def check_passwd(self, user_email, user_password):
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


if __name__ == "__main__":
    folder = Path(__file__).parent
    root_folder = Path(folder).parent
    file = Path(root_folder, "Data", "foodies.sqlite")
    user = USER(file)
