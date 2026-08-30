# SALES.md — Gumroad Listing Copy

## Title
ForgeNotes — Meeting Transcript to Summary, Decisions, and Action Items

## Subtitle
Paste a Zoom transcript. Get a summary, decisions, action items, and a follow-up email — in 10 seconds, no API key.

## Pitch (~120 words)

You just left a 45-minute meeting and nobody wrote anything down. ForgeNotes
fixes that in the time it takes to paste a transcript. Drop in a Zoom `.vtt`
export or plain text, and it pulls out an executive summary, every decision
that got made, and every action item — with owner and due date, when the
transcript mentions one. Then it drafts a follow-up email you can copy
straight into Gmail. No API key needed: it runs on rule-based text
extraction out of the box. Have an Anthropic or OpenAI key? Flip one switch
in the sidebar for sharper phrasing — it falls back automatically if the
call fails. Runs locally with one command. Export to Markdown or a
Word-ready file. Built for people who run meetings, not people who write
meeting-note software.

## 5 Bullets

- Paste or upload a transcript, get a summary, decisions, and action items with owners and dates in seconds
- No API key required — rule-based extraction works out of the box, LLM mode is optional
- One-click follow-up email draft, ready to copy into your inbox
- Export to Markdown and a Word-ready format with real download buttons
- Runs locally with one command: `streamlit run app.py` — your transcripts never leave your machine unless you turn on LLM mode

## Who it's for / not for

**For:**
- Freelancers and consultants who run client calls and need notes out fast
- Small team leads who are tired of being the unofficial notetaker
- Anyone who exports Zoom transcripts and currently does nothing with them

**Not for:**
- Teams that need real-time live transcription during the call (this works on a transcript you already have)
- Anyone expecting perfect, human-grade summarization without an LLM key — rule-based mode is genuinely useful but it's pattern matching, not comprehension
- Teams needing multi-user accounts, shared history, or a hosted dashboard (this is a local single-user tool)

## What's included

- Full Streamlit app source (`app.py` + `forgenotes_core.py`)
- Sample transcript (`sample_transcript.vtt`) to try it immediately
- Dark ForgeKit theme, pre-configured
- README with 3-step setup
- Sample output file so you know what you're buying before you run it
- Buyer license (commercial use of output allowed, no attribution required)

## FAQ

**Do I need to know Python?**
No. Install once with `pip install -r requirements.txt`, then run
`streamlit run app.py`. If you can run one command in a terminal, you can
run this.

**Does it need an API key?**
No. It works fully without one. A key only unlocks an optional, sharper LLM
pass.

**What if the LLM call fails?**
It falls back to the rule-based result automatically. You'll never get an
error screen or a blank output.

**Can I white-label this for clients?**
You can use it on unlimited client projects and use the output commercially.
You can't resell or repackage the tool itself. See LICENSE.txt.

**What transcript formats does it read?**
Zoom `.vtt` exports, `.txt` files with "Name: text" lines, and plain pasted
text with no speaker labels.

## Suggested price

**$19** (one-time). Range: $15–$25 depending on how you bundle it — $15 as a
standalone tool, $25 if bundled with other ForgeKit productivity tools.
