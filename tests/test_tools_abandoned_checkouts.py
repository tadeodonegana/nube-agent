import json

import respx

from nube_agent.config import BASE_URL
from nube_agent.tools.abandoned_checkouts import (
    get_abandoned_checkout,
    list_abandoned_checkouts,
)


class TestListAbandonedCheckouts:
    @respx.mock
    def test_basic_list(self):
        respx.get(f"{BASE_URL}/checkouts").respond(200, json=[{"id": 1}])
        result = json.loads(list_abandoned_checkouts())
        assert len(result) == 1

    @respx.mock
    def test_with_date_filters(self):
        route = respx.get(f"{BASE_URL}/checkouts").respond(200, json=[])
        list_abandoned_checkouts(created_at_min="2025-01-01", created_at_max="2025-12-31")
        params = route.calls[0].request.url.params
        assert params["created_at_min"] == "2025-01-01"
        assert params["created_at_max"] == "2025-12-31"

    @respx.mock
    def test_pagination_clamping(self):
        route = respx.get(f"{BASE_URL}/checkouts").respond(200, json=[])
        list_abandoned_checkouts(page=0, per_page=500)
        assert route.calls[0].request.url.params["page"] == "1"
        assert route.calls[0].request.url.params["per_page"] == "200"


class TestGetAbandonedCheckout:
    @respx.mock
    def test_returns_checkout(self):
        respx.get(f"{BASE_URL}/checkouts/300").respond(
            200, json={"id": 300, "abandoned_checkout_url": "https://recover.me"}
        )
        result = json.loads(get_abandoned_checkout(300))
        assert result["id"] == 300
        assert "recover" in result["abandoned_checkout_url"]
