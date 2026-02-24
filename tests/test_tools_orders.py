import json

import respx

from nube_agent.config import BASE_URL
from nube_agent.tools.orders import (
    cancel_order,
    close_order,
    get_order,
    list_orders,
    open_order,
    update_order,
)


class TestListOrders:
    @respx.mock
    def test_basic_list(self):
        respx.get(f"{BASE_URL}/orders").respond(200, json=[{"id": 1}])
        result = json.loads(list_orders())
        assert len(result) == 1

    @respx.mock
    def test_with_filters(self):
        route = respx.get(f"{BASE_URL}/orders").respond(200, json=[])
        list_orders(status="open", payment_status="paid", q="test@example.com")
        params = route.calls[0].request.url.params
        assert params["status"] == "open"
        assert params["payment_status"] == "paid"
        assert params["q"] == "test@example.com"

    @respx.mock
    def test_pagination_clamping(self):
        route = respx.get(f"{BASE_URL}/orders").respond(200, json=[])
        list_orders(page=-5, per_page=300)
        assert route.calls[0].request.url.params["page"] == "1"
        assert route.calls[0].request.url.params["per_page"] == "200"


class TestGetOrder:
    @respx.mock
    def test_returns_order(self):
        respx.get(f"{BASE_URL}/orders/100").respond(200, json={"id": 100})
        result = json.loads(get_order(100))
        assert result["id"] == 100


class TestUpdateOrder:
    @respx.mock
    def test_update(self):
        respx.put(f"{BASE_URL}/orders/100").respond(200, json={"id": 100})
        result = json.loads(update_order(100, '{"owner_note": "VIP"}'))
        assert result["id"] == 100

    def test_invalid_json(self):
        result = update_order(100, "bad")
        assert "Invalid JSON" in result


class TestCloseOrder:
    @respx.mock
    def test_close(self):
        respx.post(f"{BASE_URL}/orders/100/close").respond(
            200, json={"id": 100, "status": "closed"}
        )
        result = json.loads(close_order(100))
        assert result["status"] == "closed"


class TestOpenOrder:
    @respx.mock
    def test_open(self):
        respx.post(f"{BASE_URL}/orders/100/open").respond(200, json={"id": 100, "status": "open"})
        result = json.loads(open_order(100))
        assert result["status"] == "open"


class TestCancelOrder:
    @respx.mock
    def test_cancel(self):
        route = respx.post(f"{BASE_URL}/orders/100/cancel").respond(
            200, json={"id": 100, "status": "cancelled"}
        )
        result = json.loads(cancel_order(100, reason="customer", restock=True))
        assert result["status"] == "cancelled"
        body = json.loads(route.calls[0].request.content)
        assert body["reason"] == "customer"
        assert body["restock"] is True
