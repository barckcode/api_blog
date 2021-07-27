from os import name
from typing import Optional
from pydantic import BaseModel

class Post_Model(BaseModel):
    id: Optional[int]
    category: str
    post_name: str
    date: str
    post_title: str
    post_description: str
