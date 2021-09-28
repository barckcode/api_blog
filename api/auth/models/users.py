from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String, Boolean
from config.db import meta, engine_mysql

users_table = Table("users", meta,
    Column("id", Integer, primary_key=True, unique=True, autoincrement=True, nullable=False),
    Column("username", String(100), unique=True, nullable=False),
    Column("email", String(100), unique=True, nullable=False),
    Column("full_name", String, nullable=False),
    Column("disabled", Boolean, nullable=False),
    Column("password", String(255), nullable=False)
)

meta.create_all(engine_mysql)
