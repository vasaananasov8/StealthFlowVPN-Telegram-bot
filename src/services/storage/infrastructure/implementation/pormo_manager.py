from src.core.models.promo import Promo
from src.services.storage.infrastructure.exceptions import PromoInvalidId
from src.services.storage.infrastructure.interfaces.i_promo_manager import IPromoManager, PromoCheckResult, \
    PromoCheckValue


class PromoManager(IPromoManager):

    async def get_promo(self, _id: str) -> Promo | None:
        """
        :raise: PromoInvalidId - if invalid id
        """
        result = await self.promo_repository.get_promo(self.convert_str_to_uuid(_id))
        return Promo.model_validate(result)

    async def get_all_active_promos(self) -> list[Promo]:
        pass

    async def create_promos(self, promo_nums: int) -> list[str]:
        pass

    async def change_promo_activity(self, _id: str, new_value: bool) -> bool:
        try:
            await self.promo_repository.change_promo_activity(_id, new_value)
        except Exception:  # TODO Exceptions
            return False
        return True

    async def check_promo_is_valid(self, promo_id) -> PromoCheckResult:

        try:
            promo = await self.get_promo(promo_id)
        except PromoInvalidId:
            return PromoCheckResult(result=PromoCheckValue.INVALID_PROMO_CODE)

        if promo is None:
            return PromoCheckResult(result=PromoCheckValue.NO_PROMO)
        elif promo.is_active:
            return PromoCheckResult(result=PromoCheckValue.PROMO_ALREADY_ACTIVE)
        else:
            return PromoCheckResult(result=PromoCheckValue.VALID, promo=promo)
