from requests import get, post
import os


def get_headers(user_id: str) -> dict:
    # TODO
    # token_header_title =
    # id_header_title =
    token = os.environ["API_AUTH_TOKEN"]
    return {"client-token": token, "id_from_client": user_id}



async def send_request(url: str, req_type: str, headers: dict = None, content: dict = None):
    if req_type == "POST":
        return post(url, json=content, headers=headers)
    if req_type == "GET":
        return get(url, headers=headers)



