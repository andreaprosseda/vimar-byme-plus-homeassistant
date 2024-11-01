import secrets
import string


def get_session_token(length=12):
    characters = string.ascii_letters + string.digits
    session_id = "".join(secrets.choice(characters) for _ in range(length))
    return session_id
