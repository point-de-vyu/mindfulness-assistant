from enum import Enum


SOS_ID_REGEXP = r"3\d{18}"


class MemoryKey(str, Enum):
    SOS_SITUATION = "sos_situation"
    SOS_CATEGORY = "sos_category"
    AVAIL_RITUALS = "available_rituals"
    USR_AVAIL_RITUALS = "user_available_rituals"
    IS_LAST_RITUAL_DEFAULT = "is_last_ritual_default"
    CURRENT_RITUAL = "current_ritual"

    def __str__(self):
        return self.value


class SosSearchParams(str, Enum):
    SITUATION = "situation"
    CATEGORY = "category"

    def __str__(self):
        return self.value
