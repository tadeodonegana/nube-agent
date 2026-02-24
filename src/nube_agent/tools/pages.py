from nube_agent.api import parse_json, request, store_locale, to_json


def list_pages(page: int = 1, per_page: int = 20) -> str:
    """List all content pages in the store.

    Args:
        page: Page number (default 1).
        per_page: Pages per page, max 20 (default 20).

    Returns a JSON list of pages with id, name, handle,
    published status, and timestamps.
    """
    params = {"page": max(1, page), "per_page": max(1, min(per_page, 20))}
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
    title: str,
    content: str,
    published: bool = True,
    seo_title: str = "",
    seo_description: str = "",
    seo_handle: str = "",
) -> str:
    """Create a new content page in the store.

    Args:
        title: Page title in the store's language.
        content: Page content in the store's language (HTML allowed).
        published: Whether the page is visible on the store (default true).
        seo_title: Optional SEO title for search engines.
        seo_description: Optional SEO meta description.
        seo_handle: Optional URL slug (e.g., "about-us"). Auto-generated if empty.

    Returns the created page data.
    """
    locale = store_locale()
    locale_data: dict = {
        "title": title,
        "content": content,
    }
    if seo_title:
        locale_data["seo_title"] = seo_title
    if seo_description:
        locale_data["seo_description"] = seo_description
    if seo_handle:
        locale_data["seo_handle"] = seo_handle
    i18n = {locale: locale_data}

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
            Supported fields: title (str), content (str — HTML allowed),
            published (bool), seo_title (str), seo_description (str),
            seo_handle (str).
            Example: '{"title": "Sobre Nosotros", "content": "<p>Somos...</p>"}'

    Returns the updated page data.
    """
    parsed = parse_json(updates_json, "updates_json")
    if isinstance(parsed, str):
        return parsed

    locale = store_locale()
    locale_data: dict = {}
    for key in ("title", "content", "seo_title", "seo_description", "seo_handle"):
        if key in parsed:
            locale_data[key] = parsed[key]

    body: dict = {"page": {}}
    if locale_data:
        body["page"]["i18n"] = {locale: locale_data}
    if "published" in parsed:
        body["page"]["publish"] = parsed["published"]

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
