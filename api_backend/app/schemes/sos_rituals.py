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


class SosTable(str, Enum):
    DEFAULT_IDS = "sos_rituals_default_ids"
    RITUALS = "sos_rituals"
    CATEGORIES = "sos_categories"
    SITUATIONS = "sos_situations"
    USER_RITUAL = "user_sos_ritual"
    USER_FEEDBACK_TO_RITUAL = "user_feedback_to_ritual"

    def __str__(self):
        return self.value
