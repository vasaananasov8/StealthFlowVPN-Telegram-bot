import uuid

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from src.services.storage.schemas.meta import Base


class Promo(Base):
    __tablename__ = "promos"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    is_active: Mapped[bool]
    duration: Mapped[int]
