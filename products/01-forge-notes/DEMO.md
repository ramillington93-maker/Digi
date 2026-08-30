# DEMO.md — 20-Second Demo Recording Steps

Goal: show a blank app turn into a full set of notes in under 20 seconds, with
zero setup friction visible on screen.

## Before you hit record

1. Run `streamlit run app.py` and confirm it's open in your browser at
   `http://localhost:8501`.
2. Refresh the page once so it opens on the clean, empty state (no leftover
   results in view).
3. Resize the browser window to roughly 1280x800 so both columns of output
   are visible without scrolling.
4. Make sure "Upload file" tab is selected by default (it is, on load).

## Recording steps (numbered, in order)

1. **(0:00-0:02)** Start recording on the empty ForgeNotes screen — title,
   caption, and the empty upload box visible. Let it sit for one beat so
   viewers register the app name.
2. **(0:02-0:04)** Click **"Load sample transcript"** under the upload box.
   The paste tab will silently fill with the sample transcript text.
3. **(0:04-0:06)** Click the **"Paste text"** tab to show the transcript
   text is now loaded (this proves it's a real transcript, not a canned
   screenshot).
4. **(0:06-0:07)** Click **"Generate notes"** (the accent-yellow button).
5. **(0:07-0:09)** Let the spinner ("Reading transcript...") show briefly —
   this sells that real processing is happening.
6. **(0:09-0:15)** Once results appear, slowly scroll down past: the
   "Rule-based (no API key used)" badge, the Participants line, the
   Executive Summary column, and the Decisions Made column.
7. **(0:15-0:17)** Continue scrolling to the Action Items column — pause
   half a second on an item with a name and a date visible (e.g. "Sarah
   Kim — ... Due: September 3rd") so the owner/date extraction is legible.
8. **(0:17-0:19)** Scroll to the Export row and click **"Download notes.md"**
   — show the browser's download confirmation (file appears in the
   downloads bar/tray).
9. **(0:19-0:20)** End on the downloaded file name visible on screen (proves
   a real file was produced, not just an on-screen preview).

## Notes for a clean recording

- Don't show the sidebar API key detection step — keep the demo focused on
  the no-key happy path, since that's what every buyer will experience
  first.
- If your capture tool supports cursor highlighting, turn it on — the demo
  is short enough that viewers need to track exactly what's being clicked.
- Record at 1x speed. Don't spend more than 2 seconds on any single static
  screen — keep motion (scrolling, clicking) visible throughout.
- Optional 21st second: flash the "A ForgeKit product by Orynix
  Technologies" footer for brand recall, then cut.
