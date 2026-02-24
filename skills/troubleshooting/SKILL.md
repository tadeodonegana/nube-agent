---
name: troubleshooting
description: >
  Troubleshooting guide for common API errors, especially permission and
  scope issues when the app lacks access to certain endpoints.
---

# Troubleshooting

## Permission Errors (403 Forbidden)

When an API call returns a **403** or a message about insufficient permissions,
it means the app does not have the required OAuth scopes for that operation.

### How to Fix

1. Go to the app settings on the Partners portal:
   https://partners.tiendanube.com/applications/update/{app_id}
   (replace {app_id} with the actual application ID)
2. Under "Scopes", enable the scopes needed for the failing operation.
3. **Reinstall the app** on the store. Updating scopes alone is not enough;
   the store must re-authorize so the new scopes take effect.

### Scope Reference

| Domain              | Read scope         | Write scope         |
|---------------------|--------------------|---------------------|
| Products            | read_products      | write_products      |
| Orders              | read_orders        | write_orders        |
| Customers           | read_customers     | write_customers     |
| Coupons             | read_coupons       | write_coupons       |
| Pages (Content)     | read_content       | write_content       |
| Categories          | read_products      | write_products      |
| Abandoned Checkouts | read_orders        | —                   |

### What to Tell the User

When you detect a 403 or permission error:
- Explain which scope is likely missing based on the operation that failed.
- Provide the Partners portal URL for updating scopes.
- Remind them to reinstall the app after updating scopes.
