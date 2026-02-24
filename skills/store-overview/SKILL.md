---
name: store-overview
description: >
  Information about the Tiendanube store configuration: name, contact info,
  domains, plan details, and general settings. Read-only data.
---

# Store Overview

## Available Information

The store info endpoint (`GET /`) returns:
- **name**: Store display name
- **description**: Store description
- **email**: Contact email
- **phone**: Contact phone
- **address**: Physical address
- **domains**: List of domains (custom and `.mitiendanube.com`)
- **plan_name**: Current subscription plan
- **country**: Store country code
- **currency**: Store currency
- **languages**: Supported languages
- **created_at**: Store creation date

## Read-Only Nature

Store information is **read-only** through the API. To change store settings
(name, email, plan, etc.), the merchant must use the Tiendanube admin panel.

## Common Use Cases

- Verify API connectivity by fetching store info.
- Check which domains are configured.
- Confirm the store's currency before creating products with prices.
- View the store's plan to understand feature availability.
