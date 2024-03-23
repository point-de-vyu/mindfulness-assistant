from typing import List
from pydantic import BaseModel
from enum import Enum


class SosRitualToCreate(BaseModel):
    category: str
    situation: str
    title: str
    description: str
    url: str | None = None
    tags: List[str] | None = None


class SosRitual(SosRitualToCreate):
    id: int | None = None


class SosCategory(BaseModel):
    id: int
    name: str


class SosSituation(BaseModel):
    id: int
    name: str
