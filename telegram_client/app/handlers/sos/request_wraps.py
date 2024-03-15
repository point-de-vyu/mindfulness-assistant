import requests
from typing import Dict
import random
from telegram_client.app.schemes.requests import RequestResult
from telegram_client.app.schemes.sos_rituals import SosRitual
from telegram_client.app.utils.requests import get_headers, get_base_url


async def get_rituals(
    user_id: int, is_default: bool, search_params: Dict[str, str]
) -> RequestResult:
    route = "sos_defaults" if is_default else "sos_rituals"
    response = requests.get(
        url=get_base_url(router=route),
        params=search_params,
        headers=get_headers(user_id),
    )
    if response.status_code != 200:
        rituals = []
        error_detail = response.json()["detail"] if "detail" in response.json() else ""
    else:
        rituals = [SosRitual(**rit) for rit in response.json()]
        random.shuffle(rituals)
        error_detail = ""
    res = RequestResult(
        status_code=response.status_code, detail=error_detail, data=rituals
    )
    return res
