from pymongo import MongoClient
from cryptography.fernet import Fernet
import os
import datetime


class AnarchKeyDB:
    def __init__(self):
        if not os.path.exists("secret.key"):
            with open("secret.key", "wb") as f:
                f.write(Fernet.generate_key())
        with open("secret.key", "rb") as f:
            key = f.read()
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["AnarchKey"]
        self.key = key
        self.fernet = Fernet(key)

    def get_user_id(self, username):
        users = self.db.users.find_one({"username": username}, {"_ id": 1})
        return users["_id"] if users else None

    def get_project_id(self, project_name):
        projects = self.db.projects.find_one({"project_name": project_name}, {"_id": 1, "user_id": 1})
        return projects["_id"] if projects else None

    def get_api_key_id(self, project_id):
        api_keys = self.db.api_keys.find_one({"project_id": project_id}, {"_id": 1})
        return api_keys["_id"] if api_keys else None


class KeyEncryptor(AnarchKeyDB):
    def encrypt(self, data):
        return self.fernet.encrypt(data.encode()).decode()

    def decrypt(self, encrypted_data):
        return self.fernet.decrypt(encrypted_data.encode()).decode()


class AnarchKeyService(KeyEncryptor):
    def insert_new_user(self, email, username, password, api_key):
        user = {
            "email": email,
            "username": username,
            "password_hash": self.encrypt(password),
            "created_at": datetime.datetime.now(),
            "API_KEY": api_key
        }
        self.db.users.insert_one(user)

    def insert_new_project(self, project_name, username, description):
        project = {
            "user_id": self.get_user_id(username),
            "project_name": project_name,
            "description": description,
            "created_at": datetime.datetime.now()
        }
        self.db.projects.insert_one(project)

    def insert_new_api_key(self, project_name, raw_key):
        encrypted_key = self.encrypt(raw_key)
        api_key_doc = {
            "project_id": self.get_project_id(project_name),
            "project_name": project_name,
            "encrypted_key": encrypted_key,
            "created_at": datetime.datetime.now(),
            "last_used": None,
            "uses": 0
        }
        self.db.api_keys.insert_one(api_key_doc)

    def get_api_key(self, project_name):
        project_id = self.get_project_id(project_name)
        if not project_id:
            return None
        self.db.api_keys.update_one(
            {"project_id": project_id},
            {"$inc": {"uses": 1}}
        )
        api_keys = self.db.api_keys.find_one({"project_id": project_id}, {"encrypted_key": 1})
        x = api_keys["encrypted_key"] if api_keys else None
        return self.decrypt(x) if x else None


class AnarchKeyHelpers(AnarchKeyService):
    def get_user_info(self, username):
        try:
            return self.db.users.find_one({"username": username},
                                          {"_id": 0,
                                           "email": 1,
                                           "username": 1,
                                           "password_hash": 1,
                                           "API_KEY":1})
        except Exception as e:
            return None

    def get_all_users(self):
        return [i['username'] for i in list(self.db.users.find({}, {"_id": 0, "username": 1}))]

    def get_all_emails(self):
        return [i['email'] for i in list(self.db.users.find({}, {"_id": 0, "email": 1}))]

    def get_all_projects(self):
        return list(self.db.projects.find({}, {"_id": 0}))

    def get_all_api_keys(self):
        return list(self.db.api_keys.find({}, {"_id": 0}))

class AnarchKeyAPI(AnarchKeyHelpers):
    def __init__(self, usr, pwd, akey):
        super().__init__()
        self.username = usr
        self.password = pwd
        self.api_key = akey

    def auth_developer(self):
        info = self.get_user_info(self.username)
        print(info)
        print(self.username, self.password, self.api_key)
        if info:
            if info['username'] == self.username and self.decrypt(info['password_hash']) == self.password and info[
                'API_KEY'] == self.api_key:
                return {"success": True, "status": 200, "message": "User Logged in Successfully"}
            elif info['username'] == self.username and self.decrypt(info['password_hash']) != self.password:
                return {"success": False, "status": 302, "message": "Incorrect Password"}
            elif info['username'] == self.username and info['API_KEY'] != self.api_key:
                return {"success": False, "status": 302, "message": "Incorrect API Key"}
            else:
                return {"success": False, "status": 302, "message": "Something went wrong! Please Try Again"}
        else:
            return {"success": False, "status": 302, "message": "Username Doesn't Exist"}

    def retrieve_api_key(self, project_name, username):
        if not self.auth_developer()["success"]:
            return None
        usernames = self.get_all_users()
        if username not in usernames:
            return None
        try:
            api_key = self.get_api_key(project_name)
            if api_key:
                return api_key
            else:
                return None
        except Exception as e:
            return None

