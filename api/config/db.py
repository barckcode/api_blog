import os
from sqlalchemy import create_engine, MetaData

USER_DATABASE = os.getenv("DB_USER")
PASSWORD_DATABASE = os.getenv("DB_PASSWORD")
HOST_DATABASE = os.getenv("DB_HOST")
DATABASE = os.getenv("DB_DATABASE")
URL_CONNECTION = f"mysql+pymysql://{USER_DATABASE}:{PASSWORD_DATABASE}@{HOST_DATABASE}:3306/{DATABASE}"

meta = MetaData()

engine_mysql = create_engine(URL_CONNECTION)
db_connection = engine_mysql.connect()
