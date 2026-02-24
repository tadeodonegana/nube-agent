import json

import respx

from nube_agent.config import BASE_URL
from nube_agent.tools.coupons import (
    create_coupon,
    delete_coupon,
    get_coupon,
    list_coupons,
    update_coupon,
)


class TestListCoupons:
    @respx.mock
    def test_basic_list(self):
        respx.get(f"{BASE_URL}/coupons").respond(200, json=[{"id": 1}])
        result = json.loads(list_coupons())
        assert len(result) == 1

    @respx.mock
    def test_with_validity_filter(self):
        route = respx.get(f"{BASE_URL}/coupons").respond(200, json=[])
        list_coupons(valid="true")
        assert route.calls[0].request.url.params["valid"] == "true"

    @respx.mock
    def test_pagination_clamping(self):
        route = respx.get(f"{BASE_URL}/coupons").respond(200, json=[])
        list_coupons(page=-1, per_page=999)
        assert route.calls[0].request.url.params["page"] == "1"
        assert route.calls[0].request.url.params["per_page"] == "200"


class TestGetCoupon:
    @respx.mock
    def test_returns_coupon(self):
        respx.get(f"{BASE_URL}/coupons/20").respond(200, json={"id": 20, "code": "SALE20"})
        result = json.loads(get_coupon(20))
        assert result["code"] == "SALE20"


class TestCreateCoupon:
    @respx.mock
    def test_create_percentage(self):
        respx.post(f"{BASE_URL}/coupons").respond(201, json={"id": 21, "code": "NEW20"})
        result = json.loads(create_coupon("NEW20", "percentage", value="20"))
        assert result["id"] == 21

    def test_missing_value_for_percentage(self):
        result = create_coupon("BAD", "percentage")
        assert "Error" in result

    @respx.mock
    def test_shipping_type_no_value(self):
        respx.post(f"{BASE_URL}/coupons").respond(201, json={"id": 22, "code": "FREESHIP"})
        result = json.loads(create_coupon("FREESHIP", "shipping"))
        assert result["id"] == 22

    def test_invalid_categories_json(self):
        result = create_coupon("X", "percentage", value="10", categories_json="bad")
        assert "Invalid JSON" in result


class TestUpdateCoupon:
    @respx.mock
    def test_update(self):
        respx.put(f"{BASE_URL}/coupons/20").respond(200, json={"id": 20})
        result = json.loads(update_coupon(20, '{"value": "30"}'))
        assert result["id"] == 20

    def test_invalid_json(self):
        result = update_coupon(20, "bad")
        assert "Invalid JSON" in result


class TestDeleteCoupon:
    @respx.mock
    def test_delete(self):
        respx.delete(f"{BASE_URL}/coupons/20").respond(204)
        result = json.loads(delete_coupon(20))
        assert result["status"] == "success"
