from sqlalchemy.orm import Mapped, mapped_column

from src.services.storage.schemas.meta import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    first_name: Mapped[str | None]
    second_name: Mapped[str | None]
    language_code: Mapped[str]
    timezone: Mapped[int]
