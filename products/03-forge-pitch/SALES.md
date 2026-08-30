# Gumroad listing copy — ForgePitch

## Title
ForgePitch — Job Post to Proposal in 30 Seconds

## Subtitle
Paste a job post, get a proposal, 3 subject lines, 3 price anchors, and
a P.S. that kills the price objection. No API key needed.

## Pitch (~120 words)

You've read the job post twice and you're still staring at a blank
proposal box. ForgePitch fixes that part. Paste the job post and a
5-line version of your profile — name, skills, experience, rate,
portfolio link — and it hands back a full proposal: an opening line
that quotes the actual post, a relevant-experience paragraph, a 3-step
approach matched to the job's niche, 3 subject lines, 3 price anchors
scaled to the client's budget, and a P.S. that handles the price or
timeline objection before the client asks it. Runs on your machine.
Template mode needs no API key — set one only if you want an optional
AI polish pass. CLI and a Streamlit UI included, same output either
way.

## 5 bullets

- Paste a job post, get a full proposal in seconds — not a fill-in-the-blank template.
- 3 subject lines and 3 price anchors (low / mid / premium) generated per job, not fixed.
- Reads the job post for skills, budget hints, and tone, and writes accordingly.
- Works with zero setup and no API key. Optional AI polish if you add one.
- Both a CLI (`python cli.py`) and a Streamlit app (`streamlit run app.py`) — same logic, your choice of interface.

## Who it's for

- Freelancers applying to 5+ jobs a week on Upwork, Contra, or similar, who are tired of writing the same proposal from scratch.
- Agencies or solo consultants who want a consistent proposal structure without hiring a copywriter.
- Anyone comfortable running one Python command or one Streamlit command locally.

## Who it's not for

- Anyone who wants a browser extension that auto-fills Upwork's form — this is a paste-in, copy-out tool.
- Anyone who wants proposals written with zero editing — read every output before you send it. It's a strong first draft, not a final one.
- Anyone with no comfort running `pip install` and a terminal command (or Streamlit) at least once.

## What's included

- `cli.py` — command-line proposal generator.
- `app.py` — Streamlit UI, same logic, ForgeKit dark theme pre-configured.
- `core.py` — the template/heuristic engine (readable, editable Python — not a locked black box).
- `/samples/` — 3 realistic job posts (web dev, content writing, data/admin) plus a sample profile.
- `requirements.txt`, `.env.example`, `README.md`, this file, and your license.

## FAQ

**Do I need an OpenAI or Anthropic account?**
No. The core product is a template engine that reads your job post and
profile and needs no external API. An API key is optional and only
adds a prose-polish pass.

**What does "template mode" actually mean?**
It means the proposal text is built from real extracted signals — the
skills the job post mentions, the budget it states, its tone — not one
static block of text with your name swapped in. Every job post produces
a different result.

**Does this post the proposal for me?**
No. You paste the job post in, you copy the proposal out, you paste it
into Upwork (or wherever). No account access, no automation, no risk of
a platform flagging bot activity.

**Can I use it for niches other than the 3 sample job posts?**
Yes — the keyword detection covers web dev, content writing, data/admin
support, design, and marketing, and anything else still gets a full
proposal with a generic (but still customized) approach section.

**Refunds?**
Handled through your Gumroad purchase page per Gumroad's standard
policy.

## Suggested price

**$25** (reasonable range: $19–$29)
