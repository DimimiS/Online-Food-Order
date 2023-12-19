
import sqlite3
import bcrypt

class USER: 
    def __init__(self,file):
        self.conn = sqlite3.connect(file)

    def check_user(self,email,password):
        # check if the user is in the database 
        # at the time testing the functionality with just one user
        pass 

    def check_passwd(self, user_email, user_password):
        query = "SELECT password from Customer where id={}".format(user_email)
        cursor_password = self.conn.execute(query)

        hashed = cursor_password.fetchone()[0].encode('utf-8')
        
        return bcrypt.checkpw(user_password.encode('utf-8'), hashed)



if __name__ == "__main__" : 
    file = 'Data/foodies.sqlite'
    user = USER(file)
