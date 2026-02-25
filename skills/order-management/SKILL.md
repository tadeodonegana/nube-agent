---
name: order-management
description: >
  How to manage orders in a Tiendanube store: list, view, update, close,
  reopen, and cancel orders. Covers order statuses, filtering, payment
  and shipping status, and best practices.
---

# Order Management

## Order Structure

An order in Tiendanube has:
- **number**: Sequential identifier (starts at 100), shown to customers.
- **status**: "open", "closed", or "cancelled".
- **payment_status**: "pending", "authorized", "paid", "partially_paid", "abandoned", "refunded", "partially_refunded", "voided".
- **shipping_status**: "unpacked", "shipped", "unshipped", "delivered", "partially_packed", "partially_fulfilled".
- **products**: Array of line items with product_id, variant_id, name, price, quantity, sku.
- **customer**: Contact info (email, phone, name) and full customer object.
- **totals**: subtotal, total, total_usd, discount, currency.
- **shipping_address** and **billing_address**: Full address objects.
- **payment_details**: method, credit_card_company, installments.
- **owner_note**: Internal note visible only to the store owner.
- **note**: Note from the customer.
- **gateway**: Payment gateway used.
- **storefront**: Where the order came from — "store", "meli", "api", "form", "pos".

## Key Rules

1. **Orders are read-heavy.** You can list, view, close, reopen, and cancel — but you cannot change products or totals after creation.
2. **owner_note is the only free-text field** you can update via PUT.
3. **Cancelling an order** can optionally restock items and notify the customer.
4. **Cancelling is gated by the system** — just call cancel_order directly and the user will be prompted for approval automatically.

## Filtering Orders

The `list_orders` tool supports powerful filters:
- **status**: "open", "closed", "cancelled"
- **payment_status**: "pending", "paid", "refunded", etc.
- **shipping_status**: "unpacked", "unfulfilled", "fulfilled"
- **q**: Search by order number, customer name, or email
- **created_at_min/max**: Date range (ISO 8601)

### Common Queries
- Recent unpaid orders: `status=open, payment_status=pending`
- Orders ready to ship: `status=open, payment_status=paid, shipping_status=unpacked`
- All orders from a customer: `q=customer_email@example.com`

## Order Lifecycle

1. Customer checks out → order created with status "open"
2. Payment processed → payment_status changes to "paid"
3. Store packs & ships → shipping_status changes to "shipped"/"delivered"
4. Completed → store owner can close (archive) the order
5. If needed → cancel with reason, optional restock

## Common Operations

- **View recent orders**: `list_orders()` with default params
- **Find a specific order**: `list_orders(q="order_number_or_email")`
- **Add internal note**: `update_order(id, '{"owner_note": "..."}')`
- **Archive completed order**: `close_order(id)`
- **Cancel with restock**: `cancel_order(id, reason="customer", restock=True)`
