from flask import Flask, render_template, request, session, redirect, jsonify, url_for
import Authentication
import os
from dotenv import load_dotenv
load_dotenv()
db = Authentication.Auth()

app = Flask(__name__)
app.secret_key = os.getenv("secret")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/learn_more')
def learn_more():
    if not session.get("user_signed_in"):
        return render_template("register_login.html")
    return redirect(url_for("dashboard"))


@app.route('/send_otp', methods=['POST'])
def send_otp():
    data = request.get_json()
    email = data.get("email")
    username = data.get("username")

    if not db.duplicate_email_check(email) and not db.duplicate_username_check(username, "dev_api_tokens"):
        success, session['c_otp'] = db.auth.send_otp(email=email, username=username)

        if success:
            return jsonify(success=True)
        else:
            return jsonify(success=False, message="Failed to send OTP. Please try again.")
    else:
        return jsonify(success=False, message="Email or Username already exists.")


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    response = db.signup(username=username, password=password)
    if response:
        session["user_signed_in"] = True
        session["username"] = username
        session.pop('c_otp', None)
        return jsonify(response)

    else:
        return jsonify(response)

@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    email = db.get_email(username)
    result = db.validate_developer(username, password, email)
    if result:
        session["user_signed_in"] = True
        session["username"] = username
        # session["token"] = db.retrieve_token(username, password)[0]
        return jsonify(success=True)
    else:
        return jsonify(success=False, message="Signin failed. Incorrect credentials.")


@app.route("/logout")
def logout():
    session.pop("user_signed_in", None)
    session.pop("username", None)
    return redirect(url_for("learn_more"))





@app.route("/dashboard")
def dashboard():
    if not session.get("user_signed_in"):
        return redirect(url_for("get_started"))
    username = session.get("username")
    return render_template("dashboard.html", username=username)

@app.route('/docs')
def docs():
    return render_template('docs.html')
if __name__ == '__main__':
    app.run(load_dotenv=True)
