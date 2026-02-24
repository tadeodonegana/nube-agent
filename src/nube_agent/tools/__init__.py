from nube_agent.tools.abandoned_checkouts import (
    get_abandoned_checkout,
    list_abandoned_checkouts,
)
from nube_agent.tools.categories import (
    create_category,
    delete_category,
    get_category,
    list_categories,
    update_category,
)
from nube_agent.tools.coupons import (
    create_coupon,
    delete_coupon,
    get_coupon,
    list_coupons,
    update_coupon,
)
from nube_agent.tools.customers import (
    create_customer,
    get_customer,
    list_customers,
    update_customer,
)
from nube_agent.tools.images import (
    add_image,
    delete_image,
    list_images,
    update_image,
)
from nube_agent.tools.orders import (
    cancel_order,
    close_order,
    get_order,
    list_orders,
    open_order,
    update_order,
)
from nube_agent.tools.pages import (
    create_page,
    delete_page,
    get_page,
    list_pages,
    update_page,
)
from nube_agent.tools.products import (
    create_product,
    delete_product,
    get_product,
    list_products,
    update_product,
)
from nube_agent.tools.store import get_store_info
from nube_agent.tools.variants import (
    bulk_update_stock_price,
    create_variant,
    delete_variant,
    get_variant,
    list_variants,
    update_variant,
)

ALL_TOOLS = [
    # Store
    get_store_info,
    # Products
    list_products,
    get_product,
    create_product,
    update_product,
    delete_product,
    # Categories
    list_categories,
    get_category,
    create_category,
    update_category,
    delete_category,
    # Variants
    list_variants,
    get_variant,
    create_variant,
    update_variant,
    delete_variant,
    bulk_update_stock_price,
    # Images
    list_images,
    add_image,
    update_image,
    delete_image,
    # Orders
    list_orders,
    get_order,
    update_order,
    close_order,
    open_order,
    cancel_order,
    # Customers
    list_customers,
    get_customer,
    create_customer,
    update_customer,
    # Coupons
    list_coupons,
    get_coupon,
    create_coupon,
    update_coupon,
    delete_coupon,
    # Abandoned Checkouts
    list_abandoned_checkouts,
    get_abandoned_checkout,
    # Pages
    list_pages,
    get_page,
    create_page,
    update_page,
    delete_page,
]
