# Import the calendar into Notion

Turns `calendar-30-day.csv` into a Notion database with a calendar view. Takes about 3 minutes.

1. In Notion, open the sidebar and click **+ New page**.
2. Type `/import` and select **Import**.
3. Choose **CSV** as the source, then pick `calendar-30-day.csv` from this folder.
4. Notion creates a database with 5 columns: `date`, `platform`, `hook`, `cta`, `asset_type`. Each row becomes a page.
5. Click the `date` column header, select **Edit property**, and change the type from Text to **Date**. Notion parses the `YYYY-MM-DD` format automatically.
6. Click the `platform` column header, change the type to **Select**. Notion auto-creates options for X, Instagram, LinkedIn, and TikTok — assign each a color if you want a visual split.
7. Do the same for `asset_type` (Select) if you want to filter by content format later.
8. Click **+ Add a view** at the top of the database, choose **Calendar**, and set it to use the `date` property.
9. You now have a calendar view: click any day to see the hook, CTA, and asset type due that day.

## Optional: add a status column

Add a `status` property (Select) with options like `Not started`, `Drafted`, `Posted`. Notion won't add this from the CSV, so create it manually and set a default of `Not started` for existing rows.

## Optional: filter by platform

Add a **Board** view grouped by `platform` to see your whole month organized by channel instead of by date — useful if you batch-record videos for TikTok separately from writing LinkedIn posts.
