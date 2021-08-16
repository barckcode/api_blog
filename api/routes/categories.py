from fastapi import APIRouter, Response
from starlette.status import HTTP_204_NO_CONTENT
from config.db import db_connection
from models.category import categories_table
from schemas.post import Post_Model


# Init Routes
blog_categories = APIRouter()


# Routes
@blog_categories.get("/categories", response_model=list[Post_Model])
def get_all_posts():
    return db_connection.execute(categories_table.select()).fetchall()


@blog_categories.get("/categories/{id}", response_model=Post_Model)
def get_post_by_id(id: int):
    return db_connection.execute(categories_table.select().where(categories_table.c.id_categories == id)).first()


@blog_categories.post("/categories", response_model=Post_Model)
def create_new_post(category: Post_Model):
    new_category = {
        "category": category.category,
    }

    result = db_connection.execute(categories_table.insert().values(new_category))
    return db_connection.execute(categories_table.select().where(categories_table.c.id_categories == result.lastrowid)).first()


@blog_categories.delete("/categories/{id}", status_code=HTTP_204_NO_CONTENT)
def delete_post_by_id(id: int):
    db_connection.execute(categories_table.delete().where(categories_table.c.id_categories == id))
    return Response(status_code=HTTP_204_NO_CONTENT)


@blog_categories.put("/categories/{id}", response_model=Post_Model)
def update_post_by_id(id: int, category: Post_Model):
    db_connection.execute(categories_table.update().values(
        category = category.category,
    ).where(categories_table.c.id_categories == id))
    return db_connection.execute(categories_table.select().where(categories_table.c.id_categories == id)).first()

