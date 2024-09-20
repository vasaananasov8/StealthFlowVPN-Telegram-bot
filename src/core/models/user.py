from pydantic import BaseModel

from src.services.storage.schemas.user import User as DbUser


class User(BaseModel):
    id: int
    username: str
    first_name: str | None
    second_name: str | None
    language_code: str
    timezone: int

    def get_db_user_model(self) -> DbUser:
        return DbUser(
            id=self.id,
            username=self.username,
            first_name=self.first_name,
            second_name=self.second_name,
            language_code=self.language_code,
            timezone=self.timezone
        )