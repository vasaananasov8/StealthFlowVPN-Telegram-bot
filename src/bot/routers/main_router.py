from aiogram import Router
from src.bot.routers.user.start import router as start_router
from src.bot.routers.user.get_vpn import router as get_vpn_router
from src.bot.routers.user.user_stats import router as user_stats_router

def get_main_router() -> Router:
    router = Router(name="Main router")
    router.include_routers(
        start_router,
        get_vpn_router,
        user_stats_router
    )

    return router
