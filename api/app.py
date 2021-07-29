from fastapi import FastAPI
from routes.blogpost import blog_post


# Init FastAPI
app = FastAPI(
    title = "Blog API",
    description = "Endpoints para administrar todo lo relacionado con el Blog",
    version = 0.1,
    openapi_tags = [{
        "name": "Posts",
        "description": "Endpoint of Posts"
    }]
)


# Include Routes to FastAPI
app.include_router(blog_post)
