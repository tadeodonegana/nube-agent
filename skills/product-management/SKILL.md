---
name: product-management
description: >
  How to manage products in a Tiendanube store: create, update, delete, list,
  and search products. Covers product structure, variant pricing, stock
  management, attributes, and best practices.
---

# Product Management

## Product Structure

A product in Tiendanube has:
- **name** and **description**: Multilingual objects (`{"es": "..."}`). Always use `es` key for Spanish.
- **attributes**: List of option names (e.g., Talla, Color). Max 3 per product.
- **variants**: Every product has at least one variant. Prices and stock live on variants, not on the product itself.
- **images**: Attached via the images endpoint, not inline on the product.
- **categories**: A product can belong to multiple categories.
- **published**: Boolean controlling store visibility.
- **tags**, **brand**, **handle**: Optional metadata.

## Key Rules

1. **Prices are on variants, not products.** To set a price, include it in the variant data.
2. **Stock is on variants.** Each variant tracks its own stock independently.
3. **A product must have at least one variant.** Deleting the last variant is not allowed.
4. **Max 1000 products per page** when listing (use `per_page` param, default 10).

## Attributes and Variants (CRITICAL)

Products have an `attributes` array that defines option names (e.g., `[{"es": "Talla"}, {"es": "Color"}]`).
Each variant has a `values` array. **The number of values MUST equal the number of attributes.**

- Product with 0 attributes → variants must have 0 values (`values: []`)
- Product with 1 attribute (e.g., Talla) → each variant needs exactly 1 value
- Product with 2 attributes (e.g., Talla + Color) → each variant needs exactly 2 values

### Creating a product WITH options from the start

Include `attributes` and matching `values` in variants:
```json
{
  "name": {"es": "Remera"},
  "attributes": [{"es": "Talla"}, {"es": "Color"}],
  "variants": [
    {"price": "100.00", "stock": 10, "values": [{"es": "S"}, {"es": "Rojo"}]},
    {"price": "100.00", "stock": 5, "values": [{"es": "M"}, {"es": "Azul"}]}
  ]
}
```

### Adding options to an EXISTING product that has none

This is a multi-step process:
1. **Update the product** to add attributes: `update_product(id, '{"attributes": [{"es": "Talla"}]}')`
2. **Update the existing variant** to set its value: `update_variant(product_id, variant_id, '{"values": [{"es": "Única"}]}')`
3. **Now create new variants** with matching values: `create_variant(product_id, '{"price": "...", "values": [{"es": "S"}]}')`

Skipping step 1 or 2 will cause a 422 error: "The values has the wrong number of elements."

## Creation Pattern (simple product, no options)

To create a product with a price of $100 and stock of 10:
```json
{
  "name": {"es": "Mi Producto"},
  "variants": [{"price": "100.00", "stock": 10}]
}
```

## Search and Filtering

When listing products, you can filter by:
- `page` and `per_page` for pagination
- The API returns products sorted by most recent by default

## Common Operations

- **Update price**: Use `update_variant` on the product's variant, not `update_product`.
- **Change visibility**: Use `update_product` with `{"published": false}`.
- **Add options (size/color)**: See "Adding options to an EXISTING product" above. You MUST first add attributes to the product, then update the existing variant's values, then create new variants.
