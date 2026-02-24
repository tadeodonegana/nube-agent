import json

import respx

from nube_agent.config import BASE_URL
from nube_agent.tools.products import (
    create_product,
    delete_product,
    get_product,
    list_products,
    update_product,
)


class TestListProducts:
    @respx.mock
    def test_basic_list(self):
        respx.get(f"{BASE_URL}/products").respond(200, json=[{"id": 1}])
        result = json.loads(list_products())
        assert len(result) == 1

    @respx.mock
    def test_pagination_clamping(self):
        route = respx.get(f"{BASE_URL}/products").respond(200, json=[])
        list_products(page=-1, per_page=500)
        assert route.calls[0].request.url.params["page"] == "1"
        assert route.calls[0].request.url.params["per_page"] == "200"


class TestGetProduct:
    @respx.mock
    def test_returns_product(self):
        respx.get(f"{BASE_URL}/products/42").respond(200, json={"id": 42, "name": {"es": "Test"}})
        result = json.loads(get_product(42))
        assert result["id"] == 42


class TestCreateProduct:
    @respx.mock
    def test_simple_create(self):
        respx.post(f"{BASE_URL}/products").respond(201, json={"id": 1, "name": {"es": "Remera"}})
        result = json.loads(create_product("Remera"))
        assert result["id"] == 1

    def test_invalid_variants_json(self):
        result = create_product("Remera", variants_json="not json")
        assert "Invalid JSON" in result


class TestUpdateProduct:
    @respx.mock
    def test_update(self):
        respx.put(f"{BASE_URL}/products/1").respond(200, json={"id": 1})
        result = json.loads(update_product(1, '{"published": false}'))
        assert result["id"] == 1

    def test_invalid_json(self):
        result = update_product(1, "bad")
        assert "Invalid JSON" in result


class TestDeleteProduct:
    @respx.mock
    def test_delete(self):
        respx.delete(f"{BASE_URL}/products/1").respond(204)
        result = json.loads(delete_product(1))
        assert result["status"] == "success"
