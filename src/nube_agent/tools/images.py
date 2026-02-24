from nube_agent.api import parse_json, request, to_json


def list_images(product_id: int) -> str:
    """List all images of a product.

    Args:
        product_id: The numeric product ID.

    Returns a JSON list of images with id, src, position, and alt text.
    """
    result = request("GET", f"/products/{product_id}/images")
    return to_json(result)


def add_image(product_id: int, src: str, position: int = 1) -> str:
    """Add an image to a product from a URL.

    Args:
        product_id: The numeric product ID.
        src: Public URL of the image to add.
        position: Display position (1 = main image, default 1).

    Returns the created image data.
    """
    body = {"src": src, "position": position}
    result = request("POST", f"/products/{product_id}/images", json_body=body)
    return to_json(result)


def update_image(product_id: int, image_id: int, updates_json: str) -> str:
    """Update an existing product image.

    Args:
        product_id: The numeric product ID.
        image_id: The numeric image ID.
        updates_json: JSON string with fields to update.
            Supported: position (int), alt (str), src (str).
            Example: '{"position": 2, "alt": "Product side view"}'

    Returns the updated image data.
    """
    body = parse_json(updates_json, "updates_json")
    if isinstance(body, str):
        return body
    result = request("PUT", f"/products/{product_id}/images/{image_id}", json_body=body)
    return to_json(result)


def delete_image(product_id: int, image_id: int) -> str:
    """Delete an image from a product. This action is irreversible.

    Args:
        product_id: The numeric product ID.
        image_id: The numeric image ID to delete.

    Returns confirmation of deletion.
    """
    result = request("DELETE", f"/products/{product_id}/images/{image_id}")
    return to_json(result)
