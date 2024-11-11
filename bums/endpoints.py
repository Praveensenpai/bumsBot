from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class Endpoints:
    LOGIN_URL: Final[str] = "https://api.bums.bot/miniapps/api/user/telegram_auth"
    GAME_INFO_URL: Final[str] = (
        "https://api.bums.bot/miniapps/api/user_game_level/getGameInfo"
    )
    TAP_URL: Final[str] = "https://api.bums.bot/miniapps/api/user_game/collectCoin"
    TASK_LIST_URL: Final[str] = "https://api.bums.bot/miniapps/api/task/lists"
    TASK_FINISH_URL: Final[str] = "https://api.bums.bot/miniapps/api/task/finish_task"
    MINE_LIST_URL: Final[str] = "https://api.bums.bot/miniapps/api/mine/getMineLists"
    UPGRADE_URL: Final[str] = "https://api.bums.bot/miniapps/api/mine/upgrade"
    DAILY_SIGN_URL: Final[str] = "https://api.bums.bot/miniapps/api/sign/sign"
    SIGN_LISTS_URL: Final[str] = "https://api.bums.bot/miniapps/api/sign/getSignLists"
