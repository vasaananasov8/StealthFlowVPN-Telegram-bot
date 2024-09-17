from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    first_name: str | None
    second_name: str | None
    language_code: str
    timezone: int
