# ForgeResume — Gumroad listing copy

## Title
ForgeResume — Resume Match Score & Keyword Optimizer (Streamlit app)

## Subtitle
Turn a resume and a job post into a real match score, a missing-keyword list, and stronger bullets — in one command, no account needed.

## Pitch (~120 words)

Job boards don't tell you why you got filtered out. ForgeResume does.
Paste your resume and a job description, and it tokenizes both, strips
filler words, and computes a real keyword-overlap score — not a guess,
actual text processing you can read in the code. You get the exact
keywords the posting uses that your resume doesn't, ranked by how often
they show up. Paste a weak bullet and it rewrites it in STAR format
(Situation, Task, Action, Result), pulling in the keywords you're missing.
Generate a tailored summary for the top of your resume. Runs entirely on
your machine with `streamlit run app.py` — no account, no upload to a
server, no API key required for the core scoring. Add a key later if you
want LLM-polished rewrites instead of the built-in template.

## 5 bullets

- Real keyword-overlap match score — tokenized, stopword-filtered, stemmed. Not a black box.
- Missing-keyword list ranked by frequency, so you know what to add first.
- STAR-format bullet rewriter that works offline with a rule-based template.
- Tailored professional summary generator, built from what actually matches the posting.
- One command to run it: `streamlit run app.py`. No account, no server upload.

## Who it's for

- Job seekers applying to more than a couple of roles who want to know why
  a resume isn't landing interviews.
- Career coaches and resume writers who want a repeatable, explainable
  scoring tool for clients instead of a black-box "ATS score."
- Recruiters or hiring managers who want a fast first-pass overlap check
  between a resume and a job description.

## Who it's not for

- Anyone who wants an "ATS score" that mimics a specific vendor's exact
  proprietary algorithm — this is a transparent keyword-overlap scorer,
  not a reverse-engineered clone of any one ATS.
- Anyone who wants an app that edits a PDF resume file directly — this
  works on plain text you paste or upload as `.txt`.
- Anyone who wants fully automated resume rewriting with zero review —
  the rewrites are a strong starting draft, not a final submit-as-is file.

## What's included

- `app.py` — the full Streamlit app (single file, under 500 lines).
- `requirements.txt` — pinned dependencies.
- `.env.example` — optional API key setup.
- `.streamlit/config.toml` — dark theme, ready to go.
- `/samples` — 2 sample resumes (marketing, software engineering) and 2
  matching job descriptions, so you can see real output before you paste
  your own.
- `README.md` — setup and FAQ.
- `LICENSE.txt` — buyer license.

## FAQ

**Do I need an API key?**
No. The match score and missing-keyword detection run fully offline.
A key only upgrades the bullet rewrite and summary to LLM output.

**What does it run on?**
Python 3.11+ and Streamlit. One command: `streamlit run app.py`.

**Does it work for non-tech resumes?**
Yes — the scoring is keyword-based, not domain-specific. Sample files
include both a marketing resume and a software engineering resume.

**Can I use this for client work?**
Yes, unlimited use on your own or client resumes. See LICENSE.txt for
what you can't do (resell the source files).

**Will it guarantee I pass an ATS?**
No tool can guarantee that. It gives you a transparent, real overlap
score and the specific keywords to add — the same core signal most ATS
keyword filters use, computed in the open instead of hidden behind a
paywall.

## Suggested price

**$25** (reasonable range: $19-$29 — reduce to $19 for an early-bird or
launch-week price, $29 if bundled with a second ForgeKit product).
