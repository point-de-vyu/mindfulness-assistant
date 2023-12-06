from requests import post, get
from app.schemes.user import User
import json
from api_backend.app.utils import get_postgres_engine
from api_backend.app.managers.user_manager import UserManager
one_user = User(username="@beatle4", first_name="George", last_name="Harrisson")
one_user_json = one_user.model_dump_json()
response = post("http://0.0.0.0:8080/users/", data=one_user_json)
# response = get("http://0.0.0.0:8080/users/?date_registered=2023-12-04")
print(response.status_code)
print(response.json())


