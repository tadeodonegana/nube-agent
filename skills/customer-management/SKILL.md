---
name: customer-management
description: >
  How to manage customers in a Tiendanube store: list, view, create,
  and update customer profiles. Covers customer properties, search,
  and CRM notes.
---

# Customer Management

## Customer Structure

A customer in Tiendanube has:
- **name**, **email**, **phone**: Basic contact info.
- **identification**: ID document (CPF/CNPJ in Brazil, DNI in Argentina).
- **note**: Internal note from the store owner (CRM use).
- **default_address**: Primary shipping address.
- **addresses**: List of all shipping addresses.
- **billing_address/city/province/country/zipcode**: Billing info.
- **total_spent** and **total_spent_currency**: Lifetime spending.
- **last_order_id**: Most recent order reference.
- **active**: Whether the account is active.
- **accepts_marketing**: Email marketing consent (read-only).

## Key Rules

1. **Customers with orders cannot be deleted.** Only customers with zero orders can be removed.
2. **total_spent is read-only** — it's calculated from orders.
3. **accepts_marketing is read-only** — the customer controls this.
4. **note** is the best field for CRM tags and internal info.

## Search

The `list_customers` tool supports:
- **q**: Search by name, email, or identification number.
- **created_at_min/max**: Date range for registration date.

## Common Operations

- **Find a customer**: `list_customers(q="email_or_name")`
- **Add CRM note**: `update_customer(id, '{"note": "VIP - referred by Maria"}')`
- **Create new customer**: `create_customer(name, email, phone)`
- **Check spending**: Look at `total_spent` in customer details.
