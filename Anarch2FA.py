import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random as rd
from cred import *
import sqlite3 as sq
SENDER_EMAIL = SENDER_EMAIL
SENDER_PASSWORD =SENDER_PASSWORD

class Anarch2FA:
    def __init__(self):
        self.path = os.path.dirname(__file__)
        self.con = sq.connect(f"{self.path}/AnarchKey.db")
        self.cur = self.con.cursor()
    @staticmethod
    def generate_otp():
        otp = rd.randint(100000, 999999)
        return otp

    def duplicate_email_check(self, email):
        self.cur.execute("SELECT * FROM USERS WHERE email=?", (email,))
        result = self.cur.fetchone()
        if result:
            return True
        else:
            return False

    def duplicate_username_check(self, username):
        self.cur.execute("SELECT * FROM USERS WHERE username=?", (username,))
        result = self.cur.fetchone()
        if result:
            return True
        else:
            return False

    def send_otp(self, email, username):
        otp = self.generate_otp()
        subject = "Your AnarchKey Signup OTP Code"
        with open(f'{self.path}/static/otp.html', 'r') as file:
            body = file.read()

        # Replace placeholders with actual values
        body = body.replace("{username}", username).replace("{otp}", str(otp))
        sender_email = SENDER_EMAIL
        sender_password = SENDER_PASSWORD

        message = MIMEMultipart()
        message["From"] = "AnarchKey"
        message["To"] = email
        message["Subject"] = subject
        message.attach(MIMEText(body, "html"))

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, sender_password)
                server.send_message(message)
            print("Email sent successfully")
            return True, otp
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False, None

    def send_reset_password_email(self, email, username, reset_link):
        subject = "Protobase Password Reset Request"

        with open(f'{self.path}reset_password_template.html', 'r') as file:
            body = file.read()

        body = body.replace("{username}", username).replace("{reset_link}", reset_link)

        sender_email = SENDER_EMAIL
        sender_password = SENDER_PASSWORD

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = email
        message["Subject"] = subject
        message.attach(MIMEText(body, "html"))

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, sender_password)
                server.send_message(message)
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
