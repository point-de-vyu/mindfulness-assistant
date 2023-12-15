from requests import post, get
from app.schemes.user import User
import json
from api_backend.app.utils import get_postgres_engine
from api_backend.app.managers.user_manager import UserManager
from api_backend.app.schemes.sos_rituals import SosTable, SosRitual


# one_user = User(username="@thehacker", first_name="); DROP TABLE users;--", last_name="Harrisson")
# one_user_json = one_user.model_dump_json()
# response = post("http://0.0.0.0:8080/users/", data=one_user_json)
# # response = get("http://0.0.0.0:8080/users/?date_registered=2023-12-04")


# new_rit = SosRitual(
#     category="Affirmation",
#     situation="Anger",
#     title="Let it be",
#     description="Let it beee let it bee",
#     url="www.beatles.com"
# ).model_dump_json()
#
# response = post("http://0.0.0.0:8080/custom_sos_ritual/%40beatle1", data=new_rit)
response = get("http://0.0.0.0:8080/sos_defaults/?category=Mditation")
print(response.status_code)
print(response.json())


