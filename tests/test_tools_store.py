import json

import respx

from nube_agent.config import BASE_URL
from nube_agent.tools.store import get_store_info


class TestGetStoreInfo:
    @respx.mock
    def test_returns_json(self):
        url = f"{BASE_URL}/store"
        respx.get(url).respond(200, json={"name": {"es": "Mi Tienda"}, "currency": "ARS"})
        result = get_store_info()
        data = json.loads(result)
        assert data["name"]["es"] == "Mi Tienda"
