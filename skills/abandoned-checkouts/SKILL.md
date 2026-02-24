---
name: abandoned-checkouts
description: >
  How to view and recover abandoned checkouts in a Tiendanube store.
  Read-only access to carts where customers left before completing payment.
---

# Abandoned Checkouts

## What is an Abandoned Checkout?

An abandoned checkout is created when a customer reaches checkout step 2 (entered
contact info, chose shipping) but does not complete payment. These are available
for 30 days after creation.

## Checkout Properties

- **contact_email**, **contact_name**, **contact_phone**: Customer info.
- **products**: Array of items in the cart with name, price, quantity.
- **subtotal**, **discount**, **total**, **currency**: Cart totals.
- **abandoned_checkout_url**: Recovery link to send to the customer.
- **shipping/billing address**: Full address data.
- **payment_details**: What payment method they selected.
- **coupon**: Any coupon that was applied.
- **created_at**: When the checkout was abandoned.

## Key Rules

1. **Read-only** — you can list and view, but not modify abandoned checkouts.
2. **Recovery URL** is the key field — share it with the customer so they can resume.
3. **Available for 30 days** after creation.
4. Only created when the customer reached step 2 of checkout.

## Recovery Strategy

When a store owner asks about abandoned carts:
1. List recent abandoned checkouts.
2. Highlight the ones with the highest totals.
3. Provide the `abandoned_checkout_url` for each — the owner can send it to the customer via WhatsApp, email, etc.
4. Show contact info (email, phone) so the owner can reach out.
