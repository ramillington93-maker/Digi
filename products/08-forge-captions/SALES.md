# SALES.md — Gumroad listing copy for ForgeCaptions

## Title
ForgeCaptions — Social Caption Generator (Streamlit App)

## Subtitle
Turn a product description into 10 captions, 10 hooks, 15 hashtags, 3 CTAs, and a first comment. No API key needed.

## Pitch (~120 words)

You know what to sell. Writing the caption is what eats your Tuesday night. ForgeCaptions fixes that part.

Type your product, pick a platform — X, Instagram, LinkedIn, or TikTok — and a tone: bold, friendly, professional, or funny. In seconds you get 10 captions, 10 hooks, 15 hashtags, 3 CTA variants, and a first-comment line built to pull replies. It runs on a template engine built from 20 real caption patterns, not a mystery prompt, so the same input gives you the same result every time you tweak it.

No account. No API key. No subscription. Runs on your own machine with one command: `streamlit run app.py`. Want an AI polish pass on top? Plug in your own Anthropic or OpenAI key — totally optional.

## 5 bullets

- 10 captions, 10 hooks, 15 hashtags, 3 CTAs, and 1 first-comment line per run
- 4 platforms (X, Instagram, LinkedIn, TikTok) × 4 tones (bold, friendly, professional, funny)
- Runs locally with one command, `streamlit run app.py` — no API key, no account, no monthly fee
- Built on 20 real caption/hook patterns you can read and edit in `samples/styles.json`
- Optional AI polish pass if you add your own Anthropic or OpenAI key — skip it and it still works fully

## Who it's for

- Solo founders and small business owners posting their own product across social
- Freelancers and agencies who write captions for multiple clients and want a fast first draft
- Anyone who has the product but freezes on the caption

## Who it's not for

- Anyone who needs a scheduler or auto-posting — this generates text, it doesn't publish it
- Anyone who wants a single "AI does everything" black box with no visibility into how output is built
- Teams that need multi-user accounts or a hosted dashboard — this is a local single-user tool

## What's included

- `app.py` — the Streamlit app (run with `streamlit run app.py`)
- `generator.py` — the template engine, importable and runnable on its own
- `samples/styles.json` — 20 real caption/hook style patterns across 4 platforms and 4 tones
- `sample-output.md` — a full worked example
- `requirements.txt`, `.env.example`, `.streamlit/config.toml`
- `README.md`, `LICENSE.txt`

## FAQ

**Do I need an API key?** No. It's fully template-based out of the box. A key only unlocks an optional AI polish pass.

**What platforms does it cover?** X, Instagram, LinkedIn, TikTok.

**Does it post for me?** No. It generates the text — captions, hooks, hashtags, CTAs, first comment. You post it.

**Can I resell this tool?** No — see `LICENSE.txt`. You can use it and sell whatever you make with it (your captions, your content), you just can't resell the tool's source files.

**How is this different from asking a chatbot?** No prompt-writing, no account, no per-use cost, and it always outputs the same five sections in the same structure — captions, hooks, hashtags, CTAs, first comment — so it drops straight into your posting workflow.

## Suggested price

**$19** (range: $15–$25). Anchor near $19 — high enough to signal it's a real tool with 20 curated style patterns and a working app, low enough to be an impulse buy for anyone posting weekly.
