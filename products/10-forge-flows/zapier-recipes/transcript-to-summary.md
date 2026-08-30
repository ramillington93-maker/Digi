# Zapier Recipe: Transcript to Summary

Same automation as `n8n-workflows/transcript-to-summary.json`, built in Zapier instead.

## What it does
When a transcript file lands in a watched folder, produce a summary markdown file.

## Setup (4 steps)

1. **Trigger: Google Drive (or Dropbox) — New File in Folder**
   - App: Google Drive or Dropbox (pick whichever holds your transcript inbox — Zapier has no generic "local folder" trigger, so use a synced cloud folder).
   - Folder: your transcript inbox folder.

2. **Action: Webhooks by Zapier — POST**
   - URL: your summarization endpoint (a hosted script or API that accepts a file/text and returns a summary — Zapier can't run a local script, so this replaces the n8n "Execute Command" stub node).
   - Payload: file content or file URL from step 1.
   - Note: if you don't have a summarization API, use Zapier's OpenAI (or similar) integration here instead — pass the transcript text in and ask for a 5-bullet summary.

3. **Action: Formatter by Zapier — Text**
   - Combine the summary response into markdown: `# Summary\n\n{{summary_text}}\n\n_Generated {{zap_meta_human_now}} from {{file_name}}_`

4. **Action: Google Drive — Create File from Text**
   - Folder: your output folder.
   - File name: `summary-{{timestamp}}.md`
   - File content: the formatted markdown from step 3.

## Placeholders to change
- Watched folder ID in step 1.
- Summarization endpoint URL in step 2 (or your AI integration credentials).
- Output folder ID in step 4.

## Test it
Drop a `.txt` file into your watched folder, or reference `../dummy-payloads/transcript_dropped_payload.json` for expected field shape when wiring the Formatter step.
