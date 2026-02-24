import json

import respx

from nube_agent.config import BASE_URL
from nube_agent.tools.images import add_image, delete_image, list_images, update_image


class TestListImages:
    @respx.mock
    def test_basic_list(self):
        respx.get(f"{BASE_URL}/products/1/images").respond(200, json=[{"id": 100}])
        result = json.loads(list_images(1))
        assert result[0]["id"] == 100


class TestAddImage:
    @respx.mock
    def test_add(self):
        route = respx.post(f"{BASE_URL}/products/1/images").respond(
            201, json={"id": 101, "src": "https://img.com/a.jpg"}
        )
        result = json.loads(add_image(1, "https://img.com/a.jpg", position=2))
        assert result["id"] == 101
        body = json.loads(route.calls[0].request.content)
        assert body["position"] == 2


class TestUpdateImage:
    @respx.mock
    def test_update(self):
        respx.put(f"{BASE_URL}/products/1/images/100").respond(200, json={"id": 100})
        result = json.loads(update_image(1, 100, '{"alt": "Photo"}'))
        assert result["id"] == 100

    def test_invalid_json(self):
        result = update_image(1, 100, "bad")
        assert "Invalid JSON" in result


class TestDeleteImage:
    @respx.mock
    def test_delete(self):
        respx.delete(f"{BASE_URL}/products/1/images/100").respond(204)
        result = json.loads(delete_image(1, 100))
        assert result["status"] == "success"
