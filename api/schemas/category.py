from typing import Optional
from pydantic import BaseModel

class Category_Model(BaseModel):
    id_categories: Optional[int]
    category: str
