import uuid

from pydantic import BaseModel


class Promo(BaseModel):
    id: uuid.UUID
    is_active: bool
    duration: int
