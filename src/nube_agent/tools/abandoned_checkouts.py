from nube_agent.api import request, to_json


def list_abandoned_checkouts(
    page: int = 1,
    per_page: int = 10,
    created_at_min: str = "",
    created_at_max: str = "",
) -> str:
    """List abandoned checkouts (carts where the customer left before paying).

    These are created when a customer reaches checkout step 2 but does not
    complete the purchase. Useful for recovery campaigns.

    Args:
        page: Page number (default 1).
        per_page: Results per page, max 200 (default 10).
        created_at_min: Only checkouts created after this ISO 8601 date.
        created_at_max: Only checkouts created before this ISO 8601 date.

    Returns a JSON list of abandoned checkouts with id, contact_email,
    contact_name, products, total, abandoned_checkout_url, etc.
    The abandoned_checkout_url can be sent to the customer to recover the sale.
    """
    params: dict = {"page": max(1, page), "per_page": max(1, min(per_page, 200))}
    if created_at_min:
        params["created_at_min"] = created_at_min
    if created_at_max:
        params["created_at_max"] = created_at_max
    result = request("GET", "/checkouts", params=params)
    return to_json(result)


def get_abandoned_checkout(checkout_id: int) -> str:
    """Get detailed information about a single abandoned checkout.

    Args:
        checkout_id: The numeric checkout ID.

    Returns full checkout details including customer contact info,
    products, totals, shipping/billing addresses, payment details,
    and the recovery URL (abandoned_checkout_url).
    """
    result = request("GET", f"/checkouts/{checkout_id}")
    return to_json(result)
