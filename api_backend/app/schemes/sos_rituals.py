from typing import List
from pydantic import BaseModel
from enum import Enum


# разделить все-таки на

class SosRitual(BaseModel):
    id: int | None = None
    category: str
    situation: str
    title: str
    description: str
    url: str | None = None
    tags: List[str] | None = None


class SosTable(Enum):
    DEFAULT_IDS = "sos_rituals_default_ids"
    RITUALS = "sos_rituals"
    CATEGORIES = "sos_categories"
    SITUATIONS = "sos_situations"
    USER_RITUAL = "user_sos_ritual"
    USER_FEEDBACK_TO_RITUAL = "user_feedback_to_ritual"

    def __str__(self):
        return self.value
