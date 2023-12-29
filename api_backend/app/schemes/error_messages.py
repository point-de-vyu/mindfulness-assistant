from enum import Enum


class ErrorMsg(str, Enum):
    USER_NOT_FOUND = "No such user found"

    SOS_CATEGORY_INVALID = "Category does not exist, check name for typos"
    SOS_SITUATION_INVALID = "Situation does not exist, check name for typos"
    SOS_DEFAULT_RITUAL_ID_INVALID = "No default ritual with this ID exists"

    ACTION_FAILED = "Failed to perform action (insert or delete)"

    ROWS_MORE_THAN_ONE = "Found > 1 rows in DB when it should be 1"
    FAILED_DB_RESULT = "DB did not return a result"

    SOS_RITUAL_ID_NOT_IN_USER = "User has no ritual with such id"
    RITUAL_ALREADY_ADDED = "User already added ritual with this id"
    USER_ALREADY_EXISTS = "User with this username already exists"

    def __str__(self):
        return self.value
