import random
import string

from jose import JWTError
from sqlalchemy import select
from fastapi import FastAPI, Body, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field, EmailStr

from auth.auth import signJWT, decodeJWT
from auth.models import UserSchema, UserLoginSchema, TokenData
from database import session
from models import Urls

users = {}

app = FastAPI()

class ItemBase(BaseModel):
    urls: str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
name = "Danylo"


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return user_dict


def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication data!",
            headers={"WWW-Authenticate": "Bearer"}
        )
    try:
        payload = decodeJWT(token)
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception
    user = get_user(users, username=token_data.username)
    if user is  None:
        raise credential_exception
    return user


@app.post("/")
def cutter_id(url: ItemBase, current_user: UserSchema = Depends(get_current_user)):
    random_int = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(6)])
    new_url = Urls(url=url.urls, random=random_int)
    session.add(new_url)
    session.commit()
    return {"msg": f"http://127.0.0.1:8000/{random_int}"}


@app.get("/{code}")
async def redirect_typer(code: str):
    stmt = select(Urls).where(Urls.random == code)
    if url := session.scalar(stmt):
        print(url.url)
        return RedirectResponse(url.url)
    else:
        return {"msg": "Code doesnt exist"}


@app.post("/signup", tags=["users"])
def get_token(user: UserSchema):
    users[user.username] = user
    return signJWT(user.username)


@app.post("/login", tags=["users"])
def get_login(user: OAuth2PasswordRequestForm = Depends()):
    print(user)
    if user_data := users.get(user.username):
        if user_data.password == user.password:
            return signJWT(user.username)
    return {
        "Error": "Invalid user data!"
    }

@app.get("/users/me")
async def read_user(current_user: UserSchema = Depends(get_current_user)):
    return current_user