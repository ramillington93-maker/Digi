# Zapier Recipe: Daily Task Digest

Same automation as `n8n-workflows/daily-task-digest.json`, built in Zapier instead.

## What it does
Every morning, pull your open tasks and send yourself a digest by Slack and email.

## Setup (4 steps)

1. **Trigger: Schedule by Zapier — Every Day**
   - Time: 7:00 AM (your timezone).

2. **Action: Notion (or Airtable) — Find Database Items**
   - Database/Base: your tasks database.
   - Filter: `Status` is not `Done` (adjust to your schema).

3. **Action: Formatter by Zapier — Text (Line Itemizer)**
   - Combine the returned task titles into a bulleted list: `Daily Task Digest - {{date}}\n\n- {{task_1}}\n- {{task_2}}\n...`

4a. **Action: Slack — Send Channel Message**
   - Channel: `#daily-digest`
   - Message: the formatted digest text from step 3.

4b. **Action: Email by Zapier — Send Outbound Email**
   - To: your email address.
   - Subject: `Daily Task Digest - {{date}}`
   - Body: the formatted digest text from step 3.

## Placeholders to change
- Notion database ID (or Airtable base/table) in step 2.
- Slack channel name in step 4a.
- Recipient email address in step 4b.

## Test it
Reference `../dummy-payloads/task_digest_source_payload.json` for the expected task record shape when mapping the Formatter step.
