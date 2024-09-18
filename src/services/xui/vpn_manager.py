import json
import uuid

from datetime import datetime
from typing import Any

from dateutil.relativedelta import relativedelta

from src.services.xui.i_vpn_manager import IVpnManager
from src.services.xui.requests import statuses


class VpnManager(IVpnManager):

    async def add_client(
            self,
            connection_id: uuid.UUID,
            user_email: str,
            inbound_id: int = 1,
            total_gb: int = 0,
            duration_mouth: int = 1
    ) -> bool:
        expiry_time = datetime.now() + relativedelta(months=1)
        expiry_time = int(expiry_time.timestamp() * 1000)

        r = await self.request_handler.post(
            url=f"panel/api/inbounds/addClient",
            body=self.create_add_client_body(connection_id, user_email, expiry_time, inbound_id, total_gb)
        )
        if r.status != statuses.SUCCESS_200:
            return False
        r_body = json.loads(r.body)
        return r_body.get("success", False)

    @staticmethod
    def create_add_client_body(
            connection_id: uuid.UUID,
            user_email: str,
            expiry_time: int,
            inbound_id: int = 1,
            total_gb: int = 0,
    ) -> dict[str, Any]:
        return {
            "id": inbound_id,
            "settings": json.dumps({
                "clients":
                    [
                        {
                            "id": str(connection_id),
                            "flow": "",
                            "email": user_email,
                            "limitIp": 0,
                            "totalGB": total_gb,
                            "expiryTime": expiry_time,
                            "enable": True,
                            "tgId": "",
                            "subId": "",
                            "reset": 0
                        }
                    ]
                })
            }

