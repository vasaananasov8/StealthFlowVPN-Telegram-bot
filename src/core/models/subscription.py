from datetime import datetime

from pydantic import BaseModel


class Subscription(BaseModel):
    id: int
    user_id: int
    last_payment: int
    sale: int
    until: datetime
    active_links: int
    is_active: bool
