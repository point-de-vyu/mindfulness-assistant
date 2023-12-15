from enum import Enum


class ErrorMsg(str, Enum):
    USER_NOT_FOUND_404 = "No such user found"
    SOS_CATEGORY_NOT_FOUND_404 = "No such category found, check name for typos"
    SOS_SITUATION_NOT_FOUND_404 = "No such situation found, check name for typos"
    SOS_DEFAULT_RITUAL_NOT_FOUND_404 = "No such default sos ritual available"
    ROWS_MORE_THAN_ONE_500 = "Found > 1 rows in DB when it should be 1"

    FAILED_DB_RESULT_500 = "DB did not return a result"

    def __str__(self):
        return self.value
