# ForgeHustle

Turn a folder of CSVs into a linked Notion system for tracking an AI side hustle: offers, experiments, content, revenue, and reusable prompts, all connected.

This is a template pack, not a live integration. There's no software to run — you import 5 CSVs into Notion and link them by hand (10 minutes, exact steps in `IMPORT.md`).

## What's in the box

```
02-forge-hustle/
├── README.md                     (this file)
├── IMPORT.md                     exact Notion setup steps
├── PROMPTS.md                    all 15 prompts, readable outside Notion
├── PREVIEW.md                    mockup of the finished setup
├── LICENSE.txt
├── databases/
│   ├── Offers.csv                8 sample offers
│   ├── Experiments.csv           6 sample experiments
│   ├── Content.csv               7 sample content rows
│   ├── Revenue.csv               8 sample revenue rows
│   └── Prompts.csv               15 prompts, 8 categories
└── wiki/
    ├── How to use this system.md
    ├── Weekly review template.md
    └── Offer scoring rubric.md
```

## 3-step setup

1. **Import.** Open Notion, create a page, and import each CSV in `/databases` as its own database. Full click-by-click instructions are in `IMPORT.md`.
2. **Link.** Add an `Offer` relation property to Experiments, Content, and Revenue, pointing back to the Offers database. This is the one manual step — Notion's CSV importer can't guess relations for you.
3. **Run the loop.** Read `wiki/How to use this system.md` for the weekly rhythm: pick one offer Monday, log experiments and revenue through the week, review Friday.

## Example

The Offers database ships with 8 realistic rows already filled in — real offer names, real price points ($9 to $399), real Confidence scores — so you see the structure working before you add your own row. Delete the samples once you've got the shape, or leave them as reference.

Sample row:

| Offer Name | Status | Price | Confidence | Next Action |
|---|---|---|---|---|
| AI Resume Rewrite | Validated | $49 | 5 | Raise price to $59 |

## FAQ

**Does this connect to Notion automatically?**
No. You import CSVs and click through a short setup. No API, no plugin, no account needed beyond a free Notion workspace.

**Do I need the paid Notion plan?**
No — the free plan supports unlimited databases and CSV import.

**Can I use this for a hustle that isn't AI-related?**
Yes. The column names and sample data lean AI-side-hustle, but the structure (Offers → Experiments/Content/Revenue) works for any small offer-based business. Rename the columns as needed.

**Can I edit the sample data?**
Yes — it's yours once you buy it. Overwrite the sample rows with your own offers whenever you're ready.

**What if I don't use Notion?**
The CSVs open in Excel, Google Sheets, or Airtable too. `IMPORT.md` is Notion-specific, but the CSVs themselves aren't locked to any tool.

**Is there support if I get stuck on setup?**
Yes — reach out through your Gumroad purchase page.

## License

See `LICENSE.txt`. Short version: use it for yourself and your clients, don't resell the files themselves.

---

*A ForgeKit product by Orynix Technologies.*
