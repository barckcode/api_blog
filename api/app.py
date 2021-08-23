from fastapi import FastAPI
from routes.blogpost import blog_post
from routes.categories import blog_categories


# Init FastAPI
app = FastAPI(
    title = "Blog API",
    description = "Endpoints para administrar todo lo relacionado con el Blog",
    version = 0.2,
    contact = {
        "name": "Helmcode",
        "url": "https://helmcode.com/contact",
    },
    openapi_tags = [
        {
            "name": "Posts",
            "description": "Endpoint of Posts"
        },
        {
            "name": "Categories",
            "description": "Endpoint of Categories"
        }
    ]
)


# Include Routes to FastAPI
app.include_router(blog_post)
app.include_router(blog_categories)
