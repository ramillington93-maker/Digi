# DEMO.md — Recording a 20-second demo for ForgeHabits

Goal: show the XP system reacting to a real check-off, in Notion and in
the tracker, in under 20 seconds. Don't narrate the whole product — show
one action and its result.

## Setup (before you hit record)

1. Have the Notion ForgeHabits dashboard open in one browser tab, built
   per NOTION-SETUP.md, with sample data loaded.
2. Have the Streamlit tracker running in a terminal (`streamlit run
   app.py`) and open in a second browser tab, at `localhost:8501`.
3. Reset `habits_state.json` (delete it, or use the state that ships
   with the tracker) so the streak numbers are believable and not
   maxed out.
4. Zoom your browser to 125–150% so text is readable in a small
   recording window.

## Recording steps (aim for ~20 seconds total)

1. **(0:00–0:03)** Start on the Notion dashboard. Show the callout at
   the top: current Level and XP total.
2. **(0:03–0:07)** Scroll to the Today view. Point at an unchecked
   habit row (e.g. "Cold Shower").
3. **(0:07–0:10)** Cut to the Streamlit tracker tab. It's already open,
   showing the same habit unchecked with its current streak.
4. **(0:10–0:14)** Click the checkbox for that habit in the tracker.
   Let the page rerun — the Total XP metric and the streak number both
   update live on screen.
5. **(0:14–0:18)** Zoom or highlight the updated Total XP number and the
   new streak count so the change is unmistakable.
6. **(0:18–0:20)** End on the Badges line if a new badge appears (e.g.
   "First Rep"), or hold on the updated XP total as your closing frame.

## Capture notes

- Use a screen recorder that captures cursor clicks (QuickTime, ScreenPal,
  or OBS all work). A visible click on the checkbox sells the "this is
  real, not a mockup" point.
- Don't include the terminal window in the recording — viewers don't
  need to see `streamlit run app.py`, they need to see the result.
- Keep the file under a normal Gumroad thumbnail-video limit (usually
  under 50MB) — a 20-second screen capture at 1080p should stay well
  under that.
- Export as .mp4 or .gif. A silent .gif loop works fine for a Gumroad
  listing if you'd rather skip audio and voiceover entirely.

## Optional voiceover line (if you narrate)

"Check off a habit. XP and streak update instantly — same rules as the
Notion dashboard, tracked locally, no account needed."
