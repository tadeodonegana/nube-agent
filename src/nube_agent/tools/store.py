from nube_agent.api import request, to_json


def get_store_info() -> str:
    """Get general information about the store.

    Returns store name, description, contact email, address, plan, domains,
    and other configuration details.
    """
    result = request("GET", "/store")
    return to_json(result)
