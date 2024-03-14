from typing import Dict
import os


def get_headers(user_id: str | int) -> dict:
    token_header = os.environ["HEADER_NAME_TOKEN"]
    id_header = os.environ["HEADER_NAME_USER_ID"]
    user_id = str(user_id)
    token = os.environ["API_AUTH_TOKEN"]
    return {token_header: token, id_header: user_id}


def get_base_url(router: str, endpoint: str = os.environ["API_ENDPOINT"]) -> str:
    router = router.strip("/")
    return f"http://{endpoint}/{router}/"

