# ForgeCalendar

A 30-day content calendar you can post from today. 30 dated rows across X,
Instagram, LinkedIn, and TikTok, plus 50 extra hooks across 4 niches, plus a
small tool that rewrites any hook 5 different ways.

No API key required. Open the CSV, copy the first row, post it.

## What's included

- `calendar-30-day.csv` — 30 days of posts: date, platform, hook, CTA, and asset type. Written for an "AI tools" niche as the demo, but the structure works for any niche — swap the hook text and keep the columns.
- `HOOKS.md` — 50 more hooks split across 4 niches (AI tools, freelance, fitness coaching, local services), ~12-13 each.
- `NOTION-IMPORT.md` — exact steps to import the CSV into Notion as a database with a calendar view.
- `app.py` — a small Streamlit tool: paste a hook, get 5 rewrites (question form, number form, contrarian form, "how I" form, curiosity-gap form). Rule-based by default, no key needed. Add an API key and it upgrades to LLM rewrites automatically.
- `LICENSE.txt` — your usage rights.

## 3-step setup

1. **Open `calendar-30-day.csv`** in Google Sheets, Excel, Notion, or Airtable. That's the whole product — it works standalone, right now, with nothing to install.
2. **Swap the niche.** The hooks are written for "AI tools." Replace the subject with yours — freelance, fitness coaching, local services, or your own — using `HOOKS.md` for 50 more examples of the pattern.
3. *(Optional)* **Run the hook remixer.** `pip install -r requirements.txt`, then `streamlit run app.py`. Paste any hook, get 5 rewritten variants. No key needed for this step either.

## Example

Row 1 of the calendar:

| date | platform | hook | cta | asset_type |
|---|---|---|---|---|
| 2026-09-01 | X | I replaced 3 subscriptions with one $20 AI tool. Here's what changed. | Reply with your most annoying subscription | thread |

Paste that hook into the remixer and you get back 5 variants, one per structure — a question version, a number version, a contrarian version, a "how I" version, and a curiosity-gap version. Post whichever one fits your feed that day.

## Using the hook remixer

The remixer works out of the box with rule-based synonym and structure swaps —
no account, no key, no cost. If you set `ANTHROPIC_API_KEY` or
`OPENAI_API_KEY` (copy `.env.example` to `.env` and fill one in), it
upgrades to LLM-written variants. If the key is missing, wrong, or the API
call fails, it falls back to rule-based mode automatically. The tool never
breaks either way.

```
cp .env.example .env   # optional — only if you want the LLM upgrade
pip install -r requirements.txt
streamlit run app.py
```

## FAQ

**Do I need an API key?**
No. The CSV and hooks are the core product and need nothing but a spreadsheet app. The remixer's rule-based mode also needs nothing. The API key is only for the optional LLM upgrade on the remixer.

**Can I use a different niche than AI tools?**
Yes. The calendar structure (date, platform, hook, CTA, asset type) works for any niche. Swap the hook column and keep the rest. `HOOKS.md` has 3 other niches already written out as examples.

**Can I edit the CSV?**
Yes, freely. Add rows, remove platforms, change dates. It's a plain CSV, not a locked template.

**Does the remixer post anything automatically?**
No. It only rewrites text you paste in. You still post it yourself, on your own schedule.

**What if I don't use Notion?**
`NOTION-IMPORT.md` is optional. The CSV opens in any spreadsheet tool — Sheets, Excel, Airtable — the same way.

## License

See `LICENSE.txt`. Short version: use it on unlimited projects, including client work, don't resell the files themselves.

---

A ForgeKit product by Orynix Technologies.
