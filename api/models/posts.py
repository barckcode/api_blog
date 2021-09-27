from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import meta, engine_mysql

all_posts_table = Table("all_posts", meta,
    Column("id", Integer, primary_key=True, unique=True, autoincrement=True, nullable=False),
    Column("category", String(65), nullable=False),
    Column("post_name", String(100), nullable=False),
    Column("date", String(45), nullable=False),
    Column("post_title", String(250), nullable=False),
    Column("post_description", String(375), nullable=False),
)

meta.create_all(engine_mysql)
