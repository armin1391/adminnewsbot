from config import (
    FORCE_JOIN_ENABLED,
    FORCE_JOIN_CHANNELS
)


def is_force_join_enabled():
    return FORCE_JOIN_ENABLED


def get_force_join_channels():
    return FORCE_JOIN_CHANNELS
    
from channel_checker import get_chat_member


def is_user_joined(user_id):

    if not FORCE_JOIN_ENABLED:
        return True

    for channel in FORCE_JOIN_CHANNELS:

        status = get_chat_member(
            channel["id"],
            user_id
        )

        if status not in (
            "creator",
            "administrator",
            "member"
        ):
            return False

    return True