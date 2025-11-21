# AnarchKey Client

A Python client library for connecting to and retrieving API keys from the AnarchKey vault service.
## Description
AnarchKeyClient provides a simple interface to securely retrieve API keys stored in the AnarchKey vault service. This package helps developers manage API credentials for their projects without hardcoding sensitive information in their codebase.


## Installation
# STEP 1:
```bash
pip install AnarchKeyClient
```

# STEP 2
head over to https://anarchkey.pythonanywhere.com/ to signup
and get your username and password

# STEP 3
```bash
anarchkey init --username <YourUsername> --password <YourPassword>
```


## Usage

```python
from AnarchKeyClient import AnarchKeyClient

# Initialize the client with your username and AnarchKey API key
client = AnarchKeyClient(username="YourUsername", api_key="YourAnarchKeyAPIKey")

# Retrieve an API key for a specific project
response = client.get_api_key(project_name="YourProjectName")

# Check if request was successful
if response["success"]:
    api_key = response["key"]
    print(f"Retrieved API key: {api_key}")
else:
    print(f"Error: {response['message']}")
```

## License MIT