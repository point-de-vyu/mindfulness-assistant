from pydantic import BaseModel
from typing import Optional
from datetime import date


class User(BaseModel):
    first_name: str
    last_name: str
    username: str
    id: Optional[int] = None
    date_registered: Optional[str | date] = None
