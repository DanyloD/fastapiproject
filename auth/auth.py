from fastapi_users.authentication import CookieTransport
from jose import jwt
import time


cookie_transport = CookieTransport(cookie_name="token", cookie_max_age=3600)
SECRET = "whosaidsecret"


def token_response(token: str):
    return {
        "access token": token
    }


def signJWT(userID: str):
    payload = {
        "sub": userID,
        "expiry": time.time() + 600
    }
    token = jwt.encode(payload, SECRET, algorithm='HS256')
    return token_response(token)


def decodeJWT(token: str):
    try:
        decode_token = jwt.decode(token, SECRET, algorithms='HS256')
    except:
        return None
    return decode_token

