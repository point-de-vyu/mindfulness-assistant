from pydantic import BaseModel
from typing import Optional
from datetime import date


class UserToCreate(BaseModel):
    first_name: str
    last_name: str
    username: str


class User(UserToCreate):
    id: int
    date_registered: str | date
