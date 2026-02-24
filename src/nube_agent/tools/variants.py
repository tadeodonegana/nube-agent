from nube_agent.api import parse_json, request, to_json


def list_variants(product_id: int) -> str:
    """List all variants of a product.

    Args:
        product_id: The numeric product ID.

    Returns a JSON list of variants with id, price, stock, sku, values, etc.
    """
    result = request("GET", f"/products/{product_id}/variants")
    return to_json(result)


def get_variant(product_id: int, variant_id: int) -> str:
    """Get detailed information about a specific variant.

    Args:
        product_id: The numeric product ID.
        variant_id: The numeric variant ID.

    Returns full variant details including price, stock, sku, dimensions, weight.
    """
    result = request("GET", f"/products/{product_id}/variants/{variant_id}")
    return to_json(result)


def create_variant(product_id: int, variant_json: str) -> str:
    """Create a new variant for a product.

    IMPORTANT: The number of "values" MUST match the number of "attributes"
    defined on the product. If the product has 0 attributes, do NOT send values.
    If the product has 1 attribute (e.g., Talla), send exactly 1 value.
    If the product has no attributes yet, first use update_product to add them,
    then update the existing variant's values, then create new variants.

    Args:
        product_id: The numeric product ID.
        variant_json: JSON string with variant data.
            Fields: price (str), stock (int), sku (str), weight (str),
            width (str), height (str), depth (str),
            values (list of {lang: "value"} — must match product attributes count,
            where lang is the store's language key).
            Example (1 attribute): '{"price": "150.00", "stock": 5, "values": [{"es": "L"}]}'
            Example (2 attributes):
            '{"price": "150.00", "stock": 5, "values": [{"es": "Rojo"}, {"es": "L"}]}'

    Returns the created variant data.
    """
    body = parse_json(variant_json, "variant_json")
    if isinstance(body, str):
        return body
    result = request("POST", f"/products/{product_id}/variants", json_body=body)
    return to_json(result)


def update_variant(product_id: int, variant_id: int, updates_json: str) -> str:
    """Update an existing variant.

    Args:
        product_id: The numeric product ID.
        variant_id: The numeric variant ID.
        updates_json: JSON string with fields to update.
            Supported: price, stock, sku, weight, width, height, depth, values.
            Example: '{"price": "200.00", "stock": 20}'
            To set option values: '{"values": [{lang: "M"}]}'
            where lang is the store's language key.

    Returns the updated variant data.
    """
    body = parse_json(updates_json, "updates_json")
    if isinstance(body, str):
        return body
    result = request("PUT", f"/products/{product_id}/variants/{variant_id}", json_body=body)
    return to_json(result)


def delete_variant(product_id: int, variant_id: int) -> str:
    """Delete a variant from a product. A product must keep at least one variant.

    Args:
        product_id: The numeric product ID.
        variant_id: The numeric variant ID to delete.

    Returns confirmation of deletion.
    """
    result = request("DELETE", f"/products/{product_id}/variants/{variant_id}")
    return to_json(result)


def bulk_update_stock_price(product_id: int, updates_json: str) -> str:
    """Bulk update stock and/or price for multiple variants of a product.

    This iterates over variants and updates each one. Useful for changing
    prices or restocking all variants at once.

    Args:
        product_id: The numeric product ID.
        updates_json: JSON string with a list of objects, each having
            "variant_id" (int) and any of: "price" (str), "stock" (int).
            Example: '[{"variant_id": 123, "price": "99.00"}, {"variant_id": 456, "stock": 50}]'

    Returns a summary of all update results.
    """
    updates = parse_json(updates_json, "updates_json")
    if isinstance(updates, str):
        return updates
    if not isinstance(updates, list):
        return "Error: updates_json must be a JSON array, not a single object."
    results = []
    for item in updates:
        vid = item.get("variant_id")
        if not vid:
            results.append({"error": "Missing 'variant_id' in item", "item": item})
            continue
        body = {k: v for k, v in item.items() if k != "variant_id"}
        resp = request("PUT", f"/products/{product_id}/variants/{vid}", json_body=body)
        results.append({"variant_id": vid, "result": resp})
    return to_json(results)
