# Sample: Gumroad Sale to Log

What goes in, and what comes out, for the `gumroad-sale-to-log.json` workflow.

## Input (Gumroad webhook payload)

```json
{
  "body": {
    "sale_id": "gum_9f8e7d6c5b4a",
    "product_name": "ForgeFlows",
    "email": "buyer@example.com",
    "price": "24.00",
    "sale_timestamp": "2026-08-30T14:22:10Z"
  }
}
```

## Output

**Row appended to Google Sheet (`Sales` tab):**

| sale_date | product_name | buyer_email | sale_price | order_id |
|---|---|---|---|---|
| 2026-08-30T14:22:15.000Z | ForgeFlows | buyer@example.com | 24.00 | gum_9f8e7d6c5b4a |

**Slack message posted to `#sales`:**

```
New sale: ForgeFlows - $24.00 from buyer@example.com
```

Full dummy payload for testing: `../dummy-payloads/gumroad_sale_payload.json`
