import json
import uuid

from datetime import datetime
from typing import Any

from dateutil.relativedelta import relativedelta

from src.services.vpn.exceptions import CreateVpnClientException
from src.services.vpn.i_vpn_manager import IVpnManager
from src.services.vpn.requests import statuses
from src.services.vpn.requests.request_handler import RequestHandler


class VpnManager(IVpnManager):

    async def add_client(
            self,
            connection_id: uuid.UUID,
            user_email: str,
            inbound_id: int = 1,
            total_gb: int = 0,
            duration_mouth: int = 1
    ) -> None:
        expiry_time = datetime.now() + relativedelta(months=1)
        expiry_time = int(expiry_time.timestamp() * 1000)

        r = await self.request_handler.post(
            url=f"panel/api/inbounds/addClient",
            body=self.create_add_client_body(connection_id, user_email, expiry_time, inbound_id, total_gb)
        )
        if r.status != statuses.SUCCESS_200:
            raise CreateVpnClientException(f"Create client failed, response: {r}")
        r_body = json.loads(r.body)
        if not r_body.get("success", False):
            raise CreateVpnClientException(f"Create client failed, response: {r}")

    async def add_client_with_connection_string(
            self,
            connection_id: uuid.UUID,
            user_email: str,
            inbound_id: int = 1,
            total_gb: int = 0,
            duration_mouth: int = 1
    ) -> str | None:
        """Create client with 3x api and return connection string to created connection"""
        await self.add_client(connection_id, user_email, inbound_id, total_gb, duration_mouth)
        return self.create_connection_link(connection_id, user_email)

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
                            "flow": "xtls-rprx-vision",
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

    def create_connection_link(
            self,
            connection_id: uuid.UUID,
            user_email: str
    ) -> str:
        return (f"vless://{connection_id}@{self.config.vpn_host}:433?"
                f"type=tcp&"
                f"security=reality&"
                f"pbk={self.config.vpn_pbk}&"
                f"fp=chrome&sni=google.com&"
                f"sid={self.config.vpn_sid}&"
                f"spx=%2F&flow=xtls-rprx-vision"
                f"#{user_email}")
