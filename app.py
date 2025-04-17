from flask import Flask, render_template, request, session, redirect, jsonify, url_for, g
import os
from dotenv import load_dotenv
from AnarchDB import AnarchAPI
from AnarchKeyAuthentication import AnarchKeyAuth, AnarchKeyService

load_dotenv()
from flask import Flask

app = Flask(__name__)


app.secret_key = os.getenv("secret")

def get_api():
    if 'api' not in g:
        g.api = AnarchAPI()
    return g.api


def get_auth():
    if 'auth' not in g:
        g.auth = AnarchKeyAuth()
    return g.auth


@app.teardown_appcontext
def close_connections(e=None):
    api = g.pop('api', None)
    if api:
        api.con.close()

    auth = g.pop('auth', None)
    if auth:
        auth.con.close()


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/learn_more')
def learn_more():
    if not session.get("user_signed_in"):
        return render_template("register_login.html")
    return redirect(url_for("dashboard"))

@app.route('/dashboard')
def dashboard():
    if session.get("user_signed_in"):
        return render_template("dashboard.html")
    return redirect(url_for("learn_more"))

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
    if session.get("user_signed_in"):
        return render_template("dashboard.html")
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")

    auth = get_auth()
    response = auth.signup(username=username, password=password, email=email)
    if response['success']:
        session["user_signed_in"] = True
        session["username"] = username
        session.pop('c_otp', None)
        return jsonify(response)

    else:
        return jsonify(response)

@app.route('/signin', methods=['POST'])
def signin():
    if session.get("user_signed_in"):
        return render_template("dashboard.html")

    auth = get_auth()
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    print(username, password)
    result = auth.login(username, password)
    print(result)
    if result['success']:
        session["user_signed_in"] = True
        session["username"] = username
        return jsonify(success=True)
    else:
        return jsonify(success=False, message="Signin failed. Incorrect credentials.")


@app.route("/logout")
def logout():
    session.pop("user_signed_in", None)
    session.pop("username", None)
    return redirect(url_for("learn_more"))


@app.route('/get_api_key', methods=['POST'])
def get_api_key():

    data = request.get_json()
    project_name = data.get("project_name")
    username = data.get("username")
    apikey = data.get("api_key")
    api = get_api()
    api_key = api.retrieve_api_key(project_name, username, apikey)
    if api_key:
        return jsonify(success=True, api_key=api_key)
    else:
        return jsonify(success=False, message="API key not found.")

@app.route('/get_user_details', methods=['GET'])
def get_user_details():
    if not session.get("user_signed_in"):
        return jsonify({'success': False, 'message': 'User not logged in'})

    try:
        db_service = AnarchKeyService()
        db_service.cur.execute("SELECT email, created_at FROM USERS WHERE username=?", (session['username'],))
        result = db_service.cur.fetchone()

        if not result:
            return jsonify({'success': False, 'message': 'User not found'})

        return jsonify({
            'success': True,
            'email': result[0],
            'created_at': result[1]
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/get_user_api_keys', methods=['GET'])
def get_user_api_keys():
    if not session.get("user_signed_in"):
        return jsonify({'success': False, 'message': 'User not logged in'})

    try:
        db_service = get_auth()
        db_service.cur.execute("""
            SELECT project_name FROM PROJECTS 
            WHERE username = ?
        """, (session['username'],))

        projects = db_service.cur.fetchall()
        api_keys = []

        for project in projects:
            project_name = project[0]
            db_service.cur.execute("""
                SELECT rowid, encrypted_api_key, created_at, last_used, uses 
                FROM APIKEYS 
                WHERE project_name = ?
            """, (project_name,))

            key_data = db_service.cur.fetchone()
            if key_data:
                api_keys.append({
                    'id': key_data[0],
                    'project_name': project_name,
                    'api_key': db_service.decrypt(key_data[1]),
                    'created_at': key_data[2],
                    'usage_count': key_data[4] or 0
                })

        return jsonify({'success': True, 'api_keys': api_keys})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/add_api_key', methods=['POST'])
def add_api_key():
    print(session)
    if not session.get("user_signed_in"):
        return jsonify({'success': False, 'message': 'User not logged in'})

    data = request.get_json()
    project_name = data.get('project_name')
    api_key = data.get('api_key')
    username = session.get('username')  # Use session username instead of from request

    print(f"Received data: {project_name}, {username}")

    if not project_name or not api_key:
        return jsonify({'success': False, 'message': 'Project name and API key are required'})

    try:
        db_service = get_auth()

        # Check if project exists
        db_service.cur.execute("SELECT 1 FROM PROJECTS WHERE project_name=? AND username=?",
                               (project_name, username))
        project_exists = db_service.cur.fetchone()

        # Create project if it doesn't exist
        if not project_exists:
            print(f"Creating new project: {project_name} for {username}")
            project_result = db_service.insert_new_project(project_name, username, "Created from dashboard")
            if not project_result['success']:
                return jsonify(project_result)

        # Now add the API key
        print(f"Inserting API key for project: {project_name}")
        result = db_service.insert_new_api_key(project_name, api_key)
        return jsonify(result)
    except Exception as e:
        print(f"Error adding API key: {str(e)}")
        return jsonify({'success': False, 'message': str(e)})
@app.route('/delete_api_key', methods=['POST'])
def delete_api_key():
    if not session.get("user_signed_in"):
        return jsonify({'success': False, 'message': 'User not logged in'})

    data = request.get_json()
    key_id = data.get('key_id')

    if not key_id:
        return jsonify({'success': False, 'message': 'Key ID is required'})

    try:
        db_service = get_auth()

        # Get the project name for this key ID
        db_service.cur.execute("""
            SELECT project_name FROM APIKEYS WHERE rowid = ?
        """, (key_id,))

        result = db_service.cur.fetchone()
        print(result)
        if not result:
            return jsonify({'success': False, 'message': 'API key not found'})

        project_name = result[0]

        db_service.cur.execute("""
            SELECT * FROM PROJECTS WHERE project_name = ? AND username = ?
        """, (project_name, session['username']))

        if not db_service.cur.fetchone():
            return jsonify({'success': False, 'message': 'Unauthorized to delete this key'})

        # Delete the key
        db_service.cur.execute("DELETE FROM APIKEYS WHERE rowid = ?", (key_id,))
        db_service.con.commit()

        return jsonify({'success': True, 'message': 'API key deleted successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/get_api_usage', methods=['GET'])
def get_api_usage():
    if not session.get("user_signed_in"):
        return jsonify({'success': False, 'message': 'User not logged in'})

    try:
        db_service = get_auth()

        db_service.cur.execute("""
            SELECT project_name FROM PROJECTS 
            WHERE username = ?
        """, (session['username'],))

        projects = db_service.cur.fetchall()
        usage = []

        for project in projects:
            project_name = project[0]
            db_service.cur.execute("""
                SELECT last_used, uses FROM APIKEYS 
                WHERE project_name = ? AND last_used != '--:--:--'
            """, (project_name,))

            usage_data = db_service.cur.fetchone()
            if usage_data and usage_data[0] != '--:--:--':
                usage.append({
                    'project_name': project_name,
                    'timestamp': usage_data[0],
                    'endpoint': 'API Call',
                    'uses': usage_data[1] or 0
                })

        # Sort by timestamp, most recent first
        usage.sort(key=lambda x: x['timestamp'], reverse=True)

        return jsonify({'success': True, 'usage': usage})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


if __name__ == '__main__':
    app.run(load_dotenv=True)
