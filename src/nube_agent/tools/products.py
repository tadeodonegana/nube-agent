from nube_agent.api import parse_json, request, store_language, to_json


def list_products(page: int = 1, per_page: int = 10) -> str:
    """List products in the store with pagination.

    Args:
        page: Page number (default 1).
        per_page: Products per page, max 200 (default 10).

    Returns a JSON list of products with id, name, variants, price, stock, etc.
    """
    params = {"page": max(1, page), "per_page": max(1, min(per_page, 200))}
    result = request("GET", "/products", params=params)
    return to_json(result)


def get_product(product_id: int) -> str:
    """Get detailed information about a single product by its ID.

    Args:
        product_id: The numeric product ID.

    Returns full product details including name, description, variants,
    images, categories, and all attributes.
    """
    result = request("GET", f"/products/{product_id}")
    return to_json(result)


def create_product(
    name: str,
    variants_json: str = "",
    description: str = "",
    attributes_json: str = "",
    published: bool = True,
) -> str:
    """Create a new product in the store.

    Args:
        name: Product name in the store's language.
        variants_json: Optional JSON string with a list of variant objects.
            Each variant can have: price, stock, sku, weight, width, height, depth,
            and values (list of {lang: "value"} matching the product attributes,
            where lang is the store's language key).
            Example without options: '[{"price": "100.00", "stock": 10}]'
            Example with options:
            '[{"price": "100.00", "stock": 10, "values": [{"es": "S"}, {"es": "Rojo"}]}]'
            If empty, a single default variant is created.
        description: Optional product description in the store's language (HTML allowed).
        attributes_json: Optional JSON string with a list of attribute name objects.
            These define variant option names (e.g., Talla, Color). Max 3.
            Example: '[{"es": "Talla"}, {"es": "Color"}]'
            IMPORTANT: If attributes are set, every variant MUST have a matching
            number of values. E.g., 2 attributes = 2 values per variant.
        published: Whether the product is visible in the store (default true).

    Returns the created product data.
    """
    lang = store_language()
    body: dict = {
        "name": {lang: name},
        "published": published,
    }
    if description:
        body["description"] = {lang: description}
    if attributes_json:
        parsed = parse_json(attributes_json, "attributes_json")
        if isinstance(parsed, str):
            return parsed
        body["attributes"] = parsed
    if variants_json:
        parsed = parse_json(variants_json, "variants_json")
        if isinstance(parsed, str):
            return parsed
        body["variants"] = parsed
    result = request("POST", "/products", json_body=body)
    return to_json(result)


def update_product(product_id: int, updates_json: str) -> str:
    """Update an existing product.

    Args:
        product_id: The numeric product ID to update.
        updates_json: JSON string with fields to update.
            Supported fields: name ({lang: "..."}), description ({lang: "..."}),
            published (bool), tags, brand, handle, attributes (list of {lang: "..."}),
            where lang is the store's language key.
            Example: '{"name": {"es": "New Name"}, "published": false}'
            To add variant options: '{"attributes": [{"es": "Talla"}]}'
            IMPORTANT: After adding attributes, update existing variants to set
            their values too, or new variant creation will fail with 422.

    Returns the updated product data.
    """
    body = parse_json(updates_json, "updates_json")
    if isinstance(body, str):
        return body
    result = request("PUT", f"/products/{product_id}", json_body=body)
    return to_json(result)


def delete_product(product_id: int) -> str:
    """Delete a product from the store. This action is irreversible.

    Args:
        product_id: The numeric product ID to delete.

    Returns confirmation of deletion.
    """
    result = request("DELETE", f"/products/{product_id}")
    return to_json(result)
