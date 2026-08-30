"""
ForgeResume — resume optimizer
A ForgeKit product by Orynix Technologies

Run: streamlit run app.py

Core scoring (tokenize -> normalize -> stopword-filter -> overlap) is 100%
offline, no API key needed. An LLM (ANTHROPIC_API_KEY or OPENAI_API_KEY) is
optional and only improves the STAR bullet rewrite and the tailored summary.
Without a key, both fall back to a rule-based template.
"""

import os
import re
import json
from collections import Counter

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# --------------------------------------------------------------------------
# Stopwords — standard English function words. Kept as a plain set so the
# app never needs to download a corpus. Deliberately NOT filtering out
# domain words like "manage", "team", "budget" — those are the signal.
# --------------------------------------------------------------------------
STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an",
    "and", "any", "are", "aren't", "as", "at", "be", "because", "been",
    "before", "being", "below", "between", "both", "but", "by", "can",
    "could", "did", "do", "does", "doing", "don't", "down", "during",
    "each", "few", "for", "from", "further", "had", "has", "have", "having",
    "he", "her", "here", "hers", "herself", "him", "himself", "his", "how",
    "i", "if", "in", "into", "is", "it", "its", "itself", "just", "me",
    "more", "most", "my", "myself", "no", "nor", "not", "now", "of", "off",
    "on", "once", "only", "or", "other", "our", "ours", "ourselves", "out",
    "over", "own", "same", "she", "should", "so", "some", "such", "than",
    "that", "the", "their", "theirs", "them", "themselves", "then", "there",
    "these", "they", "this", "those", "through", "to", "too", "under",
    "until", "up", "very", "was", "we", "were", "what", "when", "where",
    "which", "while", "who", "whom", "why", "will", "with", "would", "you",
    "your", "yours", "yourself", "yourselves", "etc", "e.g", "i.e", "via",
    "per", "using", "used", "use", "including", "include", "includes",
    "within", "across", "also", "may", "must", "shall", "one", "two",
    "three", "new", "based", "role", "job", "work", "years", "year",
    "strong", "ability", "able", "well", "good", "make", "made", "get",
    "gets", "got", "please", "we're", "we'll", "you'll", "you're",
}

# Tokens that survive stopword filtering: letters, digits, and a few
# characters common in tech/skill tokens (C++, C#, Node.js, CI/CD).
TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z0-9+#.\-]*")


def tokenize(text: str) -> list[str]:
    """Split raw text into lowercase candidate tokens."""
    return [t.lower().strip(".-") for t in TOKEN_RE.findall(text or "")]


def stem(word: str) -> str:
    """
    Naive suffix-stripping stemmer. Not Porter, but enough to collapse
    manage/managed/managing/manages to one comparable form so the overlap
    score isn't wrecked by plain verb conjugation or plurals.
    """
    w = word
    if w.endswith("'s"):
        w = w[:-2]
    if len(w) > 4 and w.endswith("ies"):
        w = w[:-3] + "y"
    elif len(w) > 5 and w.endswith("ing"):
        w = w[:-3]
    elif len(w) > 4 and w.endswith("edly"):
        w = w[:-4]
    elif len(w) > 4 and w.endswith("ed") and not w.endswith("eed"):
        w = w[:-2]
    elif len(w) > 4 and w.endswith("es") and w[-3] in "sxzh":
        w = w[:-2]
    elif len(w) > 3 and w.endswith("s") and not w.endswith("ss") and not w.endswith("us"):
        w = w[:-1]
    return w


def normalize(text: str) -> list[str]:
    """
    Full pipeline: tokenize -> lowercase (done in tokenize) -> drop
    stopwords and short/pure-numeric junk -> stem. Returns the stemmed
    tokens in original order (duplicates kept, used for frequency).
    """
    out = []
    for tok in tokenize(text):
        if tok in STOPWORDS:
            continue
        if len(tok) < 2:
            continue
        if tok.replace(".", "").isdigit():
            continue
        out.append(stem(tok))
    return out


def keyword_counts(text: str) -> tuple[Counter, dict]:
    """
    Returns (Counter of stemmed-token -> frequency, display map of
    stemmed-token -> most common original surface form seen for it).
    """
    stems = normalize(text)
    raw = [t.lower() for t in tokenize(text) if t.lower() not in STOPWORDS and len(t) >= 2]
    counts = Counter(stems)
    display = {}
    display_votes: dict[str, Counter] = {}
    for raw_word in raw:
        s = stem(raw_word)
        display_votes.setdefault(s, Counter())[raw_word] += 1
    for s, votes in display_votes.items():
        display[s] = votes.most_common(1)[0][0]
    return counts, display


def compute_match(resume_text: str, jd_text: str, top_n: int = 20) -> dict:
    """
    Real keyword-overlap scoring between a resume and a job description.
    Score = (unique JD keywords also present in resume) / (unique JD
    keywords) * 100. Everything here runs offline — no network calls.
    """
    jd_counts, jd_display = keyword_counts(jd_text)
    resume_counts, _ = keyword_counts(resume_text)

    jd_stems = set(jd_counts.keys())
    resume_stems = set(resume_counts.keys())

    if not jd_stems:
        return {
            "score": 0.0, "matched": [], "missing": [],
            "jd_keyword_count": 0, "matched_count": 0,
        }

    matched_stems = jd_stems & resume_stems
    missing_stems = jd_stems - resume_stems

    score = round(100.0 * len(matched_stems) / len(jd_stems), 1)

    matched = sorted(
        (jd_display.get(s, s) for s in matched_stems),
        key=lambda w: -jd_counts[stem(w)],
    )[:top_n]

    missing_sorted = sorted(missing_stems, key=lambda s: -jd_counts[s])
    missing = [jd_display.get(s, s) for s in missing_sorted][:top_n]

    return {
        "score": score,
        "matched": matched,
        "missing": missing,
        "jd_keyword_count": len(jd_stems),
        "matched_count": len(matched_stems),
    }


# --------------------------------------------------------------------------
# LLM (optional) — used only to improve rewrites/summary. Plain HTTP calls
# via requests, no SDK dependency. Any failure (no key, network, bad
# response) falls back to the rule-based path silently.
# --------------------------------------------------------------------------

def get_llm_key() -> tuple[str | None, str | None]:
    """Returns (provider, key) — provider is 'anthropic' or 'openai', or (None, None)."""
    ak = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if ak:
        return "anthropic", ak
    ok = os.environ.get("OPENAI_API_KEY", "").strip()
    if ok:
        return "openai", ok
    return None, None


def call_llm(prompt: str, max_tokens: int = 400) -> str | None:
    provider, key = get_llm_key()
    if not provider:
        return None
    try:
        if provider == "anthropic":
            resp = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": "claude-3-5-haiku-20241022",
                    "max_tokens": max_tokens,
                    "messages": [{"role": "user", "content": prompt}],
                },
                timeout=20,
            )
            resp.raise_for_status()
            data = resp.json()
            return "".join(b.get("text", "") for b in data.get("content", [])).strip()
        else:
            resp = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}", "content-type": "application/json"},
                json={
                    "model": "gpt-4o-mini",
                    "max_tokens": max_tokens,
                    "messages": [{"role": "user", "content": prompt}],
                },
                timeout=20,
            )
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"].strip()
    except Exception:
        return None


# --------------------------------------------------------------------------
# Rule-based fallbacks (always available, no key required)
# --------------------------------------------------------------------------

WEAK_VERBS = {
    "helped with": "drove", "helped": "drove",
    "worked on": "delivered", "responsible for": "owned",
    "assisted with": "supported", "was in charge of": "led",
    "did": "executed", "handled": "managed",
}

STRONG_OPENERS = ["Led", "Built", "Drove", "Delivered", "Owned", "Launched", "Reduced", "Increased"]

HAS_NUMBER_RE = re.compile(r"\d")


def strengthen_verb(bullet: str) -> str:
    """Replace weak opener phrases with stronger verbs, longest phrase first
    so e.g. 'helped with' isn't left as 'drove with' after 'helped' matches."""
    b = bullet
    for weak, strong in sorted(WEAK_VERBS.items(), key=lambda kv: -len(kv[0])):
        b = re.sub(re.escape(weak), strong, b, flags=re.IGNORECASE)
    return b


def rule_based_rewrite(bullet: str, missing_keywords: list[str]) -> str:
    """
    Template STAR rewrite with no LLM. Pulls in 1-2 missing JD keywords
    where they fit naturally, flags the bullet for a metric if none exists.
    """
    bullet = bullet.strip().rstrip(".")
    if not bullet:
        return ""
    action = strengthen_verb(bullet)
    kws = missing_keywords[:2]
    kw_phrase = f" using {' and '.join(kws)}" if kws else ""
    has_metric = bool(HAS_NUMBER_RE.search(bullet))

    situation = "In a role facing a clear gap between current output and target goals,"
    task = f"the objective was to {bullet[0].lower() + bullet[1:]}."
    action_line = f"Action: {action}{kw_phrase}."
    if has_metric:
        result = "Result: " + bullet + " (quantify further if possible — % change, $ saved, time cut)."
    else:
        result = ("Result: [ADD A NUMBER HERE — e.g. % improvement, $ saved, time reduced, "
                   "team size, or volume handled]. A bullet without a number is a bullet "
                   "reviewers skip.")

    return (
        f"**Situation:** {situation}\n\n"
        f"**Task:** {task}\n\n"
        f"**{action_line}**\n\n"
        f"**{result}**"
    )


def llm_rewrite(bullet: str, jd_text: str, missing_keywords: list[str]) -> tuple[str, bool]:
    """Returns (rewrite_text, used_llm)."""
    provider, _ = get_llm_key()
    if provider:
        kw_hint = ", ".join(missing_keywords[:6]) or "none"
        prompt = (
            "Rewrite this resume bullet in STAR format (Situation, Task, Action, Result). "
            "Keep it to 4 short lines, one per STAR component, each starting with the bold "
            "label. Be concrete. Invent a plausible metric only if the original has none, "
            "and mark it clearly as a placeholder to fill in. Naturally weave in up to 2 of "
            f"these job-description keywords if they fit: {kw_hint}.\n\n"
            f"Original bullet: {bullet}"
        )
        result = call_llm(prompt, max_tokens=300)
        if result:
            return result, True
    return rule_based_rewrite(bullet, missing_keywords), False


def rule_based_summary(resume_text: str, matched: list[str], missing: list[str]) -> str:
    years_match = re.search(r"(\d+)\+?\s*years?", resume_text, re.IGNORECASE)
    years = years_match.group(1) if years_match else "several"
    top_matched = matched[:5]
    top_missing = missing[:3]
    skills_line = ", ".join(top_matched) if top_matched else "the core skills this role needs"
    gap_line = (
        f" Adds working exposure to {', '.join(top_missing)} to close the remaining gap with the posting."
        if top_missing else ""
    )
    return (
        f"Results-driven professional with {years} years of experience delivering measurable "
        f"outcomes in fast-moving teams. Proven strength in {skills_line}, applied to real "
        f"projects with tracked results, not just responsibilities.{gap_line} Looking to bring "
        f"that track record to a role that rewards execution over busywork."
    )


def llm_summary(resume_text: str, jd_text: str, matched: list[str], missing: list[str]) -> tuple[str, bool]:
    provider, _ = get_llm_key()
    if provider:
        prompt = (
            "Write a 3-4 sentence tailored professional summary for the TOP of a resume, "
            "aimed at the job description below. Ground it in the resume's real background — "
            "don't invent employers or titles. Naturally include these already-matching "
            f"strengths: {', '.join(matched[:6]) or 'none found'}. If natural, note growth "
            f"toward these gap areas: {', '.join(missing[:3]) or 'none'}. No hype words "
            "(empower, unlock, elevate, seamless, revolutionize, game-changer, supercharge, "
            "unleash). Plain, concrete, money-aware tone.\n\n"
            f"RESUME:\n{resume_text[:3000]}\n\nJOB DESCRIPTION:\n{jd_text[:2000]}"
        )
        result = call_llm(prompt, max_tokens=300)
        if result:
            return result, True
    return rule_based_summary(resume_text, matched, missing), False


# --------------------------------------------------------------------------
# Streamlit UI
# --------------------------------------------------------------------------

st.set_page_config(page_title="ForgeResume", page_icon="\U0001F4C4", layout="wide")

st.markdown(
    """
    <style>
    .fk-tag {display:inline-block; background:#141B24; color:#F5B942;
             border:1px solid #F5B942; border-radius:999px; padding:2px 10px;
             font-size:0.8rem; margin:2px 4px 2px 0;}
    .fk-tag-missing {border-color:#9BA8B4; color:#E8EEF4;}
    .fk-footer {color:#9BA8B4; font-size:0.85rem; margin-top:2rem;
                border-top:1px solid #141B24; padding-top:0.75rem;}
    .fk-score {font-family:'JetBrains Mono', monospace;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("ForgeResume")
st.caption("Ship today. Cash tomorrow. — Paste a resume and a job post. Get a real match score, "
           "the exact keywords you're missing, and stronger bullets. No account, no upload to a server.")

provider, _ = get_llm_key()
if provider:
    st.info(f"LLM rewrite active ({provider}). Bullet rewrites and summary will use it.", icon="✅")
else:
    st.warning(
        "No ANTHROPIC_API_KEY or OPENAI_API_KEY found — running on rule-based rewrites only. "
        "Scoring and missing-keyword detection are fully offline either way.",
        icon="ℹ️",
    )

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Your resume")
    resume_file = st.file_uploader("Upload .txt", type=["txt"], key="resume_upload")
    default_resume = resume_file.read().decode("utf-8", errors="ignore") if resume_file else ""
    resume_text = st.text_area("Or paste resume text", value=default_resume, height=280, key="resume_text")

with col2:
    st.subheader("2. Target job description")
    jd_file = st.file_uploader("Upload .txt", type=["txt"], key="jd_upload")
    default_jd = jd_file.read().decode("utf-8", errors="ignore") if jd_file else ""
    jd_text = st.text_area("Or paste job description text", value=default_jd, height=280, key="jd_text")

analyze = st.button("Analyze match", type="primary")

if analyze:
    if not resume_text.strip() or not jd_text.strip():
        st.error("Paste (or upload) both a resume and a job description first.")
    else:
        result = compute_match(resume_text, jd_text)
        st.session_state["fk_result"] = result
        st.session_state["fk_resume"] = resume_text
        st.session_state["fk_jd"] = jd_text

if "fk_result" in st.session_state:
    result = st.session_state["fk_result"]
    resume_text = st.session_state["fk_resume"]
    jd_text = st.session_state["fk_jd"]

    st.divider()
    st.subheader("Match score")
    score = result["score"]
    c1, c2 = st.columns([1, 3])
    with c1:
        st.metric("Keyword overlap", f"{score}%")
    with c2:
        st.progress(min(int(score), 100) / 100)
        st.caption(
            f"{result['matched_count']} of {result['jd_keyword_count']} distinct keywords "
            f"from the job description also appear in your resume."
        )

    mcol, gcol = st.columns(2)
    with mcol:
        st.markdown("**Matched keywords**")
        if result["matched"]:
            st.markdown(
                "".join(f'<span class="fk-tag">{w}</span>' for w in result["matched"]),
                unsafe_allow_html=True,
            )
        else:
            st.caption("No overlap found.")
    with gcol:
        st.markdown("**Missing keywords** — add these if they're true of you")
        if result["missing"]:
            st.markdown(
                "".join(f'<span class="fk-tag fk-tag-missing">{w}</span>' for w in result["missing"]),
                unsafe_allow_html=True,
            )
        else:
            st.caption("Nothing missing — strong match.")

    st.divider()
    st.subheader("3. Rewrite a weak bullet (STAR format)")
    st.caption("Paste one bullet you're not happy with. Uses your missing keywords above where they fit.")
    bullet_input = st.text_area("Weak bullet", height=80, key="bullet_input",
                                 placeholder="e.g. Helped with social media and worked on some campaigns.")
    if st.button("Rewrite bullet"):
        if bullet_input.strip():
            rewrite_text, used_llm = llm_rewrite(bullet_input, jd_text, result["missing"])
            st.session_state["fk_rewrite"] = (rewrite_text, used_llm)
        else:
            st.error("Paste a bullet first.")

    if "fk_rewrite" in st.session_state:
        rewrite_text, used_llm = st.session_state["fk_rewrite"]
        st.markdown(rewrite_text)
        st.caption("Generated with LLM" if used_llm else "Generated with rule-based template (no API key)")

    st.divider()
    st.subheader("4. Tailored professional summary")
    if st.button("Generate summary"):
        summary_text, used_llm = llm_summary(resume_text, jd_text, result["matched"], result["missing"])
        st.session_state["fk_summary"] = (summary_text, used_llm)

    if "fk_summary" in st.session_state:
        summary_text, used_llm = st.session_state["fk_summary"]
        st.text_area("Summary (copy into the top of your resume)", value=summary_text, height=140)
        st.caption("Generated with LLM" if used_llm else "Generated with rule-based template (no API key)")

st.markdown('<div class="fk-footer">A ForgeKit product by Orynix Technologies</div>', unsafe_allow_html=True)
