from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool = True
    created_at: datetime = datetime.utcnow()
    tags: List[str] = []
    manager_id: Optional[int] = None

