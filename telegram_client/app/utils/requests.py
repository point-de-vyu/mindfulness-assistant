from typing import Dict
import os


def get_headers(user_id: str | int) -> dict:
    # TODO
    # token_header_title =
    # id_header_title =
    user_id = str(user_id)
    token = os.environ["API_AUTH_TOKEN"]
    return {"client-token": token, "id_from_client": user_id}


def get_base_url(router: str, endpoint: str = os.environ["API_ENDPOINT"]) -> str:
    router = router.strip("/")
    return f"http://{endpoint}/{router}/"

