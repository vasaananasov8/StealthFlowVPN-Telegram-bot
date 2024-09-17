from typing import Any

from sqlalchemy import text

from src.services.storage.repository.interfaces.i_subscription_repository import IPostgresSubscriptionRepository
from src.services.storage.schemas.subscription import Subscription


class PostgresSubscriptionRepository(IPostgresSubscriptionRepository):
    async def get_user_subscription(self, user_id: int) -> dict[str, Any]:
        async with self.session() as s:
            query = text(f"SELECT * FROM subscriptions WHERE user_id = {user_id}")  # TODO: orm query + need fetch one
            res = await s.execute(query)
            res = res.mappings().all()
            return res[0] if len(res) == 1 else {}

    async def create_subscription(self, subscription: Subscription) -> None:
        async with self.session() as s:
            s.add(subscription)
            await s.commit()
