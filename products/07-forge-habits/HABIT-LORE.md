# HABIT-LORE.md — ForgeHabits XP System

This is the rulebook. Every number the Notion dashboard and the Streamlit
tracker use comes from this file. If you change a value here, change it in
both places or your XP totals will stop matching.

## XP per habit

Every habit has a Difficulty, set on the Habits database. Difficulty sets
Base XP.

| Difficulty | Base XP | Example |
|---|---|---|
| Easy | 5 | Read 20 pages, meditate 10 min |
| Medium | 10 | Morning run, no phone after 10pm |
| Hard | 20 | Cold shower, Sunday meal prep |

You set the difficulty. Nobody's cold shower is the same as yours.

## Streak bonus

Every day you extend a streak, you earn a bonus on top of Base XP:

```
Streak Bonus = min(current streak day, 10)
XP Earned    = Base XP + Streak Bonus
```

The bonus caps at +10 XP once you hit a 10-day streak on that habit. Past
day 10, the streak keeps building for badges, but the XP bonus stops
climbing — otherwise a 300-day streak turns one checkbox into a full day's
XP, and that's not the game.

Miss a day and the streak resets to 0. The bonus resets with it. Base XP
does not change — you still get credit for the habit itself.

**Example:** Morning Run (Medium, Base XP 10) on streak day 14.
Streak Bonus = min(14, 10) = 10. XP Earned = 10 + 10 = 20.

## Levels

Levels run on total lifetime XP, not weekly or monthly XP. There is no
level decay. What you've earned, you keep.

| Level | XP Required | Title |
|---|---|---|
| 1 | 0 | Starting Line |
| 2 | 100 | Warmed Up |
| 3 | 250 | Routine |
| 4 | 450 | Consistent |
| 5 | 700 | Disciplined |
| 6 | 1,000 | Load-Bearing |
| 7 | 1,400 | Habitual |
| 8 | 1,900 | Systemized |
| 9 | 2,500 | Unbothered |
| 10 | 3,200 | Max Grind |

Level 10 is the ceiling. There's no Level 11. If you hit Max Grind, that's
not a bug — go add a harder habit.

## Badges

Badges are earned once and don't expire, except where noted. Track them
manually on the dashboard (see NOTION-SETUP.md) or let the Streamlit
tracker flag the ones it can detect from local data (streak- and
count-based badges only — it has no calendar-time or clock-time data).

| Badge | Unlock Criteria |
|---|---|
| First Rep | Log any habit as completed, once. |
| Three Days In | Reach a 3-day streak on any single habit. |
| Week One | Reach a 7-day streak on any single habit. |
| The Grind | Reach a 30-day streak on any single habit. |
| Iron Habit | Reach a 100-day streak on any single habit. |
| No Zero Days | Log at least one habit completed every day for a full calendar month. |
| Comeback | Restart a habit and rebuild a 7-day streak after a streak break of 7+ days. |
| Stacked | Complete 3 or more habits in a single day. Five separate times. |
| Early Riser | Log a habit completed before 7:00 AM. Ten times. |
| Night Owl | Log a habit completed after 10:00 PM. Ten times. |
| Completionist | Hit 100% completion on every active habit for one full week. |
| Reward Redeemer | Redeem 5 rewards from the Rewards database, lifetime. |
| Max Grind | Reach Level 10. |

That's 13 badges. Nobody needs 40 badges. Half of them would just be
"logged in."

## Rewards economy

Rewards cost XP, same currency as levels. Redeeming a reward does not
subtract from your level — level XP is lifetime and never goes down.
Reward XP is a separate spendable balance you track on the Rewards
database (Redeemed Count, running total). Think of it as: levels are your
resume, rewards are your bank account.

Suggested pricing bands, already in Rewards.csv as a starting point:

| Band | XP Cost | Example |
|---|---|---|
| Small | 50–100 | One guilt-free episode, skip one chore |
| Medium | 150–300 | Takeout night, a new book |
| Large | 600+ | Massage, a weekend trip |

Set your own prices. A massage should cost more than a rerun.

## Why cap the streak bonus instead of letting it grow forever

Because uncapped streak multipliers are how gamified trackers turn into
number-go-up machines that reward you for opening the app, not for doing
the habit. The cap keeps the badges — not the XP curve — as the long-term
carrot. Read the badge list again. That's the actual game.
