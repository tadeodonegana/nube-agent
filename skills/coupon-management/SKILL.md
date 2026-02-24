---
name: coupon-management
description: >
  How to manage discount coupons in a Tiendanube store: create, update,
  delete, and list coupons. Covers coupon types, restrictions, and
  promotion strategies.
---

# Coupon Management

## Coupon Structure

A coupon in Tiendanube has:
- **code**: The text customers enter at checkout (e.g., "SUMMER20").
- **type**: "percentage", "absolute", or "shipping".
- **value**: Discount amount (percentage number or absolute amount in store currency).
- **valid**: Whether the coupon is currently active.
- **start_date** / **end_date**: Active date range (ISO 8601).
- **max_uses**: Maximum number of redemptions (0 = unlimited).
- **used**: Current redemption count (read-only).
- **min_price**: Minimum cart value required.
- **categories**: Restrict to specific category IDs.
- **products**: Restrict to specific product IDs.
- **includes_shipping**: Whether discount applies to shipping too.
- **first_consumer_purchase**: Only for first-time customers.
- **combines_with_other_discounts**: Whether it stacks.

## Coupon Types

1. **percentage**: Percentage off (e.g., value "20" = 20% off).
2. **absolute**: Fixed amount off in store currency (e.g., value "500" = $500 off).
3. **shipping**: Free shipping (value field is ignored).

## Common Promotion Patterns

- **Site-wide 20% off**: `type=percentage, value=20, code=SALE20`
- **$1000 off for new customers**: `type=absolute, value=1000, first_consumer_purchase=true`
- **Free shipping over $5000**: `type=shipping, min_price=5000`
- **Category-specific**: Set `categories` to restrict discount to specific categories.
- **Limited time**: Set `start_date` and `end_date`.
- **Limited uses**: Set `max_uses` (e.g., first 100 customers).

## Common Operations

- **List active coupons**: `list_coupons(valid="true")`
- **Create a promo**: `create_coupon(code, type, value, ...)`
- **Deactivate a coupon**: `update_coupon(id, '{"valid": false}')`
- **Check usage**: Look at `used` vs `max_uses` in coupon details.
- **Delete expired coupon**: `delete_coupon(id)`
