# ForgeFlows

A ForgeKit product by Orynix Technologies. Ship today. Cash tomorrow.

Four n8n workflow files that automate the busywork around a small digital-product business: logging sales, summarizing transcripts, capturing content ideas, and sending yourself a daily task digest. Import the JSON, fill in your own credentials, activate.

This is a template pack, not a hosted app. You need your own n8n instance (self-hosted or n8n Cloud) to run the workflows. Zapier versions are included too, in case you don't run n8n.

## What's included

```
n8n-workflows/
  gumroad-sale-to-log.json        - Gumroad sale -> Google Sheets row -> Slack ping
  transcript-to-summary.json      - dropped transcript file -> summary markdown file
  bookmark-to-content-idea.json   - RSS bookmark -> content idea row
  daily-task-digest.json          - scheduled trigger -> daily task digest to Slack + email
zapier-recipes/                   - matching step-by-step Zapier builds for all 4 flows
dummy-payloads/                   - sample JSON payloads to test each flow without a live source
sample-output/                    - one flow's input/output shown side by side
FLOWS.md                          - exact placeholder values to change, per workflow, per node
LICENSE.txt
```

## 3-step setup

1. **Import the JSON.** Open n8n → Workflows → Import from File → pick a file from `/n8n-workflows/`.
2. **Set credentials.** Each workflow needs 1-3 credentials (Google Sheets, Slack, Notion, SMTP). Create them in n8n's Credentials panel, then select them in the relevant node. See `FLOWS.md` for exactly which node needs which credential.
3. **Activate.** Toggle the workflow to "Active" in the top right. For webhook-based flows, copy the generated webhook URL into the source app's settings (e.g. Gumroad's Ping URL).

Setup time: 10-15 minutes per workflow, most of it spent creating credentials the first time. After that, adding a second or third workflow takes 2-3 minutes each since credentials are reused.

## Example

Gumroad sale comes in as a webhook:

```json
{ "body": { "product_name": "ForgeFlows", "email": "buyer@example.com", "price": "24.00", "sale_id": "gum_9f8e7d6c5b4a" } }
```

Workflow appends a row to your Google Sheet and posts to Slack:

```
New sale: ForgeFlows - $24.00 from buyer@example.com
```

Full walkthrough: `sample-output/gumroad-sale-to-log.sample.md`.

## Honest limits

- **Not live automation out of the box.** Every workflow has placeholder sheet IDs, channel names, folder paths, and API keys. Nothing fires until you replace them — see `FLOWS.md`.
- **`transcript-to-summary.json` needs a script or an AI API.** The "Run Summarize Script" node is a stub that shells out to a script you write. It does not include a summarizer. Swap it for an HTTP Request node to an AI API if you'd rather not write a script.
- **The Execute Command node needs self-hosted n8n.** n8n Cloud disables shell command execution for security. If you're on n8n Cloud, replace that node in `transcript-to-summary.json` with an HTTP Request node.
- **RSS-based bookmark capture depends on your bookmarking tool exposing a feed.** Not all of them do. Check your tool's export settings, or swap the trigger node for a native integration if n8n has one for your tool.

## FAQ

**Do I need to know how to code?**
No. You need to be comfortable clicking through n8n's UI and pasting in credentials. `FLOWS.md` tells you exactly which field to change in every node.

**Does this include n8n itself?**
No. n8n is free and open-source to self-host, or paid on n8n Cloud. ForgeFlows is the workflow files, not the platform.

**Can I use these with Zapier instead of n8n?**
Yes. Every workflow has a matching step-by-step recipe in `/zapier-recipes/`. Zapier doesn't support portable JSON imports for custom recipes, so those are written as numbered setup instructions instead of a file you import.

**Will this work with n8n Cloud?**
Three of the four workflows, yes, unchanged. `transcript-to-summary.json` uses a local-file trigger and a shell command node, both of which require self-hosted n8n. See "Honest limits" above.

**Can I modify the workflows?**
Yes. Rename nodes, add steps, swap Slack for Discord, whatever you need. See `LICENSE.txt` for what you can and can't do with the files themselves.

**What if a workflow doesn't fire?**
Check three things first: the workflow is toggled Active, the credential attached to each node is valid (not expired), and any webhook URL is pasted correctly into the source app. Most failures are one of those three.

## License

See `LICENSE.txt`. Short version: use it on unlimited personal or client projects, modify it freely, keep commercial output with no attribution required. Don't resell or redistribute the files themselves.
