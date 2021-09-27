from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import meta, engine_mysql

categories_table = Table("categories", meta,
    Column("id_categories", Integer, primary_key=True, unique=True, autoincrement=True, nullable=False),
    Column("category", String(65), nullable=False),
)

meta.create_all(engine_mysql)
