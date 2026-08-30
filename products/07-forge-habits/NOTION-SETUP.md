# NOTION-SETUP.md — Build the ForgeHabits Dashboard

Setup time: about 20 minutes. Everything below is manual — no Notion API,
no integration, no template button. You're building 4 databases and
wiring them together. That's the whole job.

## What you're building

4 linked databases (Habits, Logs, Rewards, Streaks) and one dashboard page
that shows today's habits, current streaks, and total XP. The CSVs in
`/databases/` are your starting data — import them, then rebuild the
relations by hand (Notion's CSV import does not preserve relations).

## Step 1 — Create the parent page

1. In Notion, create a new page called **ForgeHabits**.
2. Add a callout block at the top with your current Level and XP total
   (you'll update this by hand weekly, or read it off the Streamlit
   tracker — see README.md).

## Step 2 — Import the 4 databases

For each CSV in `/databases/` (Habits.csv, Logs.csv, Rewards.csv,
Streaks.csv):

1. Inside the ForgeHabits page, type `/table` → **Import** → **CSV** and
   select the file.
2. Notion creates a full-page database named after the file. Rename it by
   dropping the `.csv` (e.g. "Habits").
3. Check column types on import — Notion usually guesses text. Fix these:
   - Habits: **Difficulty** → Select. **Active** → Checkbox (retype
     Yes/No as checked/unchecked). **Base XP** → Number.
   - Logs: **Completed** → Checkbox. **XP Earned**, **Streak Day** →
     Number. **Date** → Date.
   - Rewards: **XP Cost**, **Redeemed Count** → Number. **Last
     Redeemed** → Date.
   - Streaks: **Current Streak**, **Longest Streak** → Number. **Last
     Completed**, **Streak Started** → Date. **Status** → Select
     (Active / Broken / Paused).

## Step 3 — Add relations

Relations connect the databases so a log entry can pull in its habit's
name and difficulty automatically.

1. Open **Logs**. Add a new property → **Relation** → point it at
   **Habits**. Name it "Habit".
2. For each row in Logs, link it to the matching Habit ID row (e.g. L001
   → H001, Morning Run).
3. Open **Streaks**. Add a **Relation** property pointing at **Habits**,
   same process, so each streak row is tied to its habit.
4. Back in **Habits**, you'll now see two new properties auto-created:
   "Related Logs" and "Related Streaks" (Notion adds the reverse side of
   a relation automatically). Leave these — they're what let you roll up
   totals.

## Step 4 — Add rollups (auto-calculated totals)

On the **Habits** database, add two rollup properties:

1. **Total XP Earned** → Property: Related Logs → Property: XP Earned →
   Calculate: Sum.
2. **Times Completed** → Property: Related Logs → Property: Completed →
   Calculate: Count checked.

These update automatically every time you add a Log row. This is the
entire "engine" of the dashboard — everything else is a view on top of
this.

## Step 5 — Build the views

Create these views on the **Logs** database (top of the database, click
**+ Add a view**):

1. **Today** — Filter: Date = Today. Sort: Time Logged, descending. This
   is your daily checklist — the only view you touch every day.
2. **This Week** — Filter: Date is within the past 7 days. Group by:
   Habit (via the relation). Shows completion pattern at a glance.
3. **Calendar** — View type: Calendar, dated by Date. Visual streak
   check — gaps are obvious.

On the **Habits** database:

4. **Active Habits** — Filter: Active = checked. This is your default
   view; hide inactive/paused habits from daily view without deleting
   them.
5. **By Category** — Group by: Category (Body / Mind / Craft / Chore).

On the **Streaks** database:

6. **Leaderboard** — Sort: Current Streak, descending. Your longest
   active streak sits at the top — the one habit you cannot afford to
   break today.

## Step 6 — Wire the dashboard page

Back on the ForgeHabits parent page:

1. Add a **Linked view** of Logs → Today's view. This is your check-off
   list.
2. Add a **Linked view** of Streaks → Leaderboard.
3. Add a **Linked view** of Rewards, sorted by XP Cost ascending — so you
   always see what you can afford next.
4. Update the callout block at the top with your Level and total XP,
   using the thresholds in HABIT-LORE.md. This one field you keep in
   sync by hand, or copy the number straight from the Streamlit tracker.

## Daily use

Every day: open the **Today** view, check off what you did, add a new Log
row for anything not already templated in (or duplicate yesterday's rows
and just flip the checkbox and date). Once a week, check the
**Leaderboard** and **By Category** views to see what's slipping.

## What this does NOT do automatically

Notion has no formula that reads "yesterday's row" to auto-increment a
streak counter without a paid automation or third-party tool. Streak Day
and Current Streak in this template are numbers you update by hand, or
numbers you get for free from the Streamlit tracker (which computes
streaks from local data with real logic — see README.md). Decide which
one is your source of truth and stick with it; don't run both and expect
them to agree.
