"""
ForgeNotes core logic.

Everything here works with zero API keys. If ANTHROPIC_API_KEY or
OPENAI_API_KEY is set in the environment, `llm_enhance()` will try to
improve the rule-based result. If the key is missing, the library isn't
installed, or the call fails for any reason, it returns None and the
app keeps the rule-based output. Nothing here ever raises out to the
caller and nothing here ever requires a key.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from typing import Optional

# ---------------------------------------------------------------------------
# Stopwords + keyword lists (kept small and readable on purpose)
# ---------------------------------------------------------------------------

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "been", "but", "by", "can",
    "did", "do", "does", "for", "from", "had", "has", "have", "he", "her",
    "him", "his", "i", "if", "in", "is", "it", "its", "just", "let", "me",
    "my", "of", "on", "or", "our", "over", "so", "that", "the", "their",
    "them", "then", "there", "these", "they", "this", "to", "up", "us",
    "was", "we", "were", "will", "with", "you", "your", "yes", "no", "okay",
    "ok", "one", "would", "could", "should", "not", "still", "get", "got",
}

DECISION_KEYWORDS = re.compile(
    r"\b(decided|decide[sd]?|agreed|agree[sd]?|final(?:ize[d]?)?|confirmed|"
    r"resolved|we will not|not going to)\b",
    re.IGNORECASE,
)

ACTION_KEYWORDS = re.compile(
    r"\b(i'll|i will|will (?:own|send|have|file|finalize|update|ping|configure|"
    r"compile|do|handle|prepare|share|follow up|schedule|draft)|"
    r"can you (?:own|do|handle|send|file|update)|action item|to-?do|"
    r"i'll own|own the|owns? the)\b",
    re.IGNORECASE,
)

MONTHS = (
    r"Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|"
    r"Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|"
    r"Nov(?:ember)?|Dec(?:ember)?"
)
WEEKDAYS = (
    r"Mon(?:day)?|Tue(?:s(?:day)?)?|Wed(?:nes(?:day)?)?|Thu(?:rs(?:day)?)?|"
    r"Fri(?:day)?|Sat(?:ur(?:day)?)?|Sun(?:day)?"
)

DATE_REGEX = re.compile(
    rf"\b(?:(?:next|this|by)\s+)?(?:{WEEKDAYS})(?:,?\s*(?:{MONTHS})\.?\s+\d{{1,2}}(?:st|nd|rd|th)?)?\b"
    rf"|\b(?:{MONTHS})\.?\s+\d{{1,2}}(?:st|nd|rd|th)?\b"
    rf"|\btoday\b|\btomorrow\b|\bend of (?:day|week|month)\b|\bEOD\b|\bEOW\b|\bQ[1-4]\b",
    re.IGNORECASE,
)

SPEAKER_LINE = re.compile(r"^\s*([A-Z][A-Za-z .'\-]{1,40}):\s*(.+)$")
SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"'])")
NAME_TOKEN = re.compile(r"\b([A-Z][a-z]+)\b")


@dataclass
class ActionItem:
    owner: str
    task: str
    due: str


@dataclass
class ExtractionResult:
    participants: list[str] = field(default_factory=list)
    summary: list[str] = field(default_factory=list)
    decisions: list[str] = field(default_factory=list)
    action_items: list[ActionItem] = field(default_factory=list)
    email_draft: str = ""
    source: str = "rule-based"


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def _strip_vtt(text: str) -> str:
    """Strip WEBVTT header, cue indexes, and timestamp lines, keep cue text."""
    lines = text.splitlines()
    kept = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            kept.append("")
            continue
        if stripped.upper().startswith("WEBVTT"):
            continue
        if re.match(r"^\d+$", stripped):
            continue
        if "-->" in stripped:
            continue
        if re.match(r"^NOTE\b", stripped, re.IGNORECASE):
            continue
        kept.append(line)
    return "\n".join(kept)


def parse_transcript(raw_text: str) -> list[tuple[str, str]]:
    """
    Returns a list of (speaker, utterance_text) pairs. `speaker` is
    "Unknown" when no "Name: text" pattern is found on a line.
    Works for .vtt (WEBVTT cue format) and plain .txt transcripts.
    """
    text = raw_text.strip()
    if not text:
        return []

    if text.upper().startswith("WEBVTT"):
        text = _strip_vtt(text)

    utterances: list[tuple[str, str]] = []
    last_speaker = "Unknown"
    buffer_speaker = None
    buffer_lines: list[str] = []

    def flush():
        nonlocal buffer_speaker, buffer_lines
        if buffer_lines:
            combined = " ".join(l.strip() for l in buffer_lines if l.strip())
            if combined:
                utterances.append((buffer_speaker or "Unknown", combined))
        buffer_speaker = None
        buffer_lines = []

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            flush()
            continue
        m = SPEAKER_LINE.match(line)
        if m:
            flush()
            speaker, rest = m.group(1).strip(), m.group(2).strip()
            last_speaker = speaker
            buffer_speaker = speaker
            buffer_lines = [rest]
        else:
            if buffer_speaker is None:
                buffer_speaker = last_speaker
            buffer_lines.append(line)
    flush()

    return utterances


def _sentences_with_speakers(utterances: list[tuple[str, str]]) -> list[tuple[str, str]]:
    out = []
    for speaker, text in utterances:
        for sent in SENTENCE_SPLIT.split(text):
            sent = sent.strip()
            if sent:
                out.append((speaker, sent))
    return out


def get_participants(utterances: list[tuple[str, str]]) -> list[str]:
    seen = []
    for speaker, _ in utterances:
        if speaker != "Unknown" and speaker not in seen:
            seen.append(speaker)
    return seen


# ---------------------------------------------------------------------------
# Summary (extractive, word-frequency scoring)
# ---------------------------------------------------------------------------

def _tokenize(text: str) -> list[str]:
    return [w.lower() for w in re.findall(r"[A-Za-z']+", text) if len(w) > 1]


def build_summary(sentence_pairs: list[tuple[str, str]], max_sentences: int = 5) -> list[str]:
    if not sentence_pairs:
        return []

    freq: dict[str, int] = {}
    for _, sent in sentence_pairs:
        for tok in _tokenize(sent):
            if tok not in STOPWORDS:
                freq[tok] = freq.get(tok, 0) + 1

    if not freq:
        return [s for _, s in sentence_pairs[:max_sentences]]

    max_freq = max(freq.values())
    scored = []
    for idx, (speaker, sent) in enumerate(sentence_pairs):
        toks = [t for t in _tokenize(sent) if t not in STOPWORDS]
        if not toks:
            continue
        score = sum(freq.get(t, 0) / max_freq for t in toks) / len(toks)
        # small bump for sentences that carry a decision or action signal
        if DECISION_KEYWORDS.search(sent) or ACTION_KEYWORDS.search(sent):
            score *= 1.25
        # skip very short filler sentences ("Bye everyone.")
        if len(toks) < 3:
            score *= 0.3
        scored.append((score, idx, speaker, sent))

    top = sorted(scored, key=lambda x: x[0], reverse=True)[:max_sentences]
    top_sorted_by_order = sorted(top, key=lambda x: x[1])
    return [f"{sent}" for _, _, _, sent in top_sorted_by_order]


# ---------------------------------------------------------------------------
# Decisions
# ---------------------------------------------------------------------------

def extract_decisions(sentence_pairs: list[tuple[str, str]]) -> list[str]:
    decisions = []
    for _, sent in sentence_pairs:
        cleaned = sent.strip()
        if cleaned.endswith("?"):
            continue  # questions aren't decisions, even if they contain "final"/"decide"
        if DECISION_KEYWORDS.search(sent):
            if cleaned not in decisions:
                decisions.append(cleaned)
    return decisions


# ---------------------------------------------------------------------------
# Action items
# ---------------------------------------------------------------------------

def _find_owner(sent: str, speaker: str, known_names: list[str]) -> str:
    first_person = re.search(r"\bi'?ll\b|\bi will\b", sent, re.IGNORECASE)
    # If someone is directly addressed ("Marcus, can you own...") prefer that name.
    for name in known_names:
        first = name.split()[0]
        if re.search(rf"\b{re.escape(first)}\b\s*,", sent) or re.search(
            rf"\b{re.escape(first)}\s+can you\b", sent, re.IGNORECASE
        ):
            return name
    if first_person:
        return speaker
    # Fall back to any known name mentioned in the sentence.
    for name in known_names:
        first = name.split()[0]
        if re.search(rf"\b{re.escape(first)}\b", sent):
            return name
    if speaker != "Unknown":
        return speaker
    # No speaker labels at all (plain pasted text) — look for "Name will ..." patterns.
    name_will = re.search(r"\b([A-Z][a-z]+)\s+will\b", sent)
    if name_will:
        return name_will.group(1)
    return "Unassigned"


def extract_action_items(
    sentence_pairs: list[tuple[str, str]], known_names: list[str]
) -> list[ActionItem]:
    items: list[ActionItem] = []
    seen_tasks = set()
    for speaker, sent in sentence_pairs:
        cleaned_sent = sent.strip()
        if cleaned_sent.endswith("?"):
            continue  # a question assigning work reads oddly as a task; the commitment reply catches it
        if not ACTION_KEYWORDS.search(sent):
            continue
        due_match = DATE_REGEX.search(sent)
        due = due_match.group(0).strip().rstrip(",") if due_match else "No date given"
        owner = _find_owner(sent, speaker, known_names)
        task = sent.strip()
        key = (owner, task.lower())
        if key in seen_tasks:
            continue
        seen_tasks.add(key)
        items.append(ActionItem(owner=owner, task=task, due=due))
    return items


# ---------------------------------------------------------------------------
# Follow-up email
# ---------------------------------------------------------------------------

def build_email_draft(
    participants: list[str],
    summary: list[str],
    decisions: list[str],
    action_items: list[ActionItem],
    meeting_title: str = "Meeting Follow-up",
) -> str:
    lines = []
    lines.append(f"Subject: {meeting_title} — Notes & Action Items")
    lines.append("")
    lines.append("Hi all,")
    lines.append("")
    lines.append("Thanks for joining. Here's a recap and the next steps.")
    lines.append("")
    if summary:
        lines.append("Summary:")
        for s in summary:
            lines.append(f"- {s}")
        lines.append("")
    if decisions:
        lines.append("Decisions:")
        for d in decisions:
            lines.append(f"- {d}")
        lines.append("")
    if action_items:
        lines.append("Action Items:")
        for a in action_items:
            lines.append(f"- {a.owner}: {a.task} (Due: {a.due})")
        lines.append("")
    lines.append("Reply here if I got anything wrong or missed something.")
    lines.append("")
    lines.append("Best,")
    if participants:
        lines.append(participants[0])
    else:
        lines.append("[Your name]")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Full pipeline (rule-based, always works, never raises)
# ---------------------------------------------------------------------------

def run_rule_based(raw_text: str, meeting_title: str = "Meeting Follow-up") -> ExtractionResult:
    utterances = parse_transcript(raw_text)
    participants = get_participants(utterances)
    sentence_pairs = _sentences_with_speakers(utterances)

    summary = build_summary(sentence_pairs, max_sentences=5)
    decisions = extract_decisions(sentence_pairs)
    action_items = extract_action_items(sentence_pairs, participants)
    email = build_email_draft(participants, summary, decisions, action_items, meeting_title)

    return ExtractionResult(
        participants=participants,
        summary=summary,
        decisions=decisions,
        action_items=action_items,
        email_draft=email,
        source="rule-based",
    )


# ---------------------------------------------------------------------------
# Optional LLM enhancement — isolated, best-effort, never required
# ---------------------------------------------------------------------------

_LLM_PROMPT_TEMPLATE = """You are helping tidy up meeting notes extracted from a raw transcript.
Return ONLY valid JSON (no markdown fences, no commentary) matching this shape:

{{
  "summary": ["3 to 5 short sentences, the executive summary"],
  "decisions": ["short sentence per decision made"],
  "action_items": [{{"owner": "name", "task": "short task description", "due": "date or 'No date given'"}}],
  "email_draft": "a complete follow-up email as plain text, including a Subject: line"
}}

Base your answer only on this transcript. Do not invent names, dates, or decisions
that are not supported by the text.

TRANSCRIPT:
{transcript}
"""


def _parse_llm_json(text: str) -> Optional[dict]:
    text = text.strip()
    # Strip markdown fences if the model added them anyway.
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
        text = re.sub(r"```\s*$", "", text)
    try:
        return json.loads(text)
    except Exception:
        # Try to salvage the first {...} block.
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except Exception:
                return None
        return None


def _try_anthropic(transcript: str) -> Optional[dict]:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return None
    try:
        import anthropic  # type: ignore

        client = anthropic.Anthropic(api_key=api_key)
        resp = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=1200,
            messages=[
                {
                    "role": "user",
                    "content": _LLM_PROMPT_TEMPLATE.format(transcript=transcript[:12000]),
                }
            ],
        )
        text = "".join(
            block.text for block in resp.content if getattr(block, "type", "") == "text"
        )
        return _parse_llm_json(text)
    except Exception:
        return None


def _try_openai(transcript: str) -> Optional[dict]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None
    try:
        import openai  # type: ignore

        client = openai.OpenAI(api_key=api_key)
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": _LLM_PROMPT_TEMPLATE.format(transcript=transcript[:12000]),
                }
            ],
            temperature=0.2,
        )
        text = resp.choices[0].message.content or ""
        return _parse_llm_json(text)
    except Exception:
        return None


def llm_enhance(raw_text: str) -> Optional[ExtractionResult]:
    """
    Best-effort LLM pass. Returns None if no key is set, the SDK isn't
    installed, the call fails, or the response can't be parsed as the
    expected JSON shape. Callers should always have a rule-based result
    ready to fall back to.
    """
    parsed = _try_anthropic(raw_text) or _try_openai(raw_text)
    if not parsed:
        return None
    try:
        action_items = [
            ActionItem(
                owner=str(a.get("owner", "Unassigned")),
                task=str(a.get("task", "")),
                due=str(a.get("due", "No date given")),
            )
            for a in parsed.get("action_items", [])
            if a.get("task")
        ]
        return ExtractionResult(
            participants=[],
            summary=[str(s) for s in parsed.get("summary", [])],
            decisions=[str(d) for d in parsed.get("decisions", [])],
            action_items=action_items,
            email_draft=str(parsed.get("email_draft", "")),
            source="llm",
        )
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Markdown exports
# ---------------------------------------------------------------------------

def to_markdown(result: ExtractionResult, meeting_title: str = "Meeting Notes") -> str:
    lines = [f"# {meeting_title}", ""]
    if result.participants:
        lines.append("**Participants:** " + ", ".join(result.participants))
        lines.append("")
    lines.append("## Executive Summary")
    lines.append("")
    if result.summary:
        for s in result.summary:
            lines.append(f"- {s}")
    else:
        lines.append("_No summary points detected._")
    lines.append("")
    lines.append("## Decisions Made")
    lines.append("")
    if result.decisions:
        for d in result.decisions:
            lines.append(f"- {d}")
    else:
        lines.append("_No explicit decisions detected._")
    lines.append("")
    lines.append("## Action Items")
    lines.append("")
    if result.action_items:
        lines.append("| Owner | Task | Due |")
        lines.append("|---|---|---|")
        for a in result.action_items:
            task = a.task.replace("|", "/")
            lines.append(f"| {a.owner} | {task} | {a.due} |")
    else:
        lines.append("_No action items detected._")
    lines.append("")
    lines.append("## Follow-up Email Draft")
    lines.append("")
    lines.append("```")
    lines.append(result.email_draft)
    lines.append("```")
    lines.append("")
    lines.append(f"_Generated by ForgeNotes ({result.source} mode). A ForgeKit product by Orynix Technologies._")
    return "\n".join(lines)


def to_docx_style_markdown(result: ExtractionResult, meeting_title: str = "Meeting Notes") -> str:
    """
    A markdown flavor formatted to paste cleanly into Word: headings use
    Title Case, bullets use plain dashes, and the table is spaced for
    Word's markdown paste behavior. Word (and Google Docs) will render
    the #/##  headings and bullets as real formatting on paste.
    """
    lines = [f"# {meeting_title}", ""]
    if result.participants:
        lines.append("Participants: " + ", ".join(result.participants))
        lines.append("")
    lines.append("## Executive Summary")
    lines.append("")
    for s in result.summary or ["No summary points detected."]:
        lines.append(f"-  {s}")
    lines.append("")
    lines.append("## Decisions Made")
    lines.append("")
    for d in result.decisions or ["No explicit decisions detected."]:
        lines.append(f"-  {d}")
    lines.append("")
    lines.append("## Action Items")
    lines.append("")
    if result.action_items:
        for a in result.action_items:
            lines.append(f"-  {a.owner} — {a.task} — Due: {a.due}")
    else:
        lines.append("-  No action items detected.")
    lines.append("")
    lines.append("## Follow-up Email Draft")
    lines.append("")
    for line in result.email_draft.splitlines():
        lines.append(line if line.strip() else "")
    lines.append("")
    lines.append("A ForgeKit product by Orynix Technologies.")
    return "\n".join(lines)
