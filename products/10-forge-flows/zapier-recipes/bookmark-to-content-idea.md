# Zapier Recipe: Bookmark to Content Idea

Same automation as `n8n-workflows/bookmark-to-content-idea.json`, built in Zapier instead.

## What it does
When you bookmark or star something (RSS feed, X/Twitter like, read-later app), append it as a content idea row in a sheet.

## Setup (3 steps)

1. **Trigger: RSS by Zapier — New Item in Feed**
   - Feed URL: your bookmark source's RSS feed (many read-later apps and some X list tools expose one; if yours doesn't, use that app's native Zapier trigger instead).

2. **Filter by Zapier — Only continue if...**
   - Condition: `Title` — Exists.
   - This replaces the n8n "IF" node that drops empty entries.

3. **Action: Google Sheets — Create Spreadsheet Row**
   - Spreadsheet: your content ideas tracker.
   - Worksheet: `ContentIdeas`.
   - Map columns A–D to: Idea Title (`Title`), Source URL (`Link`), Captured At (Zapier timestamp), Status (set to `new`).

## Placeholders to change
- RSS feed URL in step 1 (or swap for your bookmark app's native trigger).
- Google Sheet ID / spreadsheet selection in step 3.

## Test it
Reference `../dummy-payloads/bookmark_payload.json` for the field names (`title`, `link`) when mapping the Filter and Sheets steps.
