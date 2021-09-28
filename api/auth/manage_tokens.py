import os
from typing import Optional
from datetime import datetime, timedelta
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

# Internal Modules
from config.db import db_connection
from auth.models.users import users_table
from auth.schemas.tokens import Token
from auth.schemas.tokens_data import TokenData
from auth.schemas.users import UserModel


# Token
SECRET_KEY = os.getenv("TOKEN_SSL")
ALGORITHM = os.getenv("TOKEN_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("TOKEN_EXPIRATION"))


users_db = db_connection.execute(users_table.select()).fetchall()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(users_db, username: str):
    for user in users_db:
        id, username_db, email, full_name, disabled, password = user
        if username_db == username:
            return {
                "id": id,
                "username": username_db,
                "email": email,
                "full_name": full_name,
                "disabled": disabled,
                "hashed_password": password
            }


def authenticate_user(users_db, username: str, password: str):
    user = get_user(users_db, username)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: UserModel = Depends(get_current_user)):
    if current_user["disabled"]:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# Init Routes
login = APIRouter()


@login.post("/token", response_model=Token, tags=["Auth"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


#
# Examples:
##
# @login.get("/users/me/", response_model=UserModel)
# async def read_users_me(current_user: UserModel = Depends(get_current_active_user)):
#     print(current_user)
#     return {
#                 "id": current_user["id"],
#                 "username": current_user["username"],
#                 "email": current_user["email"],
#                 "full_name": current_user["full_name"],
#                 "disabled": current_user["disabled"],
#                 "password": current_user["hashed_password"]
#             }


# @login.get("/users/me/items/")
# async def read_own_items(current_user: UserModel = Depends(get_current_active_user)):
#     return [{"item_id": "Foo", "owner": current_user["username"]}]
