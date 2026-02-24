from nube_agent.api import parse_json, request, to_json


def list_customers(
    page: int = 1,
    per_page: int = 10,
    q: str = "",
    created_at_min: str = "",
    created_at_max: str = "",
) -> str:
    """List customers with optional search and pagination.

    Args:
        page: Page number (default 1).
        per_page: Results per page, max 200 (default 10).
        q: Search by name, email, or identification number.
        created_at_min: Only customers created after this ISO 8601 date.
        created_at_max: Only customers created before this ISO 8601 date.

    Returns a JSON list of customers with id, name, email, phone,
    total_spent, last_order_id, etc.
    """
    params: dict = {"page": max(1, page), "per_page": max(1, min(per_page, 200))}
    if q:
        params["q"] = q
    if created_at_min:
        params["created_at_min"] = created_at_min
    if created_at_max:
        params["created_at_max"] = created_at_max
    result = request("GET", "/customers", params=params)
    return to_json(result)


def get_customer(customer_id: int) -> str:
    """Get detailed information about a single customer by their ID.

    Args:
        customer_id: The numeric customer ID.

    Returns full customer details including name, email, phone,
    addresses, total_spent, last_order_id, and timestamps.
    """
    result = request("GET", f"/customers/{customer_id}")
    return to_json(result)


def create_customer(
    name: str,
    email: str,
    phone: str = "",
    send_email_invite: bool = False,
) -> str:
    """Create a new customer.

    Args:
        name: Customer's full name.
        email: Customer's email address.
        phone: Optional phone number.
        send_email_invite: Whether to send an account invitation email.

    Returns the created customer data.
    """
    body: dict = {"name": name, "email": email}
    if phone:
        body["phone"] = phone
    body["send_email_invite"] = send_email_invite
    result = request("POST", "/customers", json_body=body)
    return to_json(result)


def update_customer(customer_id: int, updates_json: str) -> str:
    """Update an existing customer.

    Args:
        customer_id: The numeric customer ID.
        updates_json: JSON string with fields to update.
            Supported fields: name, email, phone, note.
            Example: '{"note": "VIP customer", "phone": "+5491155556666"}'

    Returns the updated customer data.
    """
    body = parse_json(updates_json, "updates_json")
    if isinstance(body, str):
        return body
    result = request("PUT", f"/customers/{customer_id}", json_body=body)
    return to_json(result)
