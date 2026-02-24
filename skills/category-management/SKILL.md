---
name: category-management
description: >
  How to manage categories in a Tiendanube store: create hierarchies,
  assign products to categories, and handle multilingual category names.
---

# Category Management

## Category Structure

A category has:
- **name** and **description**: Multilingual objects (keyed by the store's language, e.g. `{"es": "..."}` for Spanish stores).
- **parent**: Optional parent category ID for nesting (subcategories).
- **handle**: URL-friendly slug, auto-generated from name.
- **subcategories**: Count of child categories.

## Hierarchy

- Categories can be nested. Set `parent` to a category ID to create a subcategory.
- Top-level categories have no parent (or parent = null).
- A category can contain products and subcategories simultaneously.

## Multilingual Names

Names are keyed by the store's language. The `create_category` tool handles this automatically.

## Product Assignment

Products are assigned to categories through the product endpoint, not the category endpoint.
When creating or updating a product, include `"categories": [category_id_1, category_id_2]`
in the product body.

## Common Operations

- **Reorganize hierarchy**: Update a category's `parent` field to move it.
- **Rename**: Update `name` with new multilingual object.
- **Delete**: Deleting a category does NOT delete its products. Products remain but lose that category association.
