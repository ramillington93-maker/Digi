"""
ForgeOutreach — cold email sequence builder.
A ForgeKit product by Orynix Technologies.

Run with: streamlit run app.py

No API key required. Sequences are built from real templating logic
(offer / ICP / proof point filled into day-specific angles). If
ANTHROPIC_API_KEY or OPENAI_API_KEY is set, an optional "AI polish" pass
can rewrite the tone — if that call fails or no key is set, the app
falls back to the template output. Nothing is ever sent: this tool only
generates text.
"""

import csv
import io
import os

import streamlit as st

try:
    import requests
except ImportError:  # pragma: no cover - requests ships in requirements.txt
    requests = None

APP_NAME = "ForgeOutreach"
TAGLINE = "Ship today. Cash tomorrow."

# ---------------------------------------------------------------------------
# Templating engine
# ---------------------------------------------------------------------------

def _clean(text: str) -> str:
    """Collapse whitespace, strip edges."""
    return " ".join((text or "").split()).strip()


def _strip_period(text: str) -> str:
    return text[:-1] if text.endswith(".") else text


def _short(text: str, limit: int = 42) -> str:
    text = _clean(text)
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def _sentence(text: str) -> str:
    """Ensure a chunk of user text reads as a standalone sentence."""
    text = _clean(text)
    if not text:
        return text
    if text[-1] not in ".!?":
        text += "."
    return text[0].upper() + text[1:]


def generate_sequence(offer: str, icp: str, proof: str,
                       your_name: str = "", your_company: str = "") -> list:
    """
    Build a 5-email cold outreach sequence (day 0, 2, 4, 7, 12) from three
    inputs: the offer, the ideal customer profile, and a proof point.

    Returns a list of 5 dicts with keys:
    day, angle, subject_a, subject_b, body, linkedin_dm
    """
    offer_raw = _clean(offer) or "a tool that saves your ideal customer time or money"
    icp_raw = _clean(icp) or "busy operators who own this problem"
    proof_raw = _clean(proof) or "early users saw results in the first week"

    offer_s = _strip_period(offer_raw)
    icp_s = _strip_period(icp_raw)
    proof_s = _sentence(proof_raw)

    sign = _clean(your_name) or "{{your_name}}"
    company_token = "{{company}}"
    first_token = "{{first_name}}"

    offer_subj = _short(offer_s, 46)
    icp_subj = _short(icp_s, 40)
    proof_subj = _short(proof_raw, 46)

    rows = []

    # --- Day 0: Intro ---------------------------------------------------
    body = (
        f"Hi {first_token},\n\n"
        f"I'll keep this short. I work with {icp_s}, and most of them are "
        f"losing hours to outreach that doesn't convert.\n\n"
        f"{_sentence(offer_s)}\n\n"
        f"{proof_s}\n\n"
        f"No pitch yet, just checking if this is something {company_token} "
        f"is dealing with right now. If it's not, tell me and I'll leave it "
        f"there.\n\n"
        f"Worth 15 minutes this week?\n\n"
        f"{sign}"
    )
    dm = (
        f"Hey {first_token} — sent you a note over email about {offer_subj}. "
        f"{proof_s} Worth a quick chat?"
    )
    rows.append({
        "day": 0,
        "angle": "Intro",
        "subject_a": f"Quick one, {first_token}",
        "subject_b": f"{offer_subj}?",
        "body": body,
        "linkedin_dm": dm,
    })

    # --- Day 2: Value / proof --------------------------------------------
    body = (
        f"Hi {first_token},\n\n"
        f"Following up with proof instead of asking you to take my word "
        f"for it: {proof_s}\n\n"
        f"That's not luck. It's what happens when {icp_s} stop guessing at "
        f"outreach and use something built for the problem. "
        f"{_sentence(offer_s)}\n\n"
        f"Happy to send over exactly how it works. Interested?\n\n"
        f"{sign}"
    )
    dm = (
        f"Following up here too — {proof_s} Happy to share exactly how it "
        f"works if that's useful."
    )
    rows.append({
        "day": 2,
        "angle": "Value / proof",
        "subject_a": "The number that made me write this",
        "subject_b": f"{proof_subj}",
        "body": body,
        "linkedin_dm": dm,
    })

    # --- Day 4: Case study angle ------------------------------------------
    body = (
        f"Hi {first_token},\n\n"
        f"Short version of why I keep emailing: someone in a spot a lot "
        f"like {company_token}'s — one of {icp_s} — was spending hours a "
        f"week on outreach with nothing to show for it.\n\n"
        f"They switched to {offer_s}. Result: {proof_s}\n\n"
        f"I'm not saying your situation is identical. I'm saying it's "
        f"worth 15 minutes to find out if it applies to {company_token}.\n\n"
        f"Open to it?\n\n"
        f"{sign}"
    )
    dm = (
        f"Quick one: a {icp_subj} used {offer_subj} and got this — "
        f"{proof_s} Thought of you."
    )
    rows.append({
        "day": 4,
        "angle": "Case study",
        "subject_a": "How one of your peers solved this",
        "subject_b": "A quick story before I stop emailing",
        "body": body,
        "linkedin_dm": dm,
    })

    # --- Day 7: Objection handling -----------------------------------------
    body = (
        f"Hi {first_token},\n\n"
        f"If you haven't replied because this feels like one more tool to "
        f"manage, or the timing's off, that's fair. Most {icp_s} are "
        f"already stretched thin.\n\n"
        f"Here's the honest pitch: {offer_s}. Setup takes minutes, not "
        f"weeks. {proof_s}\n\n"
        f"If it's genuinely not a priority right now, say so and I'll stop "
        f"following up. If it's worth a look, one line back is all it "
        f"takes.\n\n"
        f"{sign}"
    )
    dm = (
        f"No worries if now isn't the time for {offer_subj} — didn't want "
        f"it buried in your inbox. Let me know either way."
    )
    rows.append({
        "day": 7,
        "angle": "Objection handling",
        "subject_a": '"We already have something for this"',
        "subject_b": "In case timing is the real blocker",
        "body": body,
        "linkedin_dm": dm,
    })

    # --- Day 12: Breakup ----------------------------------------------------
    body = (
        f"Hi {first_token},\n\n"
        f"I've sent a few notes about {offer_s} and haven't heard back, so "
        f"I'll take the hint and close this out.\n\n"
        f"If priorities change: {proof_s} The offer stands whenever "
        f"{company_token} wants it.\n\n"
        f"No hard feelings. I'll stop here unless you tell me otherwise.\n\n"
        f"{sign}"
    )
    dm = (
        f"Last one from me — closing the loop on {offer_subj}. Ping me if "
        f"it becomes relevant later."
    )
    rows.append({
        "day": 12,
        "angle": "Breakup",
        "subject_a": "Closing the loop",
        "subject_b": "Should I stop emailing?",
        "body": body,
        "linkedin_dm": dm,
    })

    return rows


# ---------------------------------------------------------------------------
# Optional AI polish (degrades gracefully with no key / no network)
# ---------------------------------------------------------------------------

def ai_polish_body(body: str, offer: str, icp: str, proof: str) -> tuple:
    """
    Try to rewrite one email body with an LLM for a sharper tone.
    Returns (text, used_ai: bool). On any failure, returns the original
    body untouched and used_ai=False — the app never breaks without a key
    or without network access.
    """
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")
    if requests is None or (not anthropic_key and not openai_key):
        return body, False

    prompt = (
        "Rewrite this cold outreach email to be sharper and more concrete, "
        "same length or shorter, same facts, keep every {{merge_field}} "
        "token exactly as written, no hype words, no exclamation points. "
        f"Offer: {offer}\nICP: {icp}\nProof point: {proof}\n\n"
        f"Email:\n{body}"
    )
    try:
        if anthropic_key:
            resp = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": anthropic_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": "claude-3-5-haiku-20241022",
                    "max_tokens": 400,
                    "messages": [{"role": "user", "content": prompt}],
                },
                timeout=20,
            )
            resp.raise_for_status()
            text = resp.json()["content"][0]["text"].strip()
            return text, True
        if openai_key:
            resp = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {openai_key}",
                    "content-type": "application/json",
                },
                json={
                    "model": "gpt-4o-mini",
                    "max_tokens": 400,
                    "messages": [{"role": "user", "content": prompt}],
                },
                timeout=20,
            )
            resp.raise_for_status()
            text = resp.json()["choices"][0]["message"]["content"].strip()
            return text, True
    except Exception:
        return body, False
    return body, False


# ---------------------------------------------------------------------------
# Export builders
# ---------------------------------------------------------------------------

def build_txt(rows: list, offer: str, icp: str, proof: str) -> str:
    lines = [
        f"{APP_NAME} — 5-email cold outreach sequence",
        f"Offer: {_clean(offer)}",
        f"ICP: {_clean(icp)}",
        f"Proof point: {_clean(proof)}",
        "=" * 60,
        "",
    ]
    for r in rows:
        lines.append(f"DAY {r['day']} — {r['angle']}")
        lines.append(f"Subject A: {r['subject_a']}")
        lines.append(f"Subject B: {r['subject_b']}")
        lines.append("")
        lines.append(r["body"])
        lines.append("")
        lines.append("LinkedIn DM:")
        lines.append(r["linkedin_dm"])
        lines.append("-" * 60)
        lines.append("")
    return "\n".join(lines)


def build_csv(rows: list) -> str:
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["day", "subject_a", "subject_b", "body", "linkedin_dm"])
    for r in rows:
        writer.writerow([r["day"], r["subject_a"], r["subject_b"], r["body"], r["linkedin_dm"]])
    return buf.getvalue()


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------

st.set_page_config(page_title=APP_NAME, page_icon="✉️", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@400;600&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', system-ui, sans-serif; }
    .fk-mono, .fk-mono textarea, code, pre { font-family: 'JetBrains Mono', 'Courier New', monospace !important; }
    .fk-tag { color: #9BA8B4; font-size: 0.9rem; margin-top: -0.6rem; }
    .fk-day-badge {
        display: inline-block; background: #F5B942; color: #0B0F14;
        font-weight: 700; padding: 2px 10px; border-radius: 999px;
        font-size: 0.85rem; margin-bottom: 0.4rem;
    }
    .fk-footer { color: #9BA8B4; font-size: 0.85rem; margin-top: 2rem; border-top: 1px solid #263140; padding-top: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title(f"✉️ {APP_NAME}")
st.markdown(f"<div class='fk-tag'>{TAGLINE} — cold email sequence builder, no API key required.</div>", unsafe_allow_html=True)
st.write("")

with st.expander("How this works", expanded=False):
    st.write(
        "Fill in your offer, your ideal customer profile, and one proof point. "
        "ForgeOutreach fills them into 5 pre-built email angles: intro (day 0), "
        "value/proof (day 2), case study (day 4), objection handling (day 7), "
        "and breakup (day 12). Each email ships with two subject lines for A/B "
        "testing and a matching LinkedIn DM. Merge fields like {{first_name}} "
        "and {{company}} are left in place so your sending tool can fill them in. "
        "This tool generates text only — it does not send anything."
    )

col_left, col_right = st.columns([1, 1])

with col_left:
    offer = st.text_area(
        "Your offer — what are you selling?",
        value="A done-for-you cold email sequence generator for freelance developers",
        height=90,
    )
    icp = st.text_area(
        "Ideal customer profile — who are you selling to?",
        value="Freelance web developers who land 1-3 client projects a month and hate writing outreach",
        height=90,
    )
    proof = st.text_area(
        "Proof point — a stat, testimonial, or result",
        value="Beta users landed 3 replies from 40 sends in the first week",
        height=90,
    )

with col_right:
    your_name = st.text_input("Your name (optional — leave blank to keep {{your_name}} as a merge field)")
    your_company = st.text_input("Your company (optional)")

    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")
    ai_available = requests is not None and bool(anthropic_key or openai_key)
    use_ai = False
    if ai_available:
        use_ai = st.checkbox(
            "Polish tone with AI (optional — uses your API key, falls back to the template if it fails)",
            value=False,
        )
    else:
        st.caption(
            "No ANTHROPIC_API_KEY or OPENAI_API_KEY set — running on template logic only. "
            "That's the default and it works fully without one."
        )

    generate = st.button("Generate sequence", type="primary", use_container_width=True)

if generate:
    if not _clean(offer) or not _clean(icp) or not _clean(proof):
        st.error("Fill in offer, ICP, and proof point — all three are required.")
    else:
        rows = generate_sequence(offer, icp, proof, your_name, your_company)
        if use_ai:
            with st.spinner("Polishing with AI..."):
                any_ai = False
                for r in rows:
                    polished, used = ai_polish_body(r["body"], offer, icp, proof)
                    r["body"] = polished
                    any_ai = any_ai or used
                if not any_ai:
                    st.warning("AI polish did not run (no response or no network) — showing the template version instead.")
        st.session_state["fk_rows"] = rows
        st.session_state["fk_inputs"] = (offer, icp, proof)

if "fk_rows" in st.session_state:
    rows = st.session_state["fk_rows"]
    offer_s, icp_s, proof_s = st.session_state["fk_inputs"]

    st.write("")
    st.subheader("Your 5-email sequence")

    for r in rows:
        st.markdown(f"<span class='fk-day-badge'>DAY {r['day']}</span> &nbsp; **{r['angle']}**", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.text_input(f"Subject A — day {r['day']}", value=r["subject_a"], key=f"sa_{r['day']}", disabled=True)
        with c2:
            st.text_input(f"Subject B — day {r['day']}", value=r["subject_b"], key=f"sb_{r['day']}", disabled=True)
        st.text_area(f"Body — day {r['day']}", value=r["body"], height=180, key=f"body_{r['day']}", disabled=True)
        st.text_area(f"LinkedIn DM — day {r['day']}", value=r["linkedin_dm"], height=70, key=f"dm_{r['day']}", disabled=True)
        st.write("")

    st.write("")
    st.subheader("Export")
    txt_out = build_txt(rows, offer_s, icp_s, proof_s)
    csv_out = build_csv(rows)

    ec1, ec2 = st.columns(2)
    with ec1:
        st.download_button(
            "Download .txt (plain sequence)",
            data=txt_out,
            file_name="forgeoutreach_sequence.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with ec2:
        st.download_button(
            "Download .csv (Instantly / Lemlist upload)",
            data=csv_out,
            file_name="forgeoutreach_sequence.csv",
            mime="text/csv",
            use_container_width=True,
        )

st.markdown("<div class='fk-footer'>A ForgeKit product by Orynix Technologies</div>", unsafe_allow_html=True)
