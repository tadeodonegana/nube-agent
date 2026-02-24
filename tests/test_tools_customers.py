import json

import respx

from nube_agent.config import BASE_URL
from nube_agent.tools.customers import (
    create_customer,
    get_customer,
    list_customers,
    update_customer,
)


class TestListCustomers:
    @respx.mock
    def test_basic_list(self):
        respx.get(f"{BASE_URL}/customers").respond(200, json=[{"id": 1}])
        result = json.loads(list_customers())
        assert len(result) == 1

    @respx.mock
    def test_with_search(self):
        route = respx.get(f"{BASE_URL}/customers").respond(200, json=[])
        list_customers(q="maria@example.com")
        assert route.calls[0].request.url.params["q"] == "maria@example.com"

    @respx.mock
    def test_pagination_clamping(self):
        route = respx.get(f"{BASE_URL}/customers").respond(200, json=[])
        list_customers(page=0, per_page=500)
        assert route.calls[0].request.url.params["page"] == "1"
        assert route.calls[0].request.url.params["per_page"] == "200"


class TestGetCustomer:
    @respx.mock
    def test_returns_customer(self):
        respx.get(f"{BASE_URL}/customers/50").respond(200, json={"id": 50})
        result = json.loads(get_customer(50))
        assert result["id"] == 50


class TestCreateCustomer:
    @respx.mock
    def test_create(self):
        route = respx.post(f"{BASE_URL}/customers").respond(
            201, json={"id": 51, "name": "Maria"}
        )
        result = json.loads(create_customer("Maria", "maria@test.com", phone="+5491155550000"))
        assert result["id"] == 51
        body = json.loads(route.calls[0].request.content)
        assert body["phone"] == "+5491155550000"


class TestUpdateCustomer:
    @respx.mock
    def test_update(self):
        respx.put(f"{BASE_URL}/customers/50").respond(200, json={"id": 50})
        result = json.loads(update_customer(50, '{"note": "VIP"}'))
        assert result["id"] == 50

    def test_invalid_json(self):
        result = update_customer(50, "bad")
        assert "Invalid JSON" in result
