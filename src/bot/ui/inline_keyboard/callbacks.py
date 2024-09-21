from typing import Final

MAIN_MENU: Final[str] = "MAIN_MENU"
CANCEL: Final[str] = "CANCEL"
CONNECTION_HELP: Final[str] = "CONNECTION_HELP"
GET_VPN: Final[str] = "GET_VPN"
GET_USER_STATS: Final[str] = "GET_USER_STATS"
SUPPORT: Final[str] = "SUPPORT"
PAY: Final[str] = "PAY"
USER_PROMO: Final[str] = "USER_PROMO"
USER_STATS: Final[str] = "USER_STATS"
CHECK_ACTIVE_CONNECTION_LINKS: Final[str] = "CHECK_ACTIVE_CONNECTION_LINKS"
ANSWER_SUPPORT_MSG: Final[str] = "ANSWER_SUPPORT_MSG"

def get_user_id_from_callback_data(callback_data: str) -> int:
    return int(callback_data.split("_")[-1])

def answer_support_msg_callback(user_id: int) -> str:
    return f"ANSWER_SUPPORT_MSG_{user_id}"

