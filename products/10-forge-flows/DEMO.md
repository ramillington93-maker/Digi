# DEMO.md — 20-Second Demo Recording Steps

Goal: show a real workflow import, trigger, and output in under 20 seconds. Use the Gumroad workflow — it's the fastest to demo since the payload is short and the output (a sheet row + Slack message) is visual.

## Before you record

1. Open n8n in your browser, log in, land on the Workflows list.
2. Import `n8n-workflows/gumroad-sale-to-log.json` ahead of time (off-camera) and fill in real (or test) Google Sheets and Slack credentials so it actually runs.
3. Open a second browser tab with the Google Sheet, and a third with the Slack channel, so you can flip to them fast.
4. Have `dummy-payloads/gumroad_sale_payload.json` open in a text editor, ready to copy.

## Recording steps (aim for ~4-5 seconds per step)

1. **(0:00-0:04) Show the n8n canvas.** Start on the Workflows list, click into "ForgeFlows - Gumroad Sale to Log." Let the full 4-node canvas (Webhook → Set → Google Sheets → Slack) sit on screen for a beat so viewers can read the node names.

2. **(0:04-0:08) Trigger it.** Click the Webhook node, hit "Listen for Test Event" (or use n8n's "Execute Workflow" test button with the dummy payload pasted in). Paste in the contents of `dummy-payloads/gumroad_sale_payload.json` and send it.

3. **(0:08-0:12) Show it run.** Let the canvas animate — each node lights up green as it executes, left to right. This is the moment that sells "it just works."

4. **(0:12-0:16) Cut to the Google Sheet.** Show the new row appended: date, product name, buyer email, price, order ID.

5. **(0:16-0:20) Cut to Slack.** Show the message land in the channel: "New sale: ForgeFlows - $24.00 from buyer@example.com."

## Notes

- Keep the cursor movement minimal — jump cuts between the three views (canvas, sheet, Slack) read cleaner than dragging windows around.
- If your screen recorder supports it, zoom in on the node names during step 1 so the workflow reads clearly even at small video size.
- Mute notification sounds before recording — Slack pings during your own demo look sloppy.
- Export at 1080p minimum; Gumroad product pages compress video, so starting high keeps it legible.
