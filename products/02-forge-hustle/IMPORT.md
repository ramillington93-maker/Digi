# IMPORT.md — Notion setup, step by step

This is a template pack, not a Notion integration. Nothing runs automatically. You import 5 CSVs and do about 10 minutes of property cleanup. Follow this in order — the relation step near the end depends on the databases existing first.

Setup time: 15-20 minutes.

## Step 1: Create the parent page

1. In Notion, click **+ New page** in the sidebar.
2. Name it "ForgeHustle Tracker" (or whatever you want — this is just a home for the five databases).
3. Leave it empty for now.

## Step 2: Import each CSV as its own database

Notion imports each CSV as a new database, one at a time. Repeat this for all 5 files: `Offers.csv`, `Experiments.csv`, `Content.csv`, `Revenue.csv`, `Prompts.csv`.

1. Inside the "ForgeHustle Tracker" page, type `/csv` and select **Import CSV** from the menu — or use the sidebar: click the **⋯** next to your workspace name, choose **Import**, then **CSV**.
2. Select the CSV file from the `/databases` folder in this pack.
3. Notion creates a new full-page or inline database named after the file (e.g., "Offers"). Rename it if you want to drop the ".csv" from the title.
4. Repeat for all 5 files.

**Do Offers.csv first.** You'll need it to exist before you set up relations in Step 4.

## Step 3: Fix property types

Notion's CSV import guesses property types from the data, and it doesn't always guess right. Check each database and fix these:

**Offers**
- `Price (USD)` → should be **Number**, format as Dollar (click the property header → Edit property → Number → Format → Dollar)
- `Build Time (hrs)` → **Number**
- `Confidence (1-5)` → **Number**
- `Status` → **Select**. Add color-coded options: Idea (gray), Testing (yellow), Validated (green), Killed (red).

**Experiments**
- `Start Date`, `End Date` → **Date** (Notion usually catches these; verify)
- `Result` → **Select** with options: Win, Loss, Partial, Testing

**Content**
- `Date` → **Date**
- `Views`, `Clicks / Replies` → **Number**
- `Status` → **Select**: Posted, Live, Scheduled, Draft

**Revenue**
- `Date` → **Date**
- `Amount (USD)` → **Number**, format as Dollar
- `Type` → **Select**: One-time, Recurring (monthly)

**Prompts**
- `Category` → **Select**, one color per category, so the Prompts board reads at a glance

## Step 4: Link the databases with Relations

CSV import does not create relations — Notion has no way to know "Related Offer" in a text column should point to a row in another database. You have to add that by hand, once. It's mechanical, not hard.

For each of **Experiments**, **Content**, **Revenue**, and **Prompts**:

1. Click **+** at the right edge of the database's property headers to add a new property.
2. Name it `Offer`, set the type to **Relation**, and pick **Offers** as the database to relate to.
3. For every row, click into the new `Offer` cell, type the offer name from the existing text column (e.g., "AI Resume Rewrite"), and select the matching page when it appears in the dropdown.
4. Once every row is linked, you can delete the old plain-text "Related Offer" / "Offer" text column, or keep it as a backup — your call.

This step takes the longest (5-10 minutes across all 4 databases with the sample data). It's the one part of setup that's genuinely manual — there's no way around it in Notion's current CSV importer.

## Step 5: Set up views

These are optional but make the system usable at a glance.

**Offers**
1. Add a **Board** view, group by `Status`. This is your main offer pipeline.
2. Add a second **Board** view, group by `Confidence (1-5)`, sorted descending — your best bets rise to the top.

**Experiments**
1. Add a **Board** view, group by `Result`.

**Content**
1. Add a **Calendar** view using the `Date` property — shows your publishing cadence at a glance.

**Revenue**
1. Add a **Table** view sorted by `Date` descending.
2. Turn on the column sum: hover the bottom of the `Amount (USD)` column, click **Count**, change it to **Sum**. Now you have a running revenue total without a formula.

**Prompts**
1. Add a **Board** view, group by `Category`.

## Step 6: Add the wiki pages

1. Drag the 3 files from the `/wiki` folder into Notion the same way — `/csv` import works for text too, or just create 3 new pages and paste the Markdown content in directly (Notion renders Markdown headers, bullets, and checkboxes automatically on paste).
2. Pin "How to use this system" to the top of your ForgeHustle Tracker page for reference.

## Done

You now have a linked offer/experiment/content/revenue/prompt system in Notion. Open `wiki/How to use this system.md` for the weekly loop, and `PROMPTS.md` for the prompt library outside of Notion if you'd rather paste from a text file.
