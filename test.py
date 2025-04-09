from pymongo import MongoClient
from datetime import datetime
from cryptography.fernet import Fernet
import os

# --- SETUP ---

# Connect to MongoDB (change as needed)
client = MongoClient("mongodb://localhost:27017/")
db = client["AnarchKey"]

# Generate or load an encryption key (you'll want to store this securely!)
if not os.path.exists("secret.key"):
    with open("secret.key", "wb") as f:
        f.write(Fernet.generate_key())
with open("secret.key", "rb") as f:
    key = f.read()
fernet = Fernet(key)

# --- INSERT USER ---

user = {
    "email": "dev@example.com",
    "username": "technoblade_dev",
    "password_hash": "hashed_pw_here",  # use bcrypt in real app
    "created_at": datetime.utcnow()
}
user_id = db.users.insert_one(user).inserted_id

# --- CREATE PROJECT ---

project = {
    "user_id": user_id,
    "name": "QuickTalk",
    "description": "Secure keys for QuickTalk backend",
    "created_at": datetime.utcnow()
}
project_id = db.projects.insert_one(project).inserted_id

# --- STORE API KEY ---

raw_key = "sk-test-openai-secret-key"
encrypted_key = fernet.encrypt(raw_key.encode()).decode()

api_key_doc = {
    "project_id": project_id,
    "name": "OpenAI Key",
    "encrypted_key": encrypted_key,
    "created_at": datetime.utcnow(),
    "last_used": None
}
key_id = db.api_keys.insert_one(api_key_doc).inserted_id

# --- LOG ACCESS ---

log = {
    "key_id": key_id,
    "user_id": user_id,
    "action": "create",
    "timestamp": datetime.utcnow(),
    "ip_address": "127.0.0.1",
    "user_agent": "AnarchKey CLI/0.1"
}
db.logs.insert_one(log)

print("✅ User, project, key, and log inserted successfully.")
