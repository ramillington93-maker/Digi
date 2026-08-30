# ForgeKit Mega Bundle

A ForgeKit product line by **Orynix Technologies**. Ship today. Cash tomorrow.

Thanks for buying the bundle. Here's every tool, what it solves, and where to start.

## What's in this folder

```
ForgeKit-Mega-Bundle/
├── products/
│   ├── 01-forge-notes/       Meeting transcript -> summary, decisions, action items
│   ├── 02-forge-hustle/      Notion side-hustle tracker (template pack)
│   ├── 03-forge-pitch/       Job post -> freelance proposal
│   ├── 04-forge-calendar/    30-day content calendar + hook bank
│   ├── 05-forge-resume/      Resume match score + keyword optimizer
│   ├── 06-forge-outreach/    Cold email sequence builder
│   ├── 07-forge-habits/      Gamified Notion habit tracker
│   ├── 08-forge-captions/    Social caption generator
│   ├── 09-forge-quiz/        Static lead-magnet quiz funnel
│   └── 10-forge-flows/       n8n automation pack
├── brand/                    Colors, voice, logo — if you want to reskin anything
└── packaging/                This file, plus pricing and listing copy for reference
```

Every product folder is self-contained: its own `README.md`, `SALES.md`, `LICENSE.txt`, sample output, and (for code products) `requirements.txt` + `.env.example`. You don't need to touch anything outside a product's own folder to run it.

## Where to start

- Need to write up a meeting right now? → `products/01-forge-notes`
- Setting up a side-hustle tracking system? → `products/02-forge-hustle`
- Applying to a job today? → `products/03-forge-pitch` or `products/05-forge-resume`
- Need a month of content posted? → `products/04-forge-calendar` and `products/08-forge-captions`
- Doing outbound sales? → `products/06-forge-outreach`
- Building a lead list? → `products/09-forge-quiz`
- Automating the busywork? → `products/10-forge-flows`
- Want to actually stick to a habit? → `products/07-forge-habits`

## Running the code products

Every Python tool follows the same pattern:

```
cd products/<product-folder>
pip install -r requirements.txt
streamlit run app.py      # or: python cli.py, if the product has a CLI
```

None of them need an API key to work. If a tool supports an optional LLM upgrade, it reads `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` from your environment — copy `.env.example` to `.env` and drop your key in if you want it. Skip it and the tool still runs.

## License

One buyer license covers all 10 products. Full terms are in each product's `LICENSE.txt` (identical terms, just the product name changes). Short version: use it, modify it, sell what you make with it — don't resell the product files themselves.

## Support

Refunds and support run through your Gumroad purchase page. There's no separate support portal.
