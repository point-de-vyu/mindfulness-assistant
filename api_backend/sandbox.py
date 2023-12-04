from requests import post, get
from app.schemes.user import User
import json
from api_backend.app.utils import get_postgres_engine
from api_backend.app.managers.user_manager import UserManager
one_user = User(username="@beatle1", first_name="Paul", last_name="McCartney")
one_user_json = one_user.model_dump_json()
response = post("http://0.0.0.0:8080/users/", data=one_user_json)
# response = get("http://0.0.0.0:8080/users/test")
print(response.status_code)
print(response.json())

