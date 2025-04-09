from MongoClient import AnarchKeyHelpers
from Utils import generate_api_key

class AnarchAuthentication(AnarchKeyHelpers):
    def signup(self, email, username, password):
        api_key = generate_api_key()
        usernames = self.get_all_users()
        emails = self.get_all_emails()
        print(emails)
        print(usernames)
        if username not in usernames and email not in emails:
            self.insert_new_user(email=email,
                                 username=username,
                                 password=password,
                                 api_key=api_key)

            return {"success": True,"status":200, "message":"User SignedUp Successfully"}
        elif username not in usernames and email in emails:
            return {"success": False,"status":302, "message":"Email already in use"}
        elif username in usernames and email not in emails:
            return {"success": False,"status":302, "message":"Username already exists"}
        else:
            return {"success": False,"status":302, "message":"Username already exists"}

    def login(self,username, password):
        info = self.get_user_info(username)
        if info:
            if info['username'] == username and self.decrypt(info['password_hash']) == password:
                return {"success": True,"status":200, "message":"User Logged in Successfully"}
            elif info['username'] == username and self.decrypt(info['password_hash']) != password:
                return {"success": False,"status":302, "message":"Incorrect Password"}
            else:
                return {"success": False,"status":302, "message":"Something went wrong! Please Try Again"}
        else:
            return {"success": False, "status": 302, "message": "Username Doesn't Exist"}


"""class ProtoAuth:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = pc.ProtoBaseClient()
    def login(self,username, password):
        response = self.client.signin_username(username, password, self.api_key)
        return response

    def signup(self, username, password):
        response = self.client.signup_username(username, password, self.api_key)
        return response"""

a = AnarchAuthentication()
