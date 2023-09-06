
from src.auth.contexts.user import UserReadable


ALL_METHODS_IS_ALLOWED = "*"
LOCAL_VISIBILITY_SCOPE = "-l"


class UserPemissions(UserReadable):
    permissions: dict = {"methods" : ALL_METHODS_IS_ALLOWED, "visibility" : LOCAL_VISIBILITY_SCOPE}
