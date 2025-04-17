import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random as rd


class Anarch2FA:
    @staticmethod
    def generate_otp():
        otp = rd.randint(100000, 999999)
        return otp

    def send_otp(self, email, username):
        otp = self.generate_otp()
        subject = "Your Protobase Signup OTP Code"
        with open(f'{path}otp.html', 'r') as file:
            body = file.read()

        # Replace placeholders with actual values
        body = body.replace("{username}", username).replace("{otp}", str(otp))
        sender_email = SENDER_EMAIL
        sender_password = SENDER_PASSWORD

        message = MIMEMultipart()
        message["From"] = "ProtoBase"
        message["To"] = email
        message["Subject"] = subject
        message.attach(MIMEText(body, "html"))

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, sender_password)
                server.send_message(message)
            return True, otp
        except Exception as e:
            return False, None

    @staticmethod
    def send_reset_password_email(email, username, reset_link):
        subject = "Protobase Password Reset Request"

        with open(f'{path}reset_password_template.html', 'r') as file:
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
