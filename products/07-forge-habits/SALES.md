# SALES.md — Gumroad listing copy for ForgeHabits

## Title
ForgeHabits — Gamified Habit Tracker for Notion

## Subtitle
XP, levels, streaks, and 13 named badges. Notion template plus an
optional local tracker. No API key, no subscription.

## Pitch (~120 words)

Most Notion habit trackers give you a checkbox and a streak number.
ForgeHabits gives you a real progression system: base XP by difficulty,
a streak bonus that caps at +10 so long streaks don't break the math,
and 10 levels from Starting Line to Max Grind. Import 4 databases
(Habits, Logs, Rewards, Streaks), already loaded with sample data, wire
up the relations in about 20 minutes, and you're checking off habits
against a system that actually tracks XP instead of just showing a
calendar full of green squares. Thirteen badges with concrete unlock
criteria — streak length, completion counts, level reached, not "great
job" vibes. A rewards database lets you spend XP on things you already
enjoy. Includes a small optional Streamlit tracker if you'd rather check
boxes outside Notion — runs locally, no account, no API key.

## 5 bullets

- 4 pre-built Notion databases (Habits, Logs, Rewards, Streaks) with
  sample data, plus exact setup steps for relations, rollups, and views.
- Real XP system: base XP by difficulty, streak bonus capped at +10,
  10 levels with named thresholds — all documented in HABIT-LORE.md.
- 13 named badges with hard unlock criteria (3-day streak, 100-day
  streak, level 10, etc.) — no vague achievement fluff.
- Rewards economy: price real-life rewards in XP so leveling up buys you
  something, not just a number going up.
- Optional local Streamlit tracker included — check off today's habits,
  see streak and XP live, zero API keys, zero accounts.

## Who it's for

- People who've tried a habit tracker before, kept it for 4 days, and
  quit because there was no reason to open it on day 5.
- Notion users who want a system with actual rules, not just a database
  template with checkboxes.
- Anyone who wants a habit tracker that works completely offline and
  doesn't ask for an email address, a login, or a subscription.

## Who it's not for

- Anyone who wants push notifications, phone reminders, or a mobile app
  — this is Notion plus an optional desktop tool, not an app store
  product.
- Anyone who wants the streak counter to update itself overnight with no
  manual step — Notion can't do that without a paid automation add-on,
  and this template says so upfront (see NOTION-SETUP.md).
- Teams wanting shared multi-user tracking out of the box — this is
  built for one person's habits, though you can duplicate it per person.

## What's included

- README.md, NOTION-SETUP.md, HABIT-LORE.md, DEMO.md, LICENSE.txt
- 4 CSVs pre-loaded with realistic sample data (Habits, Logs, Rewards,
  Streaks)
- Optional Streamlit tracker (app.py) with a matching dark theme
- Sample output showing the finished dashboard and tracker

## FAQ

**Is this a Notion template link or files I import myself?** Files you
import yourself — 4 CSVs plus a full setup guide. This keeps the price
down and means you own real files, not a link that can break.

**Do I need to know Python to use this?** No. The Notion template is the
full product. The Streamlit tracker is optional and needs two terminal
commands if you want it.

**Will my streaks update automatically overnight?** Not inside Notion —
that needs a paid automation tool Notion doesn't include free. You
update it by hand, or use the included tracker as your source of truth
and skip manual updates entirely.

**Can I customize the XP values and badges?** Yes, everything is defined
in one file (HABIT-LORE.md) so you can retune the whole system without
hunting through formulas.

## Suggested price

$15 USD (reasonable range: $12–$19). At $15, the pitch is: cheaper than
one month of most habit-tracker apps, and it's yours forever — no
subscription, runs offline.
