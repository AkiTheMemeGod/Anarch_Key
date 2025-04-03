import secrets as sec

def generate_api_key() -> str:
    api_key = sec.token_urlsafe(48)
    return api_key

