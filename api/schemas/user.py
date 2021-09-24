from typing import Optional
from pydantic import BaseModel

class User_Model(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
