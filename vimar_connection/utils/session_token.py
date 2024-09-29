import secrets
import string

def get_session_token(length=12):
    characters = string.ascii_letters + string.digits
    session_id = ''.join(secrets.choice(characters) for _ in range(length))
    return session_id

# session_token = get_session_token()
# print("Unique Session Token:", session_token)