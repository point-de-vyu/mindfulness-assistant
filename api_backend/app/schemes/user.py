from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    first_name: str
    last_name: str
    username: str
    id: Optional[str] = None
    date_registered: Optional[str] = None
