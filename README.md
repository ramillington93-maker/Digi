# ForgeKit

A line of 10 small digital products, built and published by **Orynix Technologies**. Ship today. Cash tomorrow.

Ten small tools, each doing one job, packaged and ready to list on Gumroad (or any storefront). This repo is the source of truth — everything a buyer receives comes straight out of `products/`.

## What's here

```
/brand         Logo, color tokens, voice guide, shared license and Streamlit theme
/products      The 10 ForgeKit products — each one self-contained and sellable on its own
/packaging     Gumroad listing copy, bundle README, pricing strategy, launch posts
/scripts       zip-all.sh — packages every product (and a mega bundle) for upload
```

## The 10 products

| # | Product | What it does | Price |
|---|---------|---------------|------:|
| 01 | [ForgeNotes](products/01-forge-notes) | Transcript → summary, decisions, action items, follow-up email | $19 |
| 02 | [ForgeHustle](products/02-forge-hustle) | Notion side-hustle tracker (template pack) | $15 |
| 03 | [ForgePitch](products/03-forge-pitch) | Job post → freelance proposal | $25 |
| 04 | [ForgeCalendar](products/04-forge-calendar) | 30-day content calendar + 50-hook bank | $19 |
| 05 | [ForgeResume](products/05-forge-resume) | Resume ↔ job description match score + rewrites | $25 |
| 06 | [ForgeOutreach](products/06-forge-outreach) | Cold email sequence builder | $24 |
| 07 | [ForgeHabits](products/07-forge-habits) | Gamified Notion habit tracker | $15 |
| 08 | [ForgeCaptions](products/08-forge-captions) | Social caption generator | $19 |
| 09 | [ForgeQuiz](products/09-forge-quiz) | Static lead-magnet quiz funnel | $24 |
| 10 | [ForgeFlows](products/10-forge-flows) | n8n + Zapier automation pack | $24 |

Sold separately that's $209. Bundle price: **$49** (see `packaging/pricing.md` for the full pricing strategy and launch discounts).

## How to get from this repo to a live Gumroad listing

1. **Package everything into zips:**
   ```
   ./scripts/zip-all.sh
   ```
   This writes one zip per product plus `forgekit-mega-bundle.zip` into `dist/` (gitignored — regenerate any time, nothing to commit).

2. **Create each Gumroad listing.** Open `packaging/gumroad-listings.md` — every product's title, subtitle, price, and description is paste-ready. Upload the matching zip from `dist/` as the product file.

3. **Create the bundle listing** the same way, using the "THE BUNDLE" section of `gumroad-listings.md` and `dist/forgekit-mega-bundle.zip`.

4. **Launch.** `packaging/launch-posts.md` has 8 X posts, 2 Reddit posts, and a Product Hunt blurb, ready to fill in your links and post.

No other setup required — every code product runs with no paid API key, and every template pack works with just Notion's free plan.

## Quality bar every product meets

- Runs locally with one documented command (see each product's `README.md`).
- No API key required for the core feature. Where an LLM upgrade is offered, it reads `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` and degrades gracefully if absent.
- Ships with a real sample output so a buyer sees the value before running anything.
- MIT-like buyer license (`LICENSE.txt` in every product folder) — use freely, don't resell the files themselves.

## Brand

See `/brand` for the full guide. Short version: dark background (`#0B0F14`), amber accent (`#F5B942`), green success (`#3DDC97`), Inter + JetBrains Mono, and a voice that's short, concrete, and money-aware — no "empower your journey" language anywhere in this repo.
