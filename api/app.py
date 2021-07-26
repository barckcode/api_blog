from fastapi import FastAPI
from routes.blogpost import blog_post


# Init FastAPI
app = FastAPI()


# Include Routes to FastAPI
app.include_router(blog_post)
