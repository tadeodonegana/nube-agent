from nube_agent.api import parse_json, request, to_json


def list_coupons(
    page: int = 1,
    per_page: int = 10,
    valid: str = "",
) -> str:
    """List discount coupons with optional filters.

    Args:
        page: Page number (default 1).
        per_page: Results per page, max 200 (default 10).
        valid: Filter by validity — "true" or "false". Empty = all.

    Returns a JSON list of coupons with id, code, type, value,
    start_date, end_date, max_uses, used, etc.
    """
    params: dict = {"page": max(1, page), "per_page": max(1, min(per_page, 200))}
    if valid:
        params["valid"] = valid
    result = request("GET", "/coupons", params=params)
    return to_json(result)


def get_coupon(coupon_id: int) -> str:
    """Get detailed information about a single coupon by its ID.

    Args:
        coupon_id: The numeric coupon ID.

    Returns full coupon details including code, type, value,
    dates, usage stats, product/category restrictions, etc.
    """
    result = request("GET", f"/coupons/{coupon_id}")
    return to_json(result)


def create_coupon(
    code: str,
    coupon_type: str,
    value: str = "",
    start_date: str = "",
    end_date: str = "",
    max_uses: int = 0,
    min_price: str = "",
    includes_shipping: bool = False,
    first_consumer_purchase: bool = False,
    categories_json: str = "",
    products_json: str = "",
) -> str:
    """Create a new discount coupon.

    Args:
        code: Coupon code that customers enter (e.g., "SUMMER20").
        coupon_type: Discount type — "percentage", "absolute", or "shipping".
            - percentage: value is a percentage (e.g., "20" for 20% off).
            - absolute: value is a fixed amount in store currency (e.g., "500").
            - shipping: free shipping coupon (value is ignored).
        value: Discount value (required for percentage and absolute types).
        start_date: When the coupon becomes active (ISO 8601). Empty = immediately.
        end_date: When the coupon expires (ISO 8601). Empty = no expiration.
        max_uses: Max number of times the coupon can be used. 0 = unlimited.
        min_price: Minimum cart value required to use the coupon.
        includes_shipping: Whether the discount also applies to shipping cost.
        first_consumer_purchase: Only allow first-time customers to use it.
        categories_json: Optional JSON list of category IDs to restrict the coupon to.
            Example: '[12345, 67890]'
        products_json: Optional JSON list of product IDs to restrict the coupon to.
            Example: '[111, 222]'

    Returns the created coupon data.
    """
    if coupon_type in ("percentage", "absolute") and not value:
        return f"Error: 'value' is required for coupon type '{coupon_type}'."
    body: dict = {"code": code, "type": coupon_type}
    if value:
        body["value"] = value
    if start_date:
        body["start_date"] = start_date
    if end_date:
        body["end_date"] = end_date
    if max_uses:
        body["max_uses"] = max_uses
    if min_price:
        body["min_price"] = min_price
    if includes_shipping:
        body["includes_shipping"] = includes_shipping
    if first_consumer_purchase:
        body["first_consumer_purchase"] = first_consumer_purchase
    if categories_json:
        parsed = parse_json(categories_json, "categories_json")
        if isinstance(parsed, str):
            return parsed
        body["categories"] = parsed
    if products_json:
        parsed = parse_json(products_json, "products_json")
        if isinstance(parsed, str):
            return parsed
        body["products"] = parsed
    result = request("POST", "/coupons", json_body=body)
    return to_json(result)


def update_coupon(coupon_id: int, updates_json: str) -> str:
    """Update an existing coupon.

    Args:
        coupon_id: The numeric coupon ID.
        updates_json: JSON string with fields to update.
            Supported: code, type, value, start_date, end_date,
            max_uses, min_price, valid, includes_shipping,
            first_consumer_purchase, categories, products.
            Example: '{"value": "30", "end_date": "2025-12-31T23:59:59"}'

    Returns the updated coupon data.
    """
    body = parse_json(updates_json, "updates_json")
    if isinstance(body, str):
        return body
    result = request("PUT", f"/coupons/{coupon_id}", json_body=body)
    return to_json(result)


def delete_coupon(coupon_id: int) -> str:
    """Delete a coupon. This action is irreversible.

    Args:
        coupon_id: The numeric coupon ID to delete.

    Returns confirmation of deletion.
    """
    result = request("DELETE", f"/coupons/{coupon_id}")
    return to_json(result)
