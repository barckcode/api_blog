import os
from fastapi import APIRouter, Response, Depends
from starlette.status import HTTP_204_NO_CONTENT

# Internal Modules
from config.db import db_connection
from auth.models.users import users_table
from auth.schemas.users import UserModel
from auth.manage_tokens import get_current_active_user
from auth.manage_tokens import get_password_hash


# Env Vars
SECRET_KEY = os.getenv("TOKEN_SSL")
ALGORITHM = os.getenv("TOKEN_ALGORITHM")


# Init Routes
users_route = APIRouter()


# Routes
@users_route.get("/users", response_model=list[UserModel], tags=["Users"])
async def get_all_users(current_user: UserModel = Depends(get_current_active_user)):
    return db_connection.execute(users_table.select()).fetchall()


# Routes
@users_route.post("/users", response_model=UserModel, tags=["Users"])
async def create_new_user(user: UserModel, current_user: UserModel = Depends(get_current_active_user)):
    password = user.password
    hashed_password = get_password_hash(password)

    new_user = {
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "disabled": user.disabled,
        "password": hashed_password
    }

    result = db_connection.execute(users_table.insert().values(new_user))
    return db_connection.execute(users_table.select().where(users_table.c.id == result.lastrowid)).first()
