from abc import ABC, abstractmethod
from datetime import datetime

from src.bot.ui.scripts.data import SCRIPT_RU
from src.bot.ui.scripts.exceptions import LanguageCodeNotSet, NotSupportedLanguageCode
from src.config import const
from src.core.models.subscription import Subscription


class IScripts(ABC):
    lang_code: str | None
    _script_storage: dict[str, str]
    dt_format = '%d.%m.%Y %H:%M'
    d_format = '%d.%m.%Y'
    _supported_lc: str = const.SUPPORTED_LANGUAGE_CODES

    def _get_storage(self) -> None:
        match self.lang_code:
            case "ru":
                self._script_storage = SCRIPT_RU
            case _:
                ...

    def _check_is_langcode_set(self) -> None:
        if self.lang_code is None:
            raise LanguageCodeNotSet("Lang code didn't set")

    def set_language(self, lang_code: str):
        if lang_code not in self._supported_lc:
            raise NotSupportedLanguageCode(f"Lang code: {lang_code} not supported. User one of: {self._supported_lc}")
        else:
            self.lang_code = lang_code
            self._get_storage()

    @abstractmethod
    def start_script(self) -> str:
        ...

    @abstractmethod
    def get_vpn(self) -> str:
        ...

    @abstractmethod
    def connection_link(self, connection_link: str) -> str:
        ...

    @abstractmethod
    def successful_new_connection(self, connection_link: str, until: datetime) -> str:
        ...

    @abstractmethod
    def stats(self, subscription: Subscription) -> str:
        ...

    @abstractmethod
    def stats_has_not_active_subscription(self) -> str:
        ...

    @abstractmethod
    def stats_active_connection_links(self, connection_links: list[str]) -> str:
        ...
