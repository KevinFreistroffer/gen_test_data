from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
