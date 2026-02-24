import json

import respx

from nube_agent.config import BASE_URL
from nube_agent.tools.pages import (
    create_page,
    delete_page,
    get_page,
    list_pages,
    update_page,
)


class TestListPages:
    @respx.mock
    def test_basic_list(self):
        respx.get(f"{BASE_URL}/pages").respond(200, json=[{"id": 1}])
        result = json.loads(list_pages())
        assert len(result) == 1

    @respx.mock
    def test_pagination_clamping(self):
        route = respx.get(f"{BASE_URL}/pages").respond(200, json=[])
        list_pages(page=-1, per_page=999)
        assert route.calls[0].request.url.params["page"] == "1"
        assert route.calls[0].request.url.params["per_page"] == "200"


class TestGetPage:
    @respx.mock
    def test_returns_page(self):
        respx.get(f"{BASE_URL}/pages/7").respond(
            200, json={"id": 7, "name": {"es": "Sobre Nosotros"}}
        )
        result = json.loads(get_page(7))
        assert result["id"] == 7


class TestCreatePage:
    @respx.mock
    def test_create(self):
        route = respx.post(f"{BASE_URL}/pages").respond(201, json={"id": 8})
        result = json.loads(create_page("FAQ", "<p>Preguntas</p>"))
        assert result["id"] == 8
        body = json.loads(route.calls[0].request.content)
        assert body["page"]["i18n"]["es"]["title"] == "FAQ"
        assert body["page"]["i18n"]["es"]["content"] == "<p>Preguntas</p>"

    @respx.mock
    def test_create_with_seo(self):
        route = respx.post(f"{BASE_URL}/pages").respond(201, json={"id": 9})
        create_page("FAQ", "<p>Q</p>", seo_title_es="FAQ SEO", seo_handle_es="faq")
        body = json.loads(route.calls[0].request.content)
        assert body["page"]["i18n"]["es"]["seo_title"] == "FAQ SEO"
        assert body["page"]["i18n"]["es"]["seo_handle"] == "faq"


class TestUpdatePage:
    @respx.mock
    def test_update(self):
        respx.put(f"{BASE_URL}/pages/7").respond(200, json={"id": 7})
        result = json.loads(update_page(7, '{"title": "Updated"}'))
        assert result["id"] == 7

    def test_invalid_json(self):
        result = update_page(7, "bad")
        assert "Invalid JSON" in result


class TestDeletePage:
    @respx.mock
    def test_delete(self):
        respx.delete(f"{BASE_URL}/pages/7").respond(204)
        result = json.loads(delete_page(7))
        assert result["status"] == "success"
