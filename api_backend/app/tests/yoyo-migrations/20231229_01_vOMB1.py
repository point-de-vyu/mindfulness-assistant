"""

"""

from yoyo import step

__depends__ = {}

steps = [
    step("DELETE FROM users"),
    step("SELECT add_new_user('<@username>', '<some name>', '<some last name>', '<token>')")
]
