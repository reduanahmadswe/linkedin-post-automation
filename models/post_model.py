from pydantic import BaseModel
from typing import Optional

class Post(BaseModel):
    id: Optional[int]
    content: str
    status: str
    created_at: Optional[str]
