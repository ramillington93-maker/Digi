# ForgeHabits

A gamified habit tracker you build in Notion in about 20 minutes, plus a
tiny local tracker for people who'd rather check boxes than click through
Notion every morning.

A ForgeKit product by Orynix Technologies.

## What it does

- Gives you a real XP and level system for your habits — not "great job!"
  toasts, actual numbers: base XP by difficulty, a streak bonus that caps
  at +10, and a 10-level ladder from Starting Line to Max Grind.
- Ships as 4 Notion-ready databases (Habits, Logs, Rewards, Streaks) with
  sample data already in them, so you can see the system working before
  you touch a single setting.
- Includes 13 named badges with concrete unlock criteria (streak length,
  completion counts, level reached) — no vague "consistency achievement"
  nonsense.
- Comes with a rewards economy: spend XP on things you already enjoy
  (an episode, a takeout night, a massage), priced in the same currency
  as your levels.
- Includes an optional local Streamlit tracker — check off today's
  habits, see your streak and XP total, done. Runs on your machine, no
  account, no API key, no data leaves your computer.

## What it does NOT do

This is a template, not live automation. Notion has no built-in way to
auto-increment a streak counter overnight without a paid third-party
tool — you either update Current Streak by hand, or use the Streamlit
tracker as your source of truth and copy the number over. Pick one and
stick with it. See NOTION-SETUP.md, "What this does NOT do automatically."

## 3-step setup

1. **Import the databases.** In Notion, create a page called ForgeHabits
   and import each CSV in `/databases/` as its own database (`/table` →
   Import → CSV). Full column-by-column instructions, including which
   fields to convert to Select/Checkbox/Number, are in
   `NOTION-SETUP.md`.
2. **Wire the relations and rollups.** Link Logs and Streaks to Habits,
   then add two rollups on Habits (Total XP Earned, Times Completed).
   This is the 10-minute part — `NOTION-SETUP.md` walks through it step
   by step, including the views to build (Today, This Week, Calendar,
   Leaderboard).
3. **(Optional) Run the local tracker.** `pip install -r requirements.txt`
   then `streamlit run app.py`. Check off today's habits. Your streak and
   XP total update on screen and get written to `habits_state.json` next
   to `app.py`. No setup beyond that — no login, no API key.

## Example

Say you run 3 days in a row (Medium difficulty, base 10 XP). Day 1: 10 +
1 streak bonus = 11 XP. Day 2: 10 + 2 = 12 XP. Day 3: 10 + 3 = 13 XP. The
bonus caps at +10 once your streak hits 10 days, so a 40-day streak earns
the same per-day XP as an 11-day streak — the badges are what keep
climbing, not the number. Full rules, the level thresholds, and all 13
badges are in `HABIT-LORE.md`.

See `sample-output/` for a rendered look at both the Notion dashboard and
the Streamlit tracker using the sample data.

## What's included

```
07-forge-habits/
├── README.md                          (this file)
├── SALES.md                           Gumroad listing copy
├── LICENSE.txt                        buyer license
├── DEMO.md                            steps to record a 20-second demo
├── NOTION-SETUP.md                    exact Notion build steps
├── HABIT-LORE.md                      XP system, levels, 13 badges
├── app.py                             optional local tracker (Streamlit)
├── requirements.txt                   one dependency: streamlit
├── .streamlit/config.toml             dark theme for the tracker
├── databases/
│   ├── Habits.csv                     8 sample habits
│   ├── Logs.csv                       8 sample completion logs
│   ├── Rewards.csv                    7 sample rewards
│   └── Streaks.csv                    8 sample streak rows
└── sample-output/
    ├── habits_state-example.json      real output from app.py's logic
    ├── tracker-preview.txt            what the tracker screen looks like
    └── notion-dashboard-preview.md    what the Notion dashboard looks like
```

## FAQ

**Do I need a Notion paid plan?** No. Free plan supports unlimited
databases, relations, and rollups for personal use.

**Does the Streamlit tracker sync with my Notion dashboard?** No, and it
doesn't try to. They're two independent tools reading the same rules from
`HABIT-LORE.md`. If you want one number to trust, pick the tracker or
pick Notion and update the other by hand.

**Do I need Python experience to run the tracker?** No. Install Python,
run two commands (`pip install -r requirements.txt`, then
`streamlit run app.py`). If that's unfamiliar, skip it — the Notion
template is the full product on its own.

**Can I change the XP values, level thresholds, or badges?** Yes. Edit
`HABIT-LORE.md` for the rules, edit `databases/Habits.csv` (or the
`LEVELS` list at the top of `app.py`) to match. Keep both in sync or your
numbers will disagree with each other.

**What happens if I delete habits_state.json?** The tracker rebuilds it
from `databases/Habits.csv` on next launch, with everyone back at 0 XP
and 0 streak. That's your reset button.

**Can I use this for a team or a client?** The license covers unlimited
personal and client use. You can't resell the template files themselves.
See `LICENSE.txt`.

## License

See `LICENSE.txt`. Short version: use it, modify it, run it for yourself
or clients, keep the commercial output you make with it. Don't resell or
repackage the product files themselves.

---
A ForgeKit product by Orynix Technologies. Ship today. Cash tomorrow.
