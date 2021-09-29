from fastapi import APIRouter, Response, Depends
from starlette.status import HTTP_204_NO_CONTENT

# Internal Modules
from config.db import db_connection
from models.category import categories_table
from schemas.category import Category_Model
from auth.schemas.users import UserModel
from auth.manage_tokens import get_current_active_user


# Init Routes
blog_categories = APIRouter()


# Routes
@blog_categories.get("/categories", response_model=list[Category_Model], tags=["Categories"])
async def get_all_posts():
    return db_connection.execute(categories_table.select()).fetchall()


@blog_categories.get("/categories/{id}", response_model=Category_Model, tags=["Categories"])
async def get_post_by_id(id: int):
    return db_connection.execute(categories_table.select().where(categories_table.c.id_categories == id)).first()


@blog_categories.post("/categories", response_model=Category_Model, tags=["Categories"])
async def create_new_post(category: Category_Model, current_user: UserModel = Depends(get_current_active_user)):
    new_category = {
        "category": category.category,
    }

    result = db_connection.execute(categories_table.insert().values(new_category))
    return db_connection.execute(categories_table.select().where(categories_table.c.id_categories == result.lastrowid)).first()


@blog_categories.delete("/categories/{id}", status_code=HTTP_204_NO_CONTENT, tags=["Categories"])
async def delete_post_by_id(id: int, current_user: UserModel = Depends(get_current_active_user)):
    db_connection.execute(categories_table.delete().where(categories_table.c.id_categories == id))
    return Response(status_code=HTTP_204_NO_CONTENT)


@blog_categories.put("/categories/{id}", response_model=Category_Model, tags=["Categories"])
async def update_post_by_id(id: int, category: Category_Model, current_user: UserModel = Depends(get_current_active_user)):
    db_connection.execute(categories_table.update().values(
        category = category.category,
    ).where(categories_table.c.id_categories == id))
    return db_connection.execute(categories_table.select().where(categories_table.c.id_categories == id)).first()

