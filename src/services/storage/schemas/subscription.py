from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.services.storage.schemas.meta import Base


class Subscription(Base):
    __tablename__ = "subscriptions"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    last_payment: Mapped[int | None] = mapped_column(ForeignKey("payments.id"))
    sale: Mapped[int]
    until: Mapped[datetime]
    active_links: Mapped[int]
    is_active: Mapped[bool]
    