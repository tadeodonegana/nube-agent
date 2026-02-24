from nube_agent.api import parse_json, request, to_json


def list_pages(page: int = 1, per_page: int = 50) -> str:
    """List all content pages in the store.

    Args:
        page: Page number (default 1).
        per_page: Pages per page, max 200 (default 50).

    Returns a JSON list of pages with id, name, handle,
    published status, and timestamps.
    """
    params = {"page": max(1, page), "per_page": max(1, min(per_page, 200))}
    result = request("GET", "/pages", params=params)
    return to_json(result)


def get_page(page_id: int) -> str:
    """Get detailed information about a single page by its ID.

    Args:
        page_id: The numeric page ID.

    Returns full page details including localized name, handle,
    HTML content, SEO title, SEO description, and published status.
    """
    result = request("GET", f"/pages/{page_id}")
    return to_json(result)


def create_page(
    title_es: str,
    content_es: str,
    published: bool = True,
    seo_title_es: str = "",
    seo_description_es: str = "",
    seo_handle_es: str = "",
) -> str:
    """Create a new content page in the store.

    Args:
        title_es: Page title in Spanish.
        content_es: Page content in Spanish (HTML allowed).
        published: Whether the page is visible on the store (default true).
        seo_title_es: Optional SEO title for search engines.
        seo_description_es: Optional SEO meta description.
        seo_handle_es: Optional URL slug (e.g., "about-us"). Auto-generated if empty.

    Returns the created page data.
    """
    i18n: dict = {
        "es": {
            "title": title_es,
            "content": content_es,
        }
    }
    if seo_title_es:
        i18n["es"]["seo_title"] = seo_title_es
    if seo_description_es:
        i18n["es"]["seo_description"] = seo_description_es
    if seo_handle_es:
        i18n["es"]["seo_handle"] = seo_handle_es

    body = {
        "page": {
            "publish": published,
            "i18n": i18n,
        }
    }
    result = request("POST", "/pages", json_body=body)
    return to_json(result)


def update_page(page_id: int, updates_json: str) -> str:
    """Update an existing content page.

    Args:
        page_id: The numeric page ID.
        updates_json: JSON string with fields to update.
            Supported fields: title (str), content (str — HTML allowed).
            Example: '{"title": "Sobre Nosotros", "content": "<p>Somos...</p>"}'

    Returns the updated page data.
    """
    body = parse_json(updates_json, "updates_json")
    if isinstance(body, str):
        return body
    result = request("PUT", f"/pages/{page_id}", json_body=body)
    return to_json(result)


def delete_page(page_id: int) -> str:
    """Delete a content page. This action is irreversible.

    Args:
        page_id: The numeric page ID to delete.

    Returns confirmation of deletion.
    """
    result = request("DELETE", f"/pages/{page_id}")
    return to_json(result)
