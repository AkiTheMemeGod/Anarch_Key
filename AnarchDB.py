import sqlite3 as sq
import os
from cryptography.fernet import Fernet
from datetime import datetime

class AnarchDB:
    def __init__(self):
        self.con = sq.connect('AnarchKey.db')
        self.cur = self.con.cursor()
        if not os.path.exists("secret.key"):
            with open("secret.key", "wb") as f:
                f.write(Fernet.generate_key())
        with open("secret.key", "rb") as f:
            key = f.read()
        self.key = key
        self.fernet = Fernet(key)
        self.path = os.path.dirname(__file__)

    def get_user_service_key(self, username):
        self.cur.execute("SELECT API_KEY FROM USERS WHERE username = ?", (username,))
        return self.cur.fetchone()[0]
class AnarchCrypt(AnarchDB):
    def encrypt(self, data):
        return self.fernet.encrypt(data.encode()).decode()

    def decrypt(self, encrypted_data):
        return self.fernet.decrypt(encrypted_data.encode()).decode()

class AnarchKeyService(AnarchCrypt):
    def insert_new_user(self, email, username, password, api_key):
        try:
            self.cur.execute("INSERT INTO USERS (email, username, hash_pwd, created_at, API_KEY) VALUES (?, ?, ?, ?, ?)",
                             (email, username, self.encrypt(password), datetime.now(), api_key))
            self.con.commit()
            return {"success": True, "status": 200, "message": "User SignedUp Successfully"}
        except sq.IntegrityError:
            return {"success": False, "status": 302, "message": "Username already exists"}

    def insert_new_project(self, project_name, username, description):
        try:
            self.cur.execute("INSERT INTO PROJECTS (username, project_name, description, created_at) VALUES (?, ?, ?, ?)",
                             (username, project_name, description, datetime.now()))
            self.con.commit()
            return {"success": True, "status": 200, "message": "Project Created Successfully"}
        except sq.IntegrityError:
            return {"success": False, "status": 302, "message": "Project already exists"}

    def insert_new_api_key(self, project_name, raw_key):
        encrypted_key = self.encrypt(raw_key)
        try:
            self.cur.execute("INSERT INTO APIKEYS VALUES (?, ?, ?, ?, ?)",
                             (project_name, encrypted_key, datetime.now(), "--:--:--", 0))
            self.con.commit()
            return {"success": True, "status": 200, "message": "API Key Created Successfully"}
        except Exception as e:
            return {"success": False, "status": 302, "message": str(e)}

    def get_api_key(self, project_name):
        try:
            self.cur.execute("UPDATE API_KEYS SET uses = uses + 1, last_used = ? WHERE project_name=?",
                             (datetime.now(),project_name,))
            self.cur.execute("SELECT api_key FROM APIKEYS WHERE project_name=?",
                             (project_name,))
            result = self.cur.fetchone()
            if result:
                return {"success": True, "status": 200, "api_key": self.decrypt(result[0])}
            else:
                return {"success": False, "status": 302, "message": "API Key not found"}
        except Exception as e:
            return {"success": False, "status": 302, "message": str(e)}

class AnarchAPI(AnarchKeyService):
    def validate_user_api_key(self,api_key, username):
        self.cur.execute("SELECT * FROM USERS WHERE API_KEY=? AND username=?", (api_key, username,))
        result = self.cur.fetchone()
        if result:
            return {"success": True, "status": 200, "message": "API Key Validated Successfully"}

        else:
            return {"success": False, "status": 401, "message": "API Key Validation Failed"}

    def retrieve_api_key(self, project_name, username, api_key):
        if not self.validate_user_api_key(api_key, username)["success"]:
            return {"success": False, "status": 401, "message": "API Key Validation Failed"}
        self.cur.execute("UPDATE APIKEYS SET uses = uses + 1, last_used = ? WHERE project_name=?",
                         (datetime.now(), project_name,))
        self.con.commit()
        self.cur.execute("SELECT * FROM APIKEYS WHERE project_name=?", (project_name,))

        result = self.cur.fetchone()
        if result:
            return {"success": True, "status": 200, "api_key": self.decrypt(result[1])}
        else:
            return {"success": False, "status": 401, "message": "API Key Retrieval Failed"}
