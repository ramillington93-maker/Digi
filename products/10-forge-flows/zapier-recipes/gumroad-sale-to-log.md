# Zapier Recipe: Gumroad Sale to Log

Same automation as `n8n-workflows/gumroad-sale-to-log.json`, built in Zapier instead. No JSON export needed — Zapier recipes aren't portable, so follow these steps inside your own Zapier account.

## What it does
When someone buys on Gumroad, log the sale in a Google Sheet and post it to Slack.

## Setup (4 steps)

1. **Trigger: Gumroad — New Sale**
   - App: Gumroad
   - Event: New Sale
   - Connect your Gumroad account (Settings → Advanced → find your Zapier/webhook key on Gumroad's side, or use Gumroad's native Zapier trigger if available in your account).

2. **Action: Formatter by Zapier — Text**
   - Transform: combine fields into a single row-ready format.
   - Map: `Sale Date` (use Zapier's built-in timestamp), `Product Name`, `Buyer Email`, `Price`, `Order ID` from the trigger step.

3. **Action: Google Sheets — Create Spreadsheet Row**
   - Spreadsheet: pick your sales tracking sheet.
   - Worksheet: `Sales`.
   - Map columns A–E to: Sale Date, Product Name, Buyer Email, Price, Order ID.

4. **Action: Slack — Send Channel Message**
   - Channel: `#sales` (or your channel).
   - Message text: `New sale: {{Product Name}} - ${{Price}} from {{Buyer Email}}`

## Placeholders to change
- Google Sheet ID / spreadsheet selection in step 3.
- Slack channel name in step 4.
- Gumroad account connection in step 1.

## Test it
Use Zapier's "Test trigger" with a sample sale, or use the dummy payload at `../dummy-payloads/gumroad_sale_payload.json` as a reference for field names when mapping.
