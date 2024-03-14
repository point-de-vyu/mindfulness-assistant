from pydantic import BaseModel
from typing import Any


class RequestResult(BaseModel):
    status_code: int
    detail: str
    data: Any
