"""
ForgeHabits — local habit tracker (bonus tool)
A ForgeKit product by Orynix Technologies

Run: streamlit run app.py

No API keys. No network calls. No account. State lives in
habits_state.json next to this file. Delete that file to reset everything.

XP and level rules mirror HABIT-LORE.md. If you change the numbers in one
place, change them in the other.
"""

import csv
import json
import os
from datetime import date, timedelta

import streamlit as st

APP_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_PATH = os.path.join(APP_DIR, "habits_state.json")
HABITS_CSV_PATH = os.path.join(APP_DIR, "databases", "Habits.csv")

# --- Level table (must match HABIT-LORE.md) ---------------------------------
LEVELS = [
    (1, 0, "Starting Line"),
    (2, 100, "Warmed Up"),
    (3, 250, "Routine"),
    (4, 450, "Consistent"),
    (5, 700, "Disciplined"),
    (6, 1000, "Load-Bearing"),
    (7, 1400, "Habitual"),
    (8, 1900, "Systemized"),
    (9, 2500, "Unbothered"),
    (10, 3200, "Max Grind"),
]
STREAK_BONUS_CAP = 10


def get_level(total_xp):
    """Return (level_number, title, xp_into_level, xp_for_next) for a given XP total."""
    current = LEVELS[0]
    for entry in LEVELS:
        if total_xp >= entry[1]:
            current = entry
        else:
            break
    idx = LEVELS.index(current)
    if idx + 1 < len(LEVELS):
        next_entry = LEVELS[idx + 1]
        xp_into_level = total_xp - current[1]
        xp_for_next = next_entry[1] - current[1]
    else:
        xp_into_level = total_xp - current[1]
        xp_for_next = None  # maxed out
    return current[0], current[2], xp_into_level, xp_for_next


def compute_streak_from_history(history, last_date_str):
    """Walk backward from last_date through consecutive logged days."""
    streak = 0
    d = date.fromisoformat(last_date_str)
    while d.isoformat() in history:
        streak += 1
        d -= timedelta(days=1)
    return streak


def seed_state_from_csv():
    """Build a fresh state dict from databases/Habits.csv (active habits only)."""
    habits = {}
    if os.path.exists(HABITS_CSV_PATH):
        with open(HABITS_CSV_PATH, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("Active", "Yes").strip().lower() != "yes":
                    continue
                habit_id = row["Habit ID"].strip()
                habits[habit_id] = {
                    "name": row["Habit Name"].strip(),
                    "category": row.get("Category", "").strip(),
                    "difficulty": row.get("Difficulty", "Medium").strip(),
                    "base_xp": int(row.get("Base XP", 10) or 10),
                    "current_streak": 0,
                    "longest_streak": 0,
                    "last_completed_date": None,
                    "history": {},
                }
    return {"habits": habits, "total_xp": 0}


def load_state():
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                pass
    state = seed_state_from_csv()
    save_state(state)
    return state


def save_state(state):
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, sort_keys=True)


def toggle_habit(state, habit_id, today_str):
    h = state["habits"][habit_id]

    if today_str in h["history"]:
        # Un-checking today's completion. Undo the XP and recompute the streak.
        xp_earned = h["history"].pop(today_str)
        state["total_xp"] = max(0, state["total_xp"] - xp_earned)

        dates = sorted(h["history"].keys())
        if dates:
            last_date = dates[-1]
            h["last_completed_date"] = last_date
            h["current_streak"] = compute_streak_from_history(h["history"], last_date)
        else:
            h["last_completed_date"] = None
            h["current_streak"] = 0
    else:
        # Checking today's completion.
        yesterday_str = (date.today() - timedelta(days=1)).isoformat()
        if h["last_completed_date"] == yesterday_str:
            new_streak = h["current_streak"] + 1
        else:
            new_streak = 1

        bonus = min(new_streak, STREAK_BONUS_CAP)
        xp_earned = h["base_xp"] + bonus

        h["current_streak"] = new_streak
        h["longest_streak"] = max(h["longest_streak"], new_streak)
        h["last_completed_date"] = today_str
        h["history"][today_str] = xp_earned
        state["total_xp"] += xp_earned

    save_state(state)


def badges_earned(state):
    """Badges this tracker can detect from local streak/count data alone.
    Time-of-day and calendar-month badges live in HABIT-LORE.md but need
    data this offline tracker doesn't collect (clock time, full-month logs)."""
    earned = []
    habits = state["habits"]
    any_completed = any(h["history"] for h in habits.values())
    max_streak = max([h["longest_streak"] for h in habits.values()], default=0)
    level_num, _, _, _ = get_level(state["total_xp"])

    if any_completed:
        earned.append("First Rep")
    if max_streak >= 3:
        earned.append("Three Days In")
    if max_streak >= 7:
        earned.append("Week One")
    if max_streak >= 30:
        earned.append("The Grind")
    if max_streak >= 100:
        earned.append("Iron Habit")
    if level_num >= 10:
        earned.append("Max Grind")
    return earned


# --- UI -----------------------------------------------------------------
st.set_page_config(page_title="ForgeHabits Tracker", page_icon="✓", layout="centered")

st.markdown(
    """
    <style>
    .fk-mono { font-family: 'JetBrains Mono', 'Courier New', monospace; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("ForgeHabits")
st.caption("Local tracker. No account, no API key, no data leaves this machine.")

state = load_state()
today_str = date.today().isoformat()

if not state["habits"]:
    st.warning(
        "No active habits found. Check that databases/Habits.csv exists next to "
        "app.py and has rows with Active = Yes."
    )
    st.stop()

level_num, level_title, xp_into, xp_for_next = get_level(state["total_xp"])

col1, col2, col3 = st.columns(3)
col1.metric("Total XP", f"{state['total_xp']}")
col2.metric("Level", f"{level_num} — {level_title}")
if xp_for_next is not None:
    col3.metric("XP to next level", f"{xp_for_next - xp_into}")
else:
    col3.metric("XP to next level", "Maxed out")

st.divider()
st.subheader(f"Today — {today_str}")

for habit_id, h in sorted(state["habits"].items(), key=lambda kv: kv[1]["name"]):
    done_today = today_str in h["history"]
    label = f"**{h['name']}**  ·  {h['category']} / {h['difficulty']}  ·  streak {h['current_streak']}"
    checked = st.checkbox(label, value=done_today, key=f"chk_{habit_id}")
    if checked != done_today:
        toggle_habit(state, habit_id, today_str)
        st.rerun()

st.divider()
st.subheader("Streaks")
for habit_id, h in sorted(
    state["habits"].items(), key=lambda kv: kv[1]["current_streak"], reverse=True
):
    st.write(
        f"{h['name']} — current streak **{h['current_streak']}**, "
        f"longest **{h['longest_streak']}**"
    )

st.divider()
st.subheader("Badges")
earned = badges_earned(state)
if earned:
    st.write(", ".join(earned))
else:
    st.write("None yet. Check off a habit above to start.")
st.caption(
    "This tracker only detects streak- and level-based badges. See HABIT-LORE.md "
    "for the full badge list, including ones you track by hand on the Notion dashboard."
)

st.divider()
st.caption(f"State file: {STATE_PATH}")
st.caption("A ForgeKit product by Orynix Technologies")
