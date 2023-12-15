from enum import Enum


class ErrorMsg(str, Enum):
    USER_NOT_FOUND = "No such user found"
    SOS_CATEGORY_NOT_FOUND = "No such category found, check name for typos"
    SOS_SITUATION_NOT_FOUND = "No such situation found, check name for typos"
    SOS_DEFAULT_RITUAL_NOT_FOUND = "No such default sos ritual available"

    ACTION_FAILED = "Failed to perform action (insert or delete)"

    ROWS_MORE_THAN_ONE = "Found > 1 rows in DB when it should be 1"
    FAILED_DB_RESULT = "DB did not return a result"

    def __str__(self):
        return self.value
