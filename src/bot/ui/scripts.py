from attr import dataclass


@dataclass
class Scripts:
    start_script: str = """!!!---Старт---!!!"""

    @staticmethod
    def connection_link(connection_link: str) -> str:
        return f"Ваша ссылка для подключения: `{connection_link}`"
