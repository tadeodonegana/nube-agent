import json

import respx

from nube_agent.config import BASE_URL
from nube_agent.tools.categories import (
    create_category,
    delete_category,
    get_category,
    list_categories,
    update_category,
)


class TestListCategories:
    @respx.mock
    def test_basic_list(self):
        respx.get(f"{BASE_URL}/categories").respond(200, json=[{"id": 1}])
        result = json.loads(list_categories())
        assert len(result) == 1

    @respx.mock
    def test_pagination_clamping(self):
        route = respx.get(f"{BASE_URL}/categories").respond(200, json=[])
        list_categories(page=0, per_page=999)
        assert route.calls[0].request.url.params["page"] == "1"
        assert route.calls[0].request.url.params["per_page"] == "200"


class TestGetCategory:
    @respx.mock
    def test_returns_category(self):
        respx.get(f"{BASE_URL}/categories/5").respond(200, json={"id": 5})
        result = json.loads(get_category(5))
        assert result["id"] == 5


class TestCreateCategory:
    @respx.mock
    def test_simple_create(self):
        respx.post(f"{BASE_URL}/categories").respond(201, json={"id": 10})
        result = json.loads(create_category("Ropa"))
        assert result["id"] == 10

    @respx.mock
    def test_with_parent(self):
        route = respx.post(f"{BASE_URL}/categories").respond(201, json={"id": 11})
        create_category("Remeras", parent_id=10)
        body = json.loads(route.calls[0].request.content)
        assert body["parent"] == 10


class TestUpdateCategory:
    @respx.mock
    def test_update(self):
        respx.put(f"{BASE_URL}/categories/5").respond(200, json={"id": 5})
        result = json.loads(update_category(5, '{"name": {"es": "Nuevo"}}'))
        assert result["id"] == 5

    def test_invalid_json(self):
        result = update_category(5, "bad")
        assert "Invalid JSON" in result


class TestDeleteCategory:
    @respx.mock
    def test_delete(self):
        respx.delete(f"{BASE_URL}/categories/5").respond(204)
        result = json.loads(delete_category(5))
        assert result["status"] == "success"
