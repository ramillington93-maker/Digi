"""
ForgeCaptions — social caption generator.
Run with: streamlit run app.py

No API key required. Generation is template-based, built on 20 real
caption/hook patterns in samples/styles.json. An optional AI polish
pass runs only if ANTHROPIC_API_KEY or OPENAI_API_KEY is set.
"""

import streamlit as st
from dotenv import load_dotenv

from generator import (
    PLATFORMS,
    TONES,
    available_llm_provider,
    generate,
    llm_polish,
)

load_dotenv()

st.set_page_config(page_title="ForgeCaptions", page_icon="✍️", layout="centered")

st.markdown(
    """
    <style>
    .fk-tag { display:inline-block; background:#141B24; color:#F5B942;
        border-radius:6px; padding:2px 8px; margin:2px; font-family:monospace;
        font-size:0.85em; }
    .fk-footer { color:#9BA8B4; font-size:0.85em; margin-top:2rem;
        border-top:1px solid #1e2833; padding-top:1rem; }
    .fk-item { background:#141B24; border-radius:8px; padding:10px 14px;
        margin-bottom:8px; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("ForgeCaptions")
st.caption("Ship today. Cash tomorrow. — A ForgeKit product by Orynix Technologies")

st.write(
    "Describe what you're selling. Pick a platform and a tone. "
    "Get 10 captions, 10 hooks, 15 hashtags, 3 CTAs, and one first-comment "
    "line, built from real caption patterns — not a blank text box."
)

with st.form("caption_form"):
    product = st.text_area(
        "Product description",
        placeholder="e.g. a 30-day fitness planner PDF for busy parents",
        height=80,
    )
    col1, col2 = st.columns(2)
    with col1:
        platform = st.selectbox("Platform", PLATFORMS)
    with col2:
        tone = st.selectbox("Tone", TONES)

    provider = available_llm_provider()
    use_llm = False
    if provider:
        use_llm = st.checkbox(
            f"AI polish (optional, uses your {provider.upper()} key)",
            value=False,
        )
    else:
        st.caption(
            "No ANTHROPIC_API_KEY or OPENAI_API_KEY set — running template mode only. "
            "That's the default and it works fully on its own."
        )

    submitted = st.form_submit_button("Generate")

if submitted:
    if not product.strip():
        st.error("Add a product description first.")
    else:
        with st.spinner("Generating..."):
            result = generate(product, platform, tone)
            note = None
            if use_llm:
                result, note = llm_polish(result)
        if note:
            st.info(note)

        st.subheader("10 Captions")
        for i, c in enumerate(result["captions"], 1):
            st.markdown(f"<div class='fk-item'><b>{i}.</b> {c}</div>", unsafe_allow_html=True)

        st.subheader("10 Hooks")
        for i, h in enumerate(result["hooks"], 1):
            st.markdown(f"<div class='fk-item'><b>{i}.</b> {h}</div>", unsafe_allow_html=True)

        st.subheader("15 Hashtags")
        st.markdown(
            "".join(f"<span class='fk-tag'>{h}</span>" for h in result["hashtags"]),
            unsafe_allow_html=True,
        )

        st.subheader("3 CTA Variants")
        for i, c in enumerate(result["ctas"], 1):
            st.markdown(f"<div class='fk-item'><b>{i}.</b> {c}</div>", unsafe_allow_html=True)

        st.subheader("First Comment")
        st.markdown(f"<div class='fk-item'>{result['first_comment']}</div>", unsafe_allow_html=True)

        all_text = (
            "CAPTIONS\n" + "\n".join(result["captions"])
            + "\n\nHOOKS\n" + "\n".join(result["hooks"])
            + "\n\nHASHTAGS\n" + " ".join(result["hashtags"])
            + "\n\nCTAS\n" + "\n".join(result["ctas"])
            + "\n\nFIRST COMMENT\n" + result["first_comment"]
        )
        st.download_button("Download as .txt", all_text, file_name="forgecaptions_output.txt")

st.markdown(
    "<div class='fk-footer'>A ForgeKit product by Orynix Technologies</div>",
    unsafe_allow_html=True,
)
