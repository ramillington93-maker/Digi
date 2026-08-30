# FLOWS.md — What to Change Before Each Workflow Runs

Every workflow ships with placeholder values. Nothing runs live until you replace them. Search each JSON file for `REPLACE_WITH` or `REPLACE` if you want to find them fast — every placeholder uses that prefix.

---

## 1. gumroad-sale-to-log.json

| Node | Field | Placeholder | Replace with |
|---|---|---|---|
| Gumroad Sale Webhook | `webhookId` | `REPLACE_WITH_WEBHOOK_ID` | n8n generates this automatically on first save — you don't type it in, but you do need to copy the resulting webhook URL into Gumroad's "Ping URL" setting (Gumroad → Settings → Advanced → Ping). |
| Append Sale Row (Google Sheets) | `sheetId` | `REPLACE_WITH_GOOGLE_SHEET_ID` | The ID from your Google Sheet's URL (the long string between `/d/` and `/edit`). |
| Append Sale Row (Google Sheets) | credential `id` | `REPLACE_WITH_CREDENTIAL_ID` | Create a Google Sheets OAuth2 credential in n8n, then select it in this node — n8n fills the ID for you. |
| Notify Slack Channel | `channel` | `#sales` | Your real Slack channel name. |
| Notify Slack Channel | credential `id` | `REPLACE_WITH_CREDENTIAL_ID` | Create a Slack API credential (bot token) in n8n and select it. |

**Also needed:** a Gumroad account with Ping notifications enabled.

---

## 2. transcript-to-summary.json

| Node | Field | Placeholder | Replace with |
|---|---|---|---|
| Watch Transcript Folder | `path` | `/REPLACE/WITH/WATCHED_FOLDER/inbox` | An absolute folder path on the machine running n8n (must be a folder n8n's process can read — this only works on self-hosted n8n, not n8n Cloud). |
| Run Summarize Script (stub) | `command` | `/REPLACE/WITH/PATH/summarize.py` | Path to your own summarization script. This node is a stub — ForgeFlows does not include `summarize.py`. Point it at a script you write, or swap this node for an HTTP Request node calling an AI API. |
| Write Summary Markdown File | `fileName` | `/REPLACE/WITH/OUTPUT_FOLDER/...` | An absolute output folder path, writable by n8n's process. |

**Honest limit:** the "Execute Command" node runs shell commands on the n8n host. If you're on n8n Cloud, this node is disabled for security reasons — swap it for an HTTP Request node to a summarization API instead.

---

## 3. bookmark-to-content-idea.json

| Node | Field | Placeholder | Replace with |
|---|---|---|---|
| New Bookmark Trigger (RSS stub) | `feedUrl` | `https://REPLACE-WITH-YOUR-BOOKMARK-FEED.example.com/rss` | An actual RSS feed URL. Not every bookmarking tool exposes one — check your tool's export/feed settings, or swap this trigger for a native n8n node if your tool has one (e.g. Raindrop.io, Pocket). |
| Append Content Idea Row | `sheetId` | `REPLACE_WITH_GOOGLE_SHEET_ID` | The ID from your content-ideas Google Sheet's URL. |
| Append Content Idea Row | credential `id` | `REPLACE_WITH_CREDENTIAL_ID` | Same Google Sheets OAuth2 credential as workflow 1 (or a new one). |

---

## 4. daily-task-digest.json

| Node | Field | Placeholder | Replace with |
|---|---|---|---|
| Every Day at 7am | `cronExpression` | `0 7 * * *` | Adjust the hour to your timezone / n8n instance timezone if 7am isn't right. |
| Fetch Tasks (Notion/Airtable stub) | `url` | `.../databases/REPLACE_WITH_DATABASE_ID/query` | Your real Notion database ID (or swap the whole node for an Airtable node if you use Airtable — same shape, different node type). |
| Fetch Tasks (Notion/Airtable stub) | credential `id` | `REPLACE_WITH_CREDENTIAL_ID` | A Notion API integration token, created in n8n's credentials panel. |
| Send Digest to Slack | `channel` | `#daily-digest` | Your real Slack channel name. |
| Send Digest to Slack | credential `id` | `REPLACE_WITH_CREDENTIAL_ID` | Same Slack credential as workflow 1, or a new one. |
| Email Digest (stub) | `fromEmail` | `digest@REPLACE-YOUR-DOMAIN.com` | A sending address your SMTP credential is allowed to use. |
| Email Digest (stub) | `toEmail` | `REPLACE_WITH_YOUR_EMAIL@example.com` | Where you want the digest delivered. |
| Email Digest (stub) | credential `id` | `REPLACE_WITH_CREDENTIAL_ID` | An SMTP credential in n8n (Gmail, SendGrid, your host's SMTP — any of them work). |

**Note:** the Slack and Email steps both fire from the same "Build Digest Text" node — delete whichever one you don't need.

---

## General setup, all 4 workflows

1. Open n8n → Workflows → Import from File → select the `.json` file.
2. Click each node with a placeholder (see tables above) and fill in the real value.
3. Create/select credentials where the table says to (Google Sheets, Slack, Notion, SMTP — whichever the workflow uses).
4. Toggle the workflow **Active** in the top right.
5. Send a test payload (see `/dummy-payloads/`) or trigger the real event once to confirm.
