from datetime import datetime as dt, datetime

from src.bot.ui.scripts.i_scripts import IScripts
from src.config import const
from src.core.models.subscription import Subscription


class Scripts(IScripts):

    def start_script(self) -> str:
        self._check_is_langcode_set()
        return self._script_storage["start"]

    def connection_link(self, connection_link: str) -> str:
        self._check_is_langcode_set()
        return self._script_storage["connection_link"].format(connection_link)

    def successful_new_connection(self, connection_link: str, until: datetime) -> str:
        self._check_is_langcode_set()
        return self._script_storage["successful_new_connection"].format(
            until.strftime(self.dt_format), connection_link
        )

    def successful_extend_subscription(self, old_until: dt, new_until: dt) -> str:
        return self._script_storage["successful_extend_subscription"].format(
            old_until.strftime(self.dt_format), new_until.strftime(self.dt_format)
        )

    def stats_has_not_active_subscription(self) -> str:
        return self._script_storage["stats_has_not_active_subscription"]

    def stats(self, subscription: Subscription) -> str:
        return self._script_storage["stats"].format(
            subscription.until.strftime(self.d_format),
            subscription.active_links,
            const.MAX_ACTIVE_LINKS
        )

    def stats_active_connection_links(self, connection_links: list[str]) -> str:
        script = self._script_storage["stats_active_connection_links"]
        for link in connection_links:
            script += f"\n\n- <code>{link}</code>"
        return script
