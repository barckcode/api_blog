from fastapi import FastAPI

# Routes
from auth.manage_tokens import login
from auth.routes.users import users_route
from routes.blogpost import blog_post
from routes.categories import blog_categories


# Init FastAPI
app = FastAPI(
    title = "Blog API",
    description = "Endpoints para administrar todo lo relacionado con el Blog",
    version = 0.3,
    contact = {
        "name": "Helmcode",
        "url": "https://helmcode.com/contact",
    },
    openapi_tags = [
        {
            "name": "Auth",
            "description": "Auth Endpoints"
        },
        {
            "name": "Users",
            "description": "Users Endpoints"
        },
        {
            "name": "Posts",
            "description": "Posts Endpoints"
        },
        {
            "name": "Categories",
            "description": "Categories Endpoints"
        }
    ]
)


app.include_router(login)                   # Auth
app.include_router(users_route)             # Users
app.include_router(blog_post)               # Posts
app.include_router(blog_categories)         # Categories
