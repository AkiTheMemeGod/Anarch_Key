# 🏴 AnarchKey: Secure API Key Management

[![Ask DeepWiki](https://devin.ai/assets/askdeepwiki.png)](https://deepwiki.com/AkiTheMemeGod/Anarch_Key)

AnarchKey is a self-hostable, developer-friendly API key vault that puts you in control of your credentials. Stop hardcoding secrets in your code, prevent accidental leaks, and manage your API keys securely through a simple web interface and programmatic clients.

## Core Features

*   **Secure by Design:** Keys are encrypted at rest using AES encryption (`cryptography.fernet`).
*   **Centralized Management:** A user-friendly web dashboard to add, view, delete, and track the usage of your API keys across different projects.
*   **Programmatic Access:** Fetch keys securely at runtime using dedicated client libraries for Python and Node.js. No more plaintext keys in your source code.
*   **User Authentication:** A complete system with user signup, login, password management, and email-based OTP verification for sensitive actions.
*   **Usage Tracking:** Monitor when and how often your keys are accessed directly from the dashboard.
*   **Self-Hosted:** Run AnarchKey on your own infrastructure for absolute control over your security and data.

## How It Works

1.  **Deploy AnarchKey:** Set up the AnarchKey Flask server on your own infrastructure.
2.  **Sign Up & Manage:** Create an account via the web UI. Add your projects and the corresponding API keys you want to secure.
3.  **Initialize Client:** Use the AnarchKey CLI to authenticate from your development machine. This creates a secure local token.
4.  **Fetch Keys in Code:** Use the client library in your Python or Node.js application to fetch the necessary API keys at runtime. Your application never needs to store the keys directly.

## Usage

Once your server is running, you can use the client libraries to interact with it from your applications.

### Python Client (PyPI)

A Python client library for connecting to and retrieving API keys from your AnarchKey service.

**1. Installation**
```bash
pip install AnarchKeyClient
```

**2. Initialization**
Sign up for an account on your AnarchKey instance, then initialize the CLI with your credentials. This command creates a secure token at `~/.anarchkey`.

```bash
anarchkey init --username <YourUsername> --password <YourPassword>
```

**3. Usage**
```python
from AnarchKeyClient import AnarchKeyClient

# Initialize the client with your username and AnarchKey service key
# You can find your service key in the dashboard under "Account Information"
client = AnarchKeyClient(username="YourUsername", api_key="YourAnarchKeyServiceKey")

# Retrieve an API key for a specific project
response = client.get_api_key(project_name="YourProjectName")

# Check if the request was successful
if response["success"]:
    api_key = response["key"]
    print(f"Retrieved API key: {api_key}")
else:
    print(f"Error: {response['message']}")
```

### Node.js Client (npm)

A Node.js client with both a programmatic interface and a CLI.

**1. Installation**
```bash
npm install anarchkey-client -g
```

**2. Initialization**
Initialize the local token by running the CLI command with your credentials. This writes a token to `~/.anarchkey` with `0o600` permissions.

```bash
anarchkey init --username YourName --password YourPassword
```
You can specify a custom server URL with `--base-url https://your-anarchkey-instance.com/`.

**3. Usage**
```javascript
const AnarchKeyClient = require('anarchkey-client');

(async () => {
  // Initialize the client
  // Get your 'apiKey' from the web dashboard
  const client = new AnarchKeyClient({
    apiKey: 'my_anarchkey_service_key',
    username: 'me'
  });

  // Retrieve an API key for your project
  const result = await client.getApiKey('myproject');

  if (result instanceof Error) {
    console.error('Failed to retrieve key:', result.message);
  } else {
    console.log('Successfully retrieved API key:', result);
  }
})();
```

## Contributing

Contributions are welcome! If you find a bug or have a feature request, please open an issue. If you'd like to contribute code, feel free to submit a pull request.

## 📢 Stay Updated  

💡 Have ideas? Suggestions? Let's talk!  
📌 Follow updates here or connect on **[LinkedIn](https://www.linkedin.com/in/akash-k19052022/)**.  

## ⚡ "Secure Your API Keys. Take Back Control."  
