import json

import respx

from nube_agent.config import BASE_URL
from nube_agent.tools.variants import (
    bulk_update_stock_price,
    create_variant,
    delete_variant,
    get_variant,
    list_variants,
    update_variant,
)


class TestListVariants:
    @respx.mock
    def test_basic_list(self):
        respx.get(f"{BASE_URL}/products/1/variants").respond(200, json=[{"id": 10}])
        result = json.loads(list_variants(1))
        assert result[0]["id"] == 10


class TestGetVariant:
    @respx.mock
    def test_returns_variant(self):
        respx.get(f"{BASE_URL}/products/1/variants/10").respond(200, json={"id": 10})
        result = json.loads(get_variant(1, 10))
        assert result["id"] == 10


class TestCreateVariant:
    @respx.mock
    def test_create(self):
        respx.post(f"{BASE_URL}/products/1/variants").respond(
            201, json={"id": 11, "price": "100.00"}
        )
        result = json.loads(create_variant(1, '{"price": "100.00", "stock": 5}'))
        assert result["id"] == 11

    def test_invalid_json(self):
        result = create_variant(1, "bad")
        assert "Invalid JSON" in result


class TestUpdateVariant:
    @respx.mock
    def test_update(self):
        respx.put(f"{BASE_URL}/products/1/variants/10").respond(200, json={"id": 10})
        result = json.loads(update_variant(1, 10, '{"stock": 20}'))
        assert result["id"] == 10

    def test_invalid_json(self):
        result = update_variant(1, 10, "bad")
        assert "Invalid JSON" in result


class TestDeleteVariant:
    @respx.mock
    def test_delete(self):
        respx.delete(f"{BASE_URL}/products/1/variants/10").respond(204)
        result = json.loads(delete_variant(1, 10))
        assert result["status"] == "success"


class TestBulkUpdateStockPrice:
    @respx.mock
    def test_bulk_update(self):
        respx.put(f"{BASE_URL}/products/1/variants/10").respond(200, json={"id": 10})
        respx.put(f"{BASE_URL}/products/1/variants/11").respond(200, json={"id": 11})
        result = json.loads(
            bulk_update_stock_price(
                1, '[{"variant_id": 10, "price": "99"}, {"variant_id": 11, "stock": 50}]'
            )
        )
        assert len(result) == 2

    def test_not_a_list(self):
        result = bulk_update_stock_price(1, '{"variant_id": 10}')
        assert "must be a JSON array" in result

    def test_invalid_json(self):
        result = bulk_update_stock_price(1, "bad")
        assert "Invalid JSON" in result

    @respx.mock
    def test_missing_variant_id(self):
        result = json.loads(bulk_update_stock_price(1, '[{"price": "99"}]'))
        assert result[0]["error"] == "Missing 'variant_id' in item"
