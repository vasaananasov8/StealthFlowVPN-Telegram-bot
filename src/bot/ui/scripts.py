from datetime import datetime as dt, datetime

from attr import dataclass


@dataclass
class Scripts:
    dt_format = "'%d.%m.%Y %H:%M'"
    start_script: str = """!!!---Старт---!!!"""

    @staticmethod
    def connection_link(connection_link: str) -> str:
        return f"Ваша ссылка для подключения: `{connection_link}`"

    def successful_new_connection(self, connection_link: str, until: datetime) -> str:
        return (f"Соединение успешно созданно\n"
                f"Подписка работает до <b>{until.strftime(self.dt_format)}</b>\n\n"
                f"Ваша ссылка для подключения: <code>{connection_link}</code>")

    def successful_extend_subscription(self, old_until: dt, new_until: dt) -> str:
        return (f"Подписка успешно продлена c {old_until.strftime(self.dt_format)}"
                f" до {new_until.strftime(self.dt_format)}")
