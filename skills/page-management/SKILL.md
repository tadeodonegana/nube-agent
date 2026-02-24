---
name: page-management
description: >
  How to manage content pages in a Tiendanube store: create, update,
  delete, and list pages. Pages are static content like "About Us",
  "FAQ", "Terms and Conditions", etc.
---

# Page Management

## Page Structure

A page in Tiendanube has:
- **name**: Localized title (language-keyed object, e.g., `{"es": "Sobre Nosotros"}`).
- **content**: Localized HTML content.
- **handle**: URL slug (e.g., `{"es": "sobre-nosotros"}`).
- **published**: Whether the page is visible on the store.
- **seo_title** / **seo_description**: SEO metadata.

## Key Rules

1. **Content supports HTML** — you can include formatted text, links, images, etc.
2. **All text fields are multilingual** — the store's language is detected automatically.
3. **Handle is the URL slug** — auto-generated from title if not specified.

## Common Pages

- About Us / Sobre Nosotros
- FAQ / Preguntas Frecuentes
- Terms and Conditions / Términos y Condiciones
- Privacy Policy / Política de Privacidad
- Shipping Policy / Política de Envíos
- Returns Policy / Política de Devoluciones
- Contact / Contacto

## Common Operations

- **List all pages**: `list_pages()`
- **View a page**: `get_page(id)` — returns full HTML content.
- **Create a page**: `create_page(title, content, ...)` — supports SEO fields.
- **Update content**: `update_page(id, '{"title": "...", "content": "<p>...</p>"}')`
- **Delete page**: `delete_page(id)`
