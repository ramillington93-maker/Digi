"""
ForgeCalendar — Hook Remixer

Paste a hook, get 5 rewritten variants in different structures:
question, number, contrarian, "how I", and curiosity-gap.

Works with zero setup using rule-based synonym and structure swaps.
If ANTHROPIC_API_KEY or OPENAI_API_KEY is set (in the environment or a
.env file), it upgrades to LLM-written variants instead. If the key is
missing, invalid, or the API call fails for any reason, it falls back
to the rule-based mode automatically — the tool never breaks.

Run: streamlit run app.py
"""

import os
import random
import re

import streamlit as st

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

FORMS = ["Question", "Number", "Contrarian", "How I", "Curiosity Gap"]

# ---------------------------------------------------------------------------
# Rule-based mock mode (no API key required)
# ---------------------------------------------------------------------------

SYNONYMS = {
    "tool": ["app", "tool", "platform"],
    "tools": ["apps", "tools", "platforms"],
    "client": ["customer", "client"],
    "clients": ["customers", "clients"],
    "found": ["discovered", "found", "stumbled onto"],
    "changed": ["changed", "flipped", "transformed"],
    "big": ["big", "huge", "major"],
    "easy": ["easy", "simple", "painless"],
    "fast": ["fast", "quick", "instant"],
    "free": ["free", "no-cost", "zero-dollar"],
    "mistake": ["mistake", "slip-up", "misstep"],
    "secret": ["secret", "trick", "shortcut"],
}

NUMBER_CHOICES = [3, 5, 7]


def _strip_hook(text: str) -> str:
    text = text.strip()
    return text.rstrip(".!? ")


def _lower_first(s: str) -> str:
    return s[0].lower() + s[1:] if s else s


def _swap_one_synonym(text: str, seed: int) -> str:
    """Swap one recognized word for a synonym, deterministically per seed."""
    rng = random.Random(seed)
    words = re.findall(r"[A-Za-z']+|[^A-Za-z']+", text)
    candidates = [i for i, w in enumerate(words) if w.lower() in SYNONYMS]
    if not candidates:
        return text
    idx = rng.choice(candidates)
    word = words[idx]
    options = [o for o in SYNONYMS[word.lower()] if o.lower() != word.lower()]
    if not options:
        return text
    replacement = rng.choice(options)
    if word[0].isupper():
        replacement = replacement.capitalize()
    words[idx] = replacement
    return "".join(words)


def question_form(hook: str) -> str:
    core = _lower_first(_strip_hook(hook))
    return f"Ever wonder how {core}?"


def number_form(hook: str) -> str:
    core = _lower_first(_strip_hook(hook))
    n = random.Random(len(hook)).choice(NUMBER_CHOICES)
    return f"{n} things nobody tells you about how {core}"


def contrarian_form(hook: str) -> str:
    core = _strip_hook(hook)
    core = _swap_one_synonym(core, seed=len(hook) + 1)
    return f"Unpopular opinion: {_lower_first(core)}. Here's the proof."


def how_i_form(hook: str) -> str:
    core = _strip_hook(hook)
    if core.lower().startswith("i "):
        rest = core[2:]
    else:
        rest = _lower_first(core)
    rest = _swap_one_synonym(rest, seed=len(hook) + 2)
    return f"How I {rest}"


def curiosity_gap_form(hook: str) -> str:
    core = _lower_first(_strip_hook(hook))
    core = _swap_one_synonym(core, seed=len(hook) + 3)
    return f"The real reason {core} (most people miss this)"


def rule_based_variants(hook: str) -> list[str]:
    return [
        question_form(hook),
        number_form(hook),
        contrarian_form(hook),
        how_i_form(hook),
        curiosity_gap_form(hook),
    ]


# ---------------------------------------------------------------------------
# Optional LLM upgrade
# ---------------------------------------------------------------------------

LLM_PROMPT = """You rewrite social media hooks into 5 variants using these exact structures, one per line, no numbering, no quotes, no extra commentary:
1. Question form
2. Number/list form
3. Contrarian form
4. "How I" form
5. Curiosity-gap form

Keep each variant under 20 words. Match the original hook's subject matter exactly. Do not invent facts or numbers that weren't implied by the original.

Original hook: {hook}

Return exactly 5 lines, one variant per line."""


def _parse_llm_lines(text: str) -> list[str]:
    lines = [ln.strip(" -*0123456789.").strip() for ln in text.strip().splitlines()]
    lines = [ln for ln in lines if ln]
    return lines[:5]


def try_anthropic_variants(hook: str) -> list[str] | None:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return None
    try:
        import anthropic

        client = anthropic.Anthropic(api_key=api_key)
        resp = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=300,
            messages=[{"role": "user", "content": LLM_PROMPT.format(hook=hook)}],
        )
        text = "".join(
            block.text for block in resp.content if getattr(block, "type", "") == "text"
        )
        variants = _parse_llm_lines(text)
        return variants if len(variants) == 5 else None
    except Exception:
        return None


def try_openai_variants(hook: str) -> list[str] | None:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None
    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=300,
            messages=[{"role": "user", "content": LLM_PROMPT.format(hook=hook)}],
        )
        text = resp.choices[0].message.content or ""
        variants = _parse_llm_lines(text)
        return variants if len(variants) == 5 else None
    except Exception:
        return None


def get_variants(hook: str) -> tuple[list[str], str]:
    """Return (variants, mode) where mode is 'llm' or 'rule-based'."""
    variants = try_anthropic_variants(hook)
    if variants:
        return variants, "llm (Anthropic)"
    variants = try_openai_variants(hook)
    if variants:
        return variants, "llm (OpenAI)"
    return rule_based_variants(hook), "rule-based"


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------

st.set_page_config(page_title="ForgeCalendar — Hook Remixer", page_icon="\U0001F501")

st.title("Hook Remixer")
st.caption("Paste a hook. Get 5 rewrites in different structures. No account needed.")

has_key = bool(os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("OPENAI_API_KEY"))
if has_key:
    st.info("API key detected. Rewrites will use the LLM upgrade, with a rule-based fallback if the call fails.")
else:
    st.info("No API key set — running in rule-based mode. Works fully, no setup required. Add ANTHROPIC_API_KEY or OPENAI_API_KEY to a .env file for LLM rewrites.")

hook_input = st.text_area(
    "Your hook",
    placeholder="I replaced 3 subscriptions with one $20 AI tool.",
    height=100,
)

if st.button("Remix", type="primary"):
    if not hook_input.strip():
        st.warning("Paste a hook first.")
    else:
        variants, mode = get_variants(hook_input.strip())
        st.caption(f"Mode: {mode}")
        for label, variant in zip(FORMS, variants):
            st.markdown(f"**{label}**")
            st.code(variant, language=None)
