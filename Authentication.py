from Database import Database
from Utils import generate_api_key
import sqlite3 as sq
import protobase_client as pc


class Auth(Database):
    def signup(self, username, password):
        api_key = generate_api_key()
        data = (username ,password, api_key)
        try:
            self.cur.execute("INSERT INTO Account VALUES (?,?,?)", data)
            self.con.commit()
            self.con.close()
            return {"success": True,"status":200, "message":"User SignedUp Successfully"}

        except sq.IntegrityError:
            return {"success": False,"status":302, "message":"Username already exists"}

    def login(self,username, password):
        usernames = self.user_data()

        if username in usernames and usernames[username] == password:
            self.con.close()
            return {"success": True,"status":200, "message":"User Logged in Successfully"}

        elif username in usernames and usernames[username] != password:
            return {"success": False,"status":302, "message":"Incorrect Credentials"}

        elif username not in usernames:
            return {"success": False,"status":302, "message":"Incorrect Credentials"}

        else:
            return {"success": False,"status":302, "message":"Something went wrong! Please Try Again"}



class ProtoAuth:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = pc.ProtoBaseClient()
    def login(self,username, password):
        response = self.client.signin_username(username, password, self.api_key)
        return response

    def signup(self, username, password):
        response = self.client.signup_username(username, password, self.api_key)
        return response