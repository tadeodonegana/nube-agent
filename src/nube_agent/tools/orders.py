from nube_agent.api import parse_json, request, to_json


def list_orders(
    page: int = 1,
    per_page: int = 10,
    status: str = "",
    payment_status: str = "",
    shipping_status: str = "",
    q: str = "",
    created_at_min: str = "",
    created_at_max: str = "",
) -> str:
    """List orders with optional filters and pagination.

    Args:
        page: Page number (default 1).
        per_page: Results per page, max 200 (default 10).
        status: Filter by status — "open", "closed", or "cancelled".
        payment_status: Filter — "pending", "authorized", "paid",
            "abandoned", "refunded", "voided".
        shipping_status: Filter — "unpacked", "unfulfilled", "fulfilled".
        q: Search by order number, customer name, or email.
        created_at_min: Only orders created after this ISO 8601 date.
        created_at_max: Only orders created before this ISO 8601 date.

    Returns a JSON list of orders with id, number, status, total, customer, etc.
    """
    params: dict = {"page": max(1, page), "per_page": max(1, min(per_page, 200))}
    if status:
        params["status"] = status
    if payment_status:
        params["payment_status"] = payment_status
    if shipping_status:
        params["shipping_status"] = shipping_status
    if q:
        params["q"] = q
    if created_at_min:
        params["created_at_min"] = created_at_min
    if created_at_max:
        params["created_at_max"] = created_at_max
    result = request("GET", "/orders", params=params)
    return to_json(result)


def get_order(order_id: int) -> str:
    """Get detailed information about a single order by its ID.

    Args:
        order_id: The numeric order ID.

    Returns full order details including products, customer, payment,
    shipping, totals, notes, and timestamps.
    """
    result = request("GET", f"/orders/{order_id}")
    return to_json(result)


def update_order(order_id: int, updates_json: str) -> str:
    """Update an order's owner note or status.

    Args:
        order_id: The numeric order ID.
        updates_json: JSON string with fields to update.
            Supported fields: owner_note (str), status ("open"/"closed"/"cancelled").
            Example: '{"owner_note": "Customer requested gift wrapping"}'

    Returns the updated order data.
    """
    body = parse_json(updates_json, "updates_json")
    if isinstance(body, str):
        return body
    result = request("PUT", f"/orders/{order_id}", json_body=body)
    return to_json(result)


def close_order(order_id: int) -> str:
    """Close (archive) an order.

    Args:
        order_id: The numeric order ID.

    Returns the order with status set to "closed".
    """
    result = request("POST", f"/orders/{order_id}/close")
    return to_json(result)


def open_order(order_id: int) -> str:
    """Reopen a previously closed order.

    Args:
        order_id: The numeric order ID.

    Returns the order with status set to "open".
    """
    result = request("POST", f"/orders/{order_id}/open")
    return to_json(result)


def cancel_order(
    order_id: int,
    reason: str = "other",
    restock: bool = True,
    notify_customer: bool = True,
) -> str:
    """Cancel an order. This is a significant action — confirm with the user first.

    Args:
        order_id: The numeric order ID.
        reason: Cancellation reason — "customer", "inventory", "fraud", or "other".
        restock: Whether to return items to inventory (default true).
        notify_customer: Whether to send a cancellation email (default true).

    Returns the cancelled order data.
    """
    result = request(
        "POST",
        f"/orders/{order_id}/cancel",
        json_body={
            "reason": reason,
            "restock": restock,
            "email": notify_customer,
        },
    )
    return to_json(result)
