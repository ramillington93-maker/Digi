"""
ForgePitch -- Streamlit UI.

Run with: streamlit run app.py

Paste a job post and your 5-line profile, get a proposal, three subject
lines, three price anchors, and an objection-handling P.S. No API key
needed. If ANTHROPIC_API_KEY or OPENAI_API_KEY is set, an optional
"Polish with AI" step can rewrite the draft -- it falls back to the
template automatically if that call fails.
"""

from __future__ import annotations

import os
from pathlib import Path

import streamlit as st

from core import enhance_with_llm, format_proposal_markdown, generate_proposal

APP_DIR = Path(__file__).parent


def _load_dotenv_if_present() -> None:
    env_path = APP_DIR / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


_load_dotenv_if_present()

st.set_page_config(page_title="ForgePitch", page_icon="📝", layout="wide")

st.title("ForgePitch")
st.caption("Turn a job post into a proposal in 30 seconds. A ForgeKit product by Orynix Technologies.")

has_key = bool(os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("OPENAI_API_KEY"))

sample_dir = APP_DIR / "samples"
sample_jobs = sorted(sample_dir.glob("job_post_*.txt")) if sample_dir.exists() else []

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Job post")
    sample_choice = st.selectbox(
        "Load a sample job post (optional)",
        ["-- none --"] + [f.name for f in sample_jobs],
    )
    default_job = ""
    if sample_choice != "-- none --":
        default_job = (sample_dir / sample_choice).read_text(encoding="utf-8")
    job_text = st.text_area("Paste the job post text", value=default_job, height=320)

with col2:
    st.subheader("2. Your profile")
    st.caption("5 lines: Name, Skills, Experience, Rate, Portfolio link.")
    default_profile = ""
    profile_sample = sample_dir / "sample_profile.txt"
    use_sample_profile = st.checkbox("Use sample profile", value=False)
    if use_sample_profile and profile_sample.exists():
        default_profile = profile_sample.read_text(encoding="utf-8")
    profile_text = st.text_area(
        "Paste your profile",
        value=default_profile,
        height=320,
        placeholder=(
            "Name: Jamie Rivera\n"
            "Skills: Python, Django, REST APIs, PostgreSQL\n"
            "Experience: 5 years building backend APIs for startups\n"
            "Rate: $55/hr\n"
            "Portfolio: jamierivera.dev"
        ),
    )

st.divider()

enhance = st.checkbox(
    f"Polish with AI ({'key found' if has_key else 'no API key set -- will use template mode'})",
    value=has_key,
    disabled=not has_key,
)

generate = st.button("Generate proposal", type="primary")

if generate:
    if not job_text.strip() or not profile_text.strip():
        st.error("Paste both a job post and a profile first.")
    else:
        proposal = generate_proposal(job_text, profile_text)
        markdown = format_proposal_markdown(proposal)

        status = "template"
        if enhance and has_key:
            with st.spinner("Polishing with AI..."):
                markdown, status = enhance_with_llm(markdown, job_text, profile_text)

        st.subheader("Result")
        badge = "AI-polished" if status == "enhanced" else "Template mode (no API key used)"
        st.caption(badge)

        st.markdown(markdown)

        st.download_button(
            "Download as Markdown",
            data=markdown,
            file_name="proposal.md",
            mime="text/markdown",
        )
else:
    st.info("Paste a job post and a profile, then click Generate proposal.")

st.divider()
st.caption("ForgePitch -- Ship today. Cash tomorrow. A ForgeKit product by Orynix Technologies.")
