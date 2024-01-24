from pydantic import BaseModel
from typing import Optional
from datetime import date


class BaseUser(BaseModel):
    first_name: str
    last_name: str
    username: str


class UserToCreate(BaseUser):
    id_from_client: int


class User(BaseUser):
    id: int
    date_registered: str | date
