from pydantic import BaseModel


class Promo(BaseModel):
    id: str
    is_active: bool
    duration: int
