from nube_agent.api import parse_json, request, store_language, to_json


def list_categories(page: int = 1, per_page: int = 50) -> str:
    """List all categories in the store with pagination.

    Args:
        page: Page number (default 1).
        per_page: Categories per page, max 200 (default 50).

    Returns a JSON list of categories with id, name, parent, subcategories count.
    """
    params = {"page": max(1, page), "per_page": max(1, min(per_page, 200))}
    result = request("GET", "/categories", params=params)
    return to_json(result)


def get_category(category_id: int) -> str:
    """Get detailed information about a single category.

    Args:
        category_id: The numeric category ID.

    Returns full category details including name, description, parent, handle.
    """
    result = request("GET", f"/categories/{category_id}")
    return to_json(result)


def create_category(name: str, parent_id: int = 0, description: str = "") -> str:
    """Create a new category in the store.

    Args:
        name: Category name in the store's language.
        parent_id: Optional parent category ID for subcategories (0 for top-level).
        description: Optional description in the store's language.

    Returns the created category data.
    """
    lang = store_language()
    body: dict = {"name": {lang: name}}
    if parent_id != 0:
        body["parent"] = parent_id
    if description:
        body["description"] = {lang: description}
    result = request("POST", "/categories", json_body=body)
    return to_json(result)


def update_category(category_id: int, updates_json: str) -> str:
    """Update an existing category.

    Args:
        category_id: The numeric category ID to update.
        updates_json: JSON string with fields to update.
            Supported fields: name ({lang: "..."}), description ({lang: "..."}),
            parent (int), handle (str), where lang is the store's language key.
            Example: '{"name": {"es": "New Name"}}'

    Returns the updated category data.
    """
    body = parse_json(updates_json, "updates_json")
    if isinstance(body, str):
        return body
    result = request("PUT", f"/categories/{category_id}", json_body=body)
    return to_json(result)


def delete_category(category_id: int) -> str:
    """Delete a category from the store. This action is irreversible.

    Args:
        category_id: The numeric category ID to delete.

    Returns confirmation of deletion.
    """
    result = request("DELETE", f"/categories/{category_id}")
    return to_json(result)
