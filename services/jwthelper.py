import jwt
from datetime import datetime, timezone, timedelta

SECRET_KEY = "hUl1evdKXBNQVSROevNhoa32OAnnAlvA"
ALGORITHM = "HS256"

def create_jwt(user_id: str):
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=72)  # expires in 72 hours
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_jwt(token: str):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
