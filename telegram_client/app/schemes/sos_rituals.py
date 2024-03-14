from pydantic import BaseModel
from typing import List


class SosRitual(BaseModel):
    id: int
    category: str
    situation: str
    title: str
    description: str
    url: str | None = None
    tags: List[str] | None = None