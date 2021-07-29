from os import name
from fastapi import APIRouter, Response
from starlette.status import HTTP_204_NO_CONTENT
from config.db import db_connection
from models.posts import all_posts_table
from schemas.post import Post_Model


# Init Routes
blog_post = APIRouter()

# Routes
@blog_post.get("/posts", response_model=Post_Model)
def get_all_posts():
    return db_connection.execute(all_posts_table.select()).fetchall()


@blog_post.get("/posts/{id}", response_model=Post_Model)
def get_post_by_id(id: int):
    return db_connection.execute(all_posts_table.select().where(all_posts_table.c.id == id)).first()


@blog_post.post("/posts", response_model=Post_Model)
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


@blog_post.delete("/posts/{id}", status_code=HTTP_204_NO_CONTENT)
def delete_post_by_id(id: int):
    db_connection.execute(all_posts_table.delete().where(all_posts_table.c.id == id))
    return Response(status_code=HTTP_204_NO_CONTENT)


@blog_post.put("/posts/{id}", response_model=Post_Model)
def update_post_by_id(id: int, post: Post_Model):
    db_connection.execute(all_posts_table.update().values(
        category = post.category,
        post_name = post.post_name,
        date = post.date,
        post_title = post.post_title,
        post_description = post.post_description
    ).where(all_posts_table.c.id == id))
    return db_connection.execute(all_posts_table.select().where(all_posts_table.c.id == id)).first()

