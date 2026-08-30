# ForgeKit — Gumroad Listings (paste-ready)

Publisher name to use on every listing: **Orynix Technologies**. Product line: **ForgeKit**. For the full pitch, FAQ, and "who it's for / not for" copy on any single product, open that product's `SALES.md` — this file is the condensed, paste-into-Gumroad version for all 11 listings (10 products + the bundle) in one place.

Suggested Gumroad tags for every listing: `forgekit`, `orynix-technologies`, `notion-template` / `streamlit-app` / `automation` (whichever applies), `indie-hacker`, `digital-product`.

Cover image: use `brand/logo.svg` (export to PNG at 1280×720 for Gumroad's cover slot) on the `#0B0F14` background.

---

## 01 — ForgeNotes — $19

**Title:** ForgeNotes — Meeting Transcript to Summary, Decisions, and Action Items

**Subtitle:** Paste a Zoom transcript. Get a summary, decisions, action items, and a follow-up email — in 10 seconds, no API key.

**Price:** $19 (launch: $14)

**Description (paste directly):**

You just left a 45-minute meeting and nobody wrote anything down. ForgeNotes fixes that in the time it takes to paste a transcript. Drop in a Zoom `.vtt` export or plain text, and it pulls out an executive summary, every decision that got made, and every action item — with owner and due date, when the transcript mentions one. Then it drafts a follow-up email you can copy straight into your inbox.

**What you get:**
- Paste or upload a transcript, get a summary, decisions, and action items with owners and dates in seconds
- No API key required — rule-based extraction works out of the box, LLM mode is optional
- One-click follow-up email draft, ready to copy into your inbox
- Export to Markdown and a Word-ready format with real download buttons
- Runs locally with one command: `streamlit run app.py` — your transcripts never leave your machine unless you turn on LLM mode

**Setup:** `pip install -r requirements.txt` → `streamlit run app.py`. 2 minutes.

---

## 02 — ForgeHustle — $15

**Title:** ForgeHustle — Notion AI Side-Hustle Tracker

**Subtitle:** Track offers, experiments, content, and revenue in one linked Notion system. 15-minute setup.

**Price:** $15 (launch: $10)

**Description:**

You've got three AI side-hustle ideas in your head, a half-finished spreadsheet, and no idea which one actually makes money. ForgeHustle fixes that with five linked Notion databases — Offers, Experiments, Content, Revenue, and Prompts — all connected, all pre-filled with realistic sample data so you see the structure working before you touch it.

**What you get:**
- 5 linked Notion databases pre-filled with 34 rows of realistic sample data
- Exact, click-by-click Notion CSV import and relation-linking instructions
- 15 copy-paste AI prompts across 8 categories (offer testing, pricing, launch, Gumroad, and more)
- 3 wiki pages: weekly loop, Friday review checklist, offer confidence-scoring rubric
- Works on Notion's free plan — no account, no plugin, no API key required

**Setup:** Import 5 CSVs into Notion, link with one relation property. 15-20 minutes, steps in `IMPORT.md`.

---

## 03 — ForgePitch — $25

**Title:** ForgePitch — Job Post to Proposal in 30 Seconds

**Subtitle:** Paste a job post, get a proposal, 3 subject lines, 3 price anchors, and a P.S. that kills the price objection. No API key needed.

**Price:** $25 (launch: $20)

**Description:**

You've read the job post twice and you're still staring at a blank proposal box. ForgePitch fixes that part. Paste the job post and a 5-line version of your profile — name, skills, experience, rate, portfolio link — and it hands back a full proposal, three subject lines, three price anchors, and an objection-handling P.S.

**What you get:**
- Paste a job post, get a full proposal in seconds — not a fill-in-the-blank template
- 3 subject lines and 3 price anchors (low / mid / premium), generated per job
- Reads the job post for skills, budget hints, and tone, and writes accordingly
- Works with zero setup and no API key — optional AI polish if you add one
- CLI (`python cli.py`) and Streamlit app (`streamlit run app.py`) — same logic, your choice

**Setup:** `pip install -r requirements.txt` → `python cli.py` or `streamlit run app.py`. 2 minutes.

---

## 04 — ForgeCalendar — $19

**Title:** ForgeCalendar — 30-Day Content Calendar + Hook Bank

**Subtitle:** 30 dated posts across X, Instagram, LinkedIn, and TikTok. 50 more hooks across 4 niches. A hook remixer tool included.

**Price:** $19 (launch: $14)

**Description:**

You know what to post. You don't have a month of it lined up. ForgeCalendar gives you 30 dated rows — platform, hook, CTA, and asset type — ready to copy into a spreadsheet or Notion today, plus 50 more hooks across 4 niches so you can see the pattern and swap in your own subject.

**What you get:**
- 30-day content calendar CSV — opens in Sheets, Excel, Notion, or Airtable
- 50 more hooks across 4 niches (AI tools, freelance, fitness coaching, local services)
- Hook remixer tool: paste a hook, get 5 rewrites
- Works with zero setup, no API key, no account
- Step-by-step Notion import guide for a calendar-view database

**Setup:** Open the CSV, or `streamlit run app.py` for the remixer. 1 minute.

---

## 05 — ForgeResume — $25

**Title:** ForgeResume — Resume Match Score & Keyword Optimizer

**Subtitle:** Turn a resume and a job post into a real match score, a missing-keyword list, and stronger bullets — in one command, no account needed.

**Price:** $25 (launch: $20)

**Description:**

Job boards don't tell you why you got filtered out. ForgeResume does. Paste your resume and a job description, and it tokenizes both, strips filler words, and computes a real keyword-overlap score — not a guess, actual text processing you can read in the code.

**What you get:**
- Real keyword-overlap match score — tokenized, stopword-filtered, stemmed
- Missing-keyword list ranked by frequency
- STAR-format bullet rewriter, works offline
- Tailored professional summary generator
- One command to run: `streamlit run app.py` — no account, no server upload

**Setup:** `pip install -r requirements.txt` → `streamlit run app.py`. 2 minutes.

---

## 06 — ForgeOutreach — $24

**Title:** ForgeOutreach — Cold Email Sequence Builder

**Subtitle:** Turn an offer, an ICP, and a proof point into a 5-email cold outreach sequence.

**Price:** $24 (launch: $19)

**Description:**

Cold email is a first-draft problem. You know your offer, you know who you're selling to, and you still burn an hour staring at a blank subject line. ForgeOutreach builds a full 5-email sequence — day 0, 2, 4, 7, 12 — with two subject lines and a LinkedIn DM variant per email.

**What you get:**
- 5-email sequence built from your offer, ICP, and one proof point
- Two subject lines (A/B) per email, plus a LinkedIn DM variant for every day
- One-click `.csv` export shaped for Instantly / Lemlist / Smartlead, plus `.txt` export
- No API key required — optional AI polish if you add your own key
- Runs local with one command — your data never leaves your machine
- Generation only — this tool does not send email

**Setup:** `pip install -r requirements.txt` → `streamlit run app.py`. 2 minutes.

---

## 07 — ForgeHabits — $15

**Title:** ForgeHabits — Gamified Habit Tracker for Notion

**Subtitle:** XP, levels, streaks, and 13 named badges. Notion template plus an optional local tracker. No API key, no subscription.

**Price:** $15 (launch: $10)

**Description:**

Most Notion habit trackers give you a checkbox and a streak number. ForgeHabits gives you a real progression system: base XP by difficulty, a streak bonus that caps at +10, and 10 levels from Starting Line to Max Grind.

**What you get:**
- 4 pre-built Notion databases (Habits, Logs, Rewards, Streaks) with sample data and exact setup steps
- Real XP system: base XP by difficulty, capped streak bonus, 10 named levels
- 13 named badges with hard unlock criteria
- Rewards economy: price real-life rewards in XP
- Optional local Streamlit tracker — zero API keys, zero accounts

**Setup:** Import 4 CSVs into Notion, steps in `NOTION-SETUP.md`. 15 minutes.

---

## 08 — ForgeCaptions — $19

**Title:** ForgeCaptions — Social Caption Generator

**Subtitle:** Turn a product description into 10 captions, 10 hooks, 15 hashtags, 3 CTAs, and a first comment. No API key needed.

**Price:** $19 (launch: $14)

**Description:**

You know what to sell. Writing the caption is what eats your Tuesday night. Type your product, pick a platform and a tone, and get 10 captions, 10 hooks, 15 hashtags, 3 CTA variants, and a first-comment line — built from 20 real caption patterns, not a mystery prompt.

**What you get:**
- 10 captions, 10 hooks, 15 hashtags, 3 CTAs, 1 first-comment line per run
- 4 platforms (X, Instagram, LinkedIn, TikTok) × 4 tones
- Runs locally with one command — no API key, no account, no monthly fee
- Built on 20 real, editable caption/hook patterns
- Optional AI polish pass if you add your own key

**Setup:** `pip install -r requirements.txt` → `streamlit run app.py`. 2 minutes.

---

## 09 — ForgeQuiz — $24

**Title:** ForgeQuiz — Lead-Magnet Quiz Funnel (No Backend)

**Subtitle:** Turn 7 questions into an email list. No server, no code, ready in 15 minutes.

**Price:** $24 (launch: $19)

**Description:**

ForgeQuiz is a 7-question quiz that scores each visitor into one of 3 results and hands them a downloadable summary with their email on it. It's pure HTML, CSS, and JavaScript — no backend, no database, no monthly hosting bill.

**What you get:**
- 7 questions, 3 results, fully scored client-side
- Downloadable result file on submit, works offline
- Every piece of copy documented in `QUIZ-COPY.md` — swap the niche without touching code
- Mobile-first, dark ForgeKit theme, works down to 375px
- Opens by double-clicking `index.html` — no npm, no build step

**Setup:** Double-click `index.html`. It's already running.

---

## 10 — ForgeFlows — $24

**Title:** ForgeFlows — n8n Automation Pack

**Subtitle:** 4 n8n automations that log sales, summarize transcripts, and send you a daily task digest.

**Price:** $24 (launch: $19)

**Description:**

You're doing the same three tasks by hand every day: logging sales, writing up meeting notes, checking what's due. ForgeFlows replaces them with four n8n workflows you import once and forget. Zapier recipes included if you don't run n8n.

**What you get:**
- 4 ready-to-import n8n workflow files
- Matching Zapier recipes for all 4 flows
- Dummy test payloads for every trigger
- `FLOWS.md` tells you exactly which field to change before you run anything
- No code required — import, add credentials, activate

**Setup:** Import JSON into n8n, add credentials, activate. 10-15 minutes per workflow.

---

## THE BUNDLE — ForgeKit Mega Bundle — $49

**Title:** ForgeKit Mega Bundle — All 10 Tools

**Subtitle:** Everything ForgeKit ships, in one download. $209 of tools for $49.

**Price:** $49 (launch: $39)

**Description:**

Ten small tools. One job each. Ship today, not next quarter.

ForgeKit is a line of digital products built to get a solo seller from zero to a live Gumroad listing in a day: meeting notes, a Notion side-hustle tracker, a freelance proposal generator, a content calendar, a resume optimizer, a cold email builder, a habit tracker, a caption generator, a lead-magnet quiz, and an automation pack. Every tool runs locally, needs no paid API, and ships with a real sample so you see the output before you touch the code.

Bought separately, these ten products add up to $209. The bundle is $49 — less than the price of any three of them alone.

**What's included:**
- All 10 ForgeKit products, full source and templates, no expiry
- 01 ForgeNotes, 02 ForgeHustle, 03 ForgePitch, 04 ForgeCalendar, 05 ForgeResume, 06 ForgeOutreach, 07 ForgeHabits, 08 ForgeCaptions, 09 ForgeQuiz, 10 ForgeFlows
- One license covering the whole set — see `packaging/bundle-readme.md` inside the download
- Future ForgeKit products ship to bundle owners at a discount (list this as a Gumroad "updates" perk if using Gumroad's versioning)

**Who it's for:** Anyone building a portfolio of small income tools, agencies who want the whole kit for client work, and buyers who'd rather pay once than pick one.

**Who it's not for:** Anyone who only needs one specific tool — buy that one standalone, it's cheaper up front.

**Setup:** Unzip `forgekit-complete.zip`. Each product folder is self-contained with its own README. Start with whichever one solves today's problem.
