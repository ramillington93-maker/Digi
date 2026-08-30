"""
ForgeNotes — turn a meeting transcript into a summary, decisions, action
items, and a follow-up email draft. Works with no API key. If
ANTHROPIC_API_KEY or OPENAI_API_KEY is set, it tries to sharpen the
results and falls back to the rule-based output if that call fails.

Run: streamlit run app.py
"""

import os
from datetime import datetime

import streamlit as st

from forgenotes_core import (
    ExtractionResult,
    run_rule_based,
    llm_enhance,
    to_markdown,
    to_docx_style_markdown,
)

st.set_page_config(
    page_title="ForgeNotes",
    page_icon="📝",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Small CSS polish on top of the theme (kept minimal, theme does most of it)
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    .fk-badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 999px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .fk-badge-rule {
        background: rgba(61, 220, 151, 0.15);
        color: #3DDC97;
        border: 1px solid #3DDC97;
    }
    .fk-badge-llm {
        background: rgba(245, 185, 66, 0.15);
        color: #F5B942;
        border: 1px solid #F5B942;
    }
    .fk-footer {
        color: #9BA8B4;
        font-size: 0.8rem;
        margin-top: 3rem;
        border-top: 1px solid #263140;
        padding-top: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("📝 ForgeNotes")
st.caption("Paste a transcript. Get a summary, decisions, and action items. No account needed.")

# ---------------------------------------------------------------------------
# Sidebar: mode + settings
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("Settings")

    has_anthropic = bool(os.environ.get("ANTHROPIC_API_KEY"))
    has_openai = bool(os.environ.get("OPENAI_API_KEY"))
    has_key = has_anthropic or has_openai

    if has_key:
        provider = "Anthropic" if has_anthropic else "OpenAI"
        st.success(f"API key detected ({provider}). LLM-enhanced mode is available.")
        use_llm = st.checkbox("Use LLM to sharpen results", value=True)
    else:
        st.info(
            "No ANTHROPIC_API_KEY or OPENAI_API_KEY found.\n\n"
            "Running in rule-based mode — this still works fully, no key required."
        )
        use_llm = False

    meeting_title = st.text_input("Meeting title (used in exports)", value="Meeting Notes")

    st.divider()
    st.markdown("**How extraction works**")
    st.caption(
        "Rule-based mode scores sentences by keyword frequency for the summary, "
        "and scans for phrases like 'decided', 'agreed', 'I'll', and dates to "
        "pull decisions and action items. No transcript ever leaves your machine "
        "unless you turn on LLM mode with your own key."
    )

    st.divider()
    st.caption("A ForgeKit product by Orynix Technologies.")

# ---------------------------------------------------------------------------
# Input
# ---------------------------------------------------------------------------
tab_upload, tab_paste = st.tabs(["Upload file", "Paste text"])

transcript_text = ""

with tab_upload:
    uploaded = st.file_uploader("Upload a .vtt or .txt transcript", type=["vtt", "txt"])
    if uploaded is not None:
        try:
            transcript_text = uploaded.read().decode("utf-8", errors="ignore")
            st.success(f"Loaded {uploaded.name} ({len(transcript_text)} characters).")
        except Exception as e:
            st.error(f"Could not read that file: {e}")

    st.caption("Don't have a transcript handy? Try the sample:")
    if st.button("Load sample transcript"):
        try:
            with open("sample_transcript.vtt", "r", encoding="utf-8") as f:
                # Set the widget's own key before it's instantiated this run —
                # this is the supported way to populate a text_area programmatically.
                st.session_state["paste_area"] = f.read()
        except FileNotFoundError:
            st.error("sample_transcript.vtt not found in this folder.")

with tab_paste:
    pasted = st.text_area(
        "Paste transcript text",
        height=280,
        key="paste_area",
        placeholder="Priya Nair: Okay, let's start...\nMarcus Chen: It's in review...",
    )
    if pasted:
        transcript_text = pasted

run_clicked = st.button("Generate notes", type="primary", disabled=not transcript_text.strip())

# ---------------------------------------------------------------------------
# Processing
# ---------------------------------------------------------------------------
if run_clicked and transcript_text.strip():
    with st.spinner("Reading transcript..."):
        rule_result = run_rule_based(transcript_text, meeting_title=meeting_title)

    final_result: ExtractionResult = rule_result

    if use_llm:
        with st.spinner("Asking the LLM to sharpen results..."):
            llm_result = llm_enhance(transcript_text)
        if llm_result is not None:
            # Keep participants from rule-based parsing (LLM doesn't get them),
            # everything else from the LLM pass.
            llm_result.participants = rule_result.participants
            final_result = llm_result
        else:
            st.warning(
                "LLM call unavailable or failed — showing rule-based results instead. "
                "Nothing crashed, nothing was lost."
            )

    st.session_state["result"] = final_result
    st.session_state["meeting_title"] = meeting_title

# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------
result: ExtractionResult = st.session_state.get("result")

if result:
    badge_class = "fk-badge-llm" if result.source == "llm" else "fk-badge-rule"
    badge_text = "LLM-enhanced" if result.source == "llm" else "Rule-based (no API key used)"
    st.markdown(f'<span class="fk-badge {badge_class}">{badge_text}</span>', unsafe_allow_html=True)

    if result.participants:
        st.markdown("**Participants:** " + ", ".join(result.participants))

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Executive Summary")
        if result.summary:
            for s in result.summary:
                st.markdown(f"- {s}")
        else:
            st.caption("No summary points detected.")

        st.subheader("Decisions Made")
        if result.decisions:
            for d in result.decisions:
                st.markdown(f"- {d}")
        else:
            st.caption("No explicit decisions detected.")

    with col2:
        st.subheader("Action Items")
        if result.action_items:
            for a in result.action_items:
                st.markdown(f"**{a.owner}** — {a.task}")
                st.caption(f"Due: {a.due}")
        else:
            st.caption("No action items detected.")

    st.subheader("Follow-up Email Draft")
    st.text_area("Email draft (editable, copy from here)", value=result.email_draft, height=280)

    st.divider()
    st.subheader("Export")

    title_for_export = st.session_state.get("meeting_title", "Meeting Notes")
    md_export = to_markdown(result, meeting_title=title_for_export)
    docx_style_export = to_docx_style_markdown(result, meeting_title=title_for_export)
    stamp = datetime.now().strftime("%Y-%m-%d")

    ecol1, ecol2, ecol3 = st.columns(3)
    with ecol1:
        st.download_button(
            "Download notes.md",
            data=md_export,
            file_name=f"forgenotes-{stamp}.md",
            mime="text/markdown",
        )
    with ecol2:
        st.download_button(
            "Download for Word (.md)",
            data=docx_style_export,
            file_name=f"forgenotes-word-{stamp}.md",
            mime="text/markdown",
            help="Plain-text markdown formatted to paste cleanly into Word or Google Docs.",
        )
    with ecol3:
        st.download_button(
            "Download email draft (.txt)",
            data=result.email_draft,
            file_name=f"forgenotes-email-{stamp}.txt",
            mime="text/plain",
        )
else:
    st.info("Upload a transcript, paste one, or load the sample — then click Generate notes.")

st.markdown(
    '<div class="fk-footer">ForgeNotes — A ForgeKit product by Orynix Technologies.</div>',
    unsafe_allow_html=True,
)
