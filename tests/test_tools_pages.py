import json

import respx

from nube_agent import api as api_mod
from nube_agent.config import BASE_URL
from nube_agent.tools.pages import (
    create_page,
    delete_page,
    get_page,
    list_pages,
    update_page,
)

STORE_RESPONSE = {"main_language": "es", "country": "AR"}


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
        assert route.calls[0].request.url.params["per_page"] == "20"


class TestGetPage:
    @respx.mock
    def test_returns_page(self):
        respx.get(f"{BASE_URL}/pages/7").respond(
            200, json={"id": 7, "name": {"es": "Sobre Nosotros"}}
        )
        result = json.loads(get_page(7))
        assert result["id"] == 7


class TestCreatePage:
    def setup_method(self):
        api_mod._store_info.cache_clear()

    @respx.mock
    def test_create(self):
        respx.get(f"{BASE_URL}/store").respond(200, json=STORE_RESPONSE)
        route = respx.post(f"{BASE_URL}/pages").respond(201, json={"id": 8})
        result = json.loads(create_page("FAQ", "<p>Preguntas</p>"))
        assert result["id"] == 8
        body = json.loads(route.calls[0].request.content)
        assert body["page"]["i18n"]["es_AR"]["title"] == "FAQ"
        assert body["page"]["i18n"]["es_AR"]["content"] == "<p>Preguntas</p>"

    @respx.mock
    def test_create_with_seo(self):
        respx.get(f"{BASE_URL}/store").respond(200, json=STORE_RESPONSE)
        route = respx.post(f"{BASE_URL}/pages").respond(201, json={"id": 9})
        create_page("FAQ", "<p>Q</p>", seo_title="FAQ SEO", seo_handle="faq")
        body = json.loads(route.calls[0].request.content)
        assert body["page"]["i18n"]["es_AR"]["seo_title"] == "FAQ SEO"
        assert body["page"]["i18n"]["es_AR"]["seo_handle"] == "faq"


class TestUpdatePage:
    def setup_method(self):
        api_mod._store_info.cache_clear()

    @respx.mock
    def test_update(self):
        respx.get(f"{BASE_URL}/store").respond(200, json=STORE_RESPONSE)
        route = respx.put(f"{BASE_URL}/pages/7").respond(200, json={"id": 7})
        result = json.loads(update_page(7, '{"title": "Updated", "content": "<p>Hi</p>"}'))
        assert result["id"] == 7
        body = json.loads(route.calls[0].request.content)
        assert body["page"]["i18n"]["es_AR"]["title"] == "Updated"
        assert body["page"]["i18n"]["es_AR"]["content"] == "<p>Hi</p>"

    @respx.mock
    def test_update_with_published(self):
        respx.get(f"{BASE_URL}/store").respond(200, json=STORE_RESPONSE)
        route = respx.put(f"{BASE_URL}/pages/7").respond(200, json={"id": 7})
        update_page(7, '{"title": "T", "published": true}')
        body = json.loads(route.calls[0].request.content)
        assert body["page"]["publish"] is True
        assert body["page"]["i18n"]["es_AR"]["title"] == "T"

    def test_invalid_json(self):
        result = update_page(7, "bad")
        assert "Invalid JSON" in result


class TestDeletePage:
    @respx.mock
    def test_delete(self):
        respx.delete(f"{BASE_URL}/pages/7").respond(204)
        result = json.loads(delete_page(7))
        assert result["status"] == "success"
