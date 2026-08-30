# ForgeNotes

Turn a meeting transcript into a summary, decisions, action items, and a
follow-up email draft. No account. No API key required.

## What it does

Paste a Zoom transcript (or upload a `.vtt` / `.txt` file) and ForgeNotes
gives you:

- **Executive summary** — 3-5 sentences, pulled from what was actually said
- **Decisions made** — every line that reads like a decision ("we decided," "agreed," "confirmed")
- **Action items** — owner, task, and due date, pulled from phrases like "I'll," "will," "by Friday"
- **Follow-up email draft** — ready to copy into Gmail or Outlook

It runs entirely on rule-based text extraction (regex + sentence scoring).
No LLM, no API key, no internet call required. If you set `ANTHROPIC_API_KEY`
or `OPENAI_API_KEY`, ForgeNotes will try an LLM pass to sharpen the wording —
and if that call fails or the key is missing, it silently falls back to the
rule-based result. It never crashes and never requires a key.

## Setup (3 steps)

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL Streamlit prints (usually `http://localhost:8501`).

That's it. No signup, no config, no database.

**Optional:** copy `.env.example` to `.env` and set `ANTHROPIC_API_KEY` or
`OPENAI_API_KEY` if you want LLM-enhanced output. You'll also need the
matching SDK: `pip install anthropic` or `pip install openai`. This is
optional — the tool works fully without it.

## Example

Click "Load sample transcript" in the app, or run it yourself against the
included `sample_transcript.vtt` (a realistic 5-person onboarding sync with
decisions, owners, and dates). See [sample-output.md](sample-output.md) for
the exact output that transcript produces.

## How the rule-based extraction works

- **Summary:** scores every sentence by word frequency (how much it overlaps
  with the meeting's most common non-filler words), boosts sentences with
  named entities and dates, downweights short reply fragments like "Sure,"
  and "Yes," then picks the top 5 in original order.
- **Decisions:** scans for "decided," "agreed," "final," "confirmed,"
  "resolved," and similar phrases. Skips anything phrased as a question.
- **Action items:** scans for "I'll," "I will," "can you," and similar
  commitment phrases, then pulls a date from the same sentence (weekday
  names, month + day, "today," "tomorrow," "Q1"-"Q4") and an owner (the
  speaker if they said "I'll," or a named participant if one is addressed
  directly).

This is a heuristic, not a language model. It will occasionally pull a
decision that's really a strong opinion, or miss an action item phrased in
an unusual way. Turn on LLM mode with your own key if you want closer-to-perfect
phrasing — the rule-based pass is what ships by default and it's what most
buyers will run.

## Export

Three download buttons, no copy-pasting from the browser:

- **notes.md** — the full summary, decisions, action items, and email draft as Markdown
- **Word-ready .md** — the same content, formatted to paste cleanly into Word or Google Docs
- **email draft .txt** — just the follow-up email, ready to paste into your email client

## FAQ

**Does this need an API key?**
No. It works fully offline with rule-based extraction. An API key is
optional and only improves phrasing.

**What transcript formats work?**
Zoom `.vtt` exports, plain `.txt` transcripts with "Name: text" lines, and
plain pasted text with no speaker labels at all (action item owners will be
less precise without speaker labels).

**Where does my transcript go?**
Nowhere, unless you turn on LLM mode. In rule-based mode everything runs
locally in the Streamlit process. In LLM mode, the transcript is sent to
whichever provider's API key you supplied (Anthropic or OpenAI) — your key,
their API, not ours.

**Can I use this for client meetings?**
Yes. See LICENSE.txt — commercial use of the output is allowed, no
attribution required.

**It didn't catch an action item / decision. Why?**
It's regex-based, not a language model. It looks for specific phrasing
("decided," "I'll," "by [date]"). Unusual phrasing can slip through. Turn on
LLM mode for better recall if you have a key.

## License

See [LICENSE.txt](LICENSE.txt). Short version: use it, modify it, run it on
unlimited projects, sell the output. Don't resell the tool itself.

---

A ForgeKit product by Orynix Technologies.
