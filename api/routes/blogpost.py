from fastapi import APIRouter, Response, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.status import HTTP_204_NO_CONTENT
from config.db import db_connection
from models.posts import all_posts_table
from schemas.post import Post_Model
from schemas.user import User_Model


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}


# Auth
def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class UserInDB(User_Model):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User_Model = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# Init Routes
blog_post = APIRouter()


@blog_post.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@blog_post.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}


@blog_post.get("/users/me")
async def read_users_me(current_user: User_Model = Depends(get_current_active_user)):
    return current_user








# Routes
@blog_post.get("/posts", response_model=list[Post_Model], tags=["Posts"])
async def get_all_posts(token: str = Depends(oauth2_scheme)):
    return db_connection.execute(all_posts_table.select()).fetchall()


@blog_post.get("/posts/{id}", response_model=Post_Model, tags=["Posts"])
def get_post_by_id(id: int):
    return db_connection.execute(all_posts_table.select().where(all_posts_table.c.id == id)).first()


@blog_post.post("/posts", response_model=Post_Model, tags=["Posts"])
def create_new_post(post: Post_Model):
    new_post = {
        "category": post.category,
        "post_name": post.post_name,
        "date": post.date,
        "post_title": post.post_title,
        "post_description": post.post_description
    }

    result = db_connection.execute(all_posts_table.insert().values(new_post))
    return db_connection.execute(all_posts_table.select().where(all_posts_table.c.id == result.lastrowid)).first()


@blog_post.delete("/posts/{id}", status_code=HTTP_204_NO_CONTENT, tags=["Posts"])
def delete_post_by_id(id: int):
    db_connection.execute(all_posts_table.delete().where(all_posts_table.c.id == id))
    return Response(status_code=HTTP_204_NO_CONTENT)


@blog_post.put("/posts/{id}", response_model=Post_Model, tags=["Posts"])
def update_post_by_id(id: int, post: Post_Model):
    db_connection.execute(all_posts_table.update().values(
        category = post.category,
        post_name = post.post_name,
        date = post.date,
        post_title = post.post_title,
        post_description = post.post_description
    ).where(all_posts_table.c.id == id))
    return db_connection.execute(all_posts_table.select().where(all_posts_table.c.id == id)).first()

