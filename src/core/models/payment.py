from datetime import datetime

from pydantic import BaseModel


class Payment(BaseModel):
    id: int
    user_id: int
    amount: float
    currency: str  # TODO: mby need enum
    dt: datetime
