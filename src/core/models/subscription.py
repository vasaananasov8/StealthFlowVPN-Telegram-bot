from datetime import datetime

from pydantic import BaseModel

from src.services.storage.schemas.subscription import Subscription as DbSubscription


class Subscription(BaseModel):
    id: int | None
    user_id: int
    last_payment: int | None
    sale: int
    until: datetime
    active_links: int
    is_active: bool

    def get_db_subscription_model(self) -> DbSubscription:
        return DbSubscription(
            id=self.id,
            user_id=self.user_id,
            last_payment=self.last_payment,
            sale=self.sale,
            until=self.until,
            active_links=self.active_links,
            is_active=self.is_active
        )