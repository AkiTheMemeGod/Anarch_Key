from Utils import generate_api_key
from AnarchDB import AnarchKeyService
from datetime import datetime

class AnarchKeyAuth(AnarchKeyService):

    def signup(self,email, username, password):
        api_key = generate_api_key()
        response = self.insert_new_user(email, username ,password, api_key)
        return response

    def login(self,username, password):
        self.cur.execute("SELECT hash_pwd FROM USERS WHERE username=?", (username,))
        result = self.cur.fetchone()

        if result:
            hash_pwd = result[0]
            decrypted_pwd = self.decrypt(hash_pwd)
            if decrypted_pwd == password:
                return {"success": True, "status": 200, "message": "Login Successful"}
            else:
                return {"success": False, "status": 401, "message": "Invalid Password"}
        else:
            return {"success": False, "status": 404, "message": "User Not Found"}


