"""
ForgePitch core logic.

Parses a pasted job post + a 5-line freelancer profile, extracts real
signals (skills mentioned, budget hints, tone, niche), and fills a
proposal template with those signals. This is "mock mode" -- it needs
no API key and never returns a fixed string; every output changes with
the input text.

If ANTHROPIC_API_KEY or OPENAI_API_KEY is set, `enhance_with_llm()` can
rewrite the template output for better prose. That call is isolated and
wrapped in try/except -- any failure (missing key, network error, bad
SDK) falls back to the template output untouched.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Reference data used to read the job post
# ---------------------------------------------------------------------------

NICHE_KEYWORDS = {
    "web development": [
        "python", "javascript", "typescript", "react", "vue", "node",
        "node.js", "html", "css", "wordpress", "php", "api", "django",
        "flask", "shopify", "website", "web app", "webapp", "backend",
        "frontend", "full stack", "full-stack", "developer", "bug fix",
        "database", "sql", "rest api", "next.js", "app",
    ],
    "content writing": [
        "blog", "article", "content", "copywriting", "copywriter",
        "seo writing", "ghostwriting", "ghostwriter", "editor",
        "proofread", "write", "writer", "newsletter", "case study",
        "landing page copy", "email copy", "script writing",
    ],
    "data & admin support": [
        "data entry", "excel", "spreadsheet", "virtual assistant",
        "admin", "administrative", "crm", "research", "transcription",
        "scheduling", "data cleaning", "google sheets", "lead list",
        "data scraping", "bookkeeping", "calendar management",
    ],
    "design": [
        "figma", "ui/ux", "ui design", "ux design", "logo", "branding",
        "graphic design", "illustrator", "photoshop", "mockup",
        "wireframe", "canva",
    ],
    "marketing": [
        "seo", "social media", "email marketing", "ads", "google ads",
        "facebook ads", "marketing campaign", "growth", "analytics",
        "conversion rate",
    ],
}

# Flat skill vocabulary used to find concrete terms to quote back at the
# client (superset of the niche lists, de-duplicated at import time).
ALL_SKILL_TERMS = sorted({term for terms in NICHE_KEYWORDS.values() for term in terms})

URGENT_WORDS = [
    "asap", "urgent", "immediately", "right away", "quick turnaround",
    "tight deadline", "start today", "start now", "fast",
]
CASUAL_WORDS = ["hey", "hi there", "looking for someone chill", "no fluff", "keep it simple"]
FORMAL_WORDS = [
    "we require", "candidate", "applicant", "the successful", "shall",
    "pursuant", "deliverables", "scope of work", "our organization",
    "company", "corporation",
]

BUDGET_RANGE_RE = re.compile(
    r"\$\s?(\d[\d,]*(?:\.\d+)?)\s*(?:-|to|–|—)\s*\$?\s?(\d[\d,]*(?:\.\d+)?)"
)
BUDGET_SINGLE_RE = re.compile(r"\$\s?(\d[\d,]*(?:\.\d+)?)")
HOURLY_RE = re.compile(r"(\d[\d,]*(?:\.\d+)?)\s*(?:/|per)\s*(?:hr|hour)", re.IGNORECASE)


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class Profile:
    name: str = "Freelancer"
    skills: str = ""
    experience: str = ""
    rate: str = ""
    portfolio: str = ""


@dataclass
class JobSignals:
    raw_text: str
    title_guess: str = ""
    niche: str = "general freelance work"
    matched_skills: list[str] = field(default_factory=list)
    budget_hint: str = ""
    budget_low: float | None = None
    budget_high: float | None = None
    tone: str = "neutral"
    hook_sentence: str = ""


# ---------------------------------------------------------------------------
# Profile parsing
# ---------------------------------------------------------------------------

def parse_profile(text: str) -> Profile:
    """Parse a 5-line profile. Accepts `Label: value` lines in any order,
    or five bare lines in the order name/skills/experience/rate/portfolio."""
    lines = [ln.strip() for ln in text.strip().splitlines() if ln.strip()]
    profile = Profile()

    labeled = {}
    for ln in lines:
        m = re.match(r"^(name|skills?|experience|rate|portfolio|link)\s*:\s*(.+)$", ln, re.IGNORECASE)
        if m:
            key, val = m.group(1).lower(), m.group(2).strip()
            labeled[key] = val

    if labeled:
        profile.name = labeled.get("name", profile.name)
        profile.skills = labeled.get("skill", labeled.get("skills", ""))
        profile.experience = labeled.get("experience", "")
        profile.rate = labeled.get("rate", "")
        profile.portfolio = labeled.get("portfolio", labeled.get("link", ""))
    else:
        # Fall back to positional lines.
        fields = ["name", "skills", "experience", "rate", "portfolio"]
        for i, val in enumerate(lines[:5]):
            setattr(profile, fields[i], val)

    profile.name = profile.name or "Freelancer"
    return profile


# ---------------------------------------------------------------------------
# Job post parsing / signal extraction
# ---------------------------------------------------------------------------

def _detect_niche(text_lower: str) -> tuple[str, list[str]]:
    best_niche = "general freelance work"
    best_score = 0
    best_matches: list[str] = []
    for niche, terms in NICHE_KEYWORDS.items():
        matches = [t for t in terms if t in text_lower]
        if len(matches) > best_score:
            best_score = len(matches)
            best_niche = niche
            best_matches = matches
    return best_niche, best_matches


def _detect_budget(text: str) -> tuple[str, float | None, float | None]:
    range_m = BUDGET_RANGE_RE.search(text)
    if range_m:
        low = float(range_m.group(1).replace(",", ""))
        high = float(range_m.group(2).replace(",", ""))
        return f"${range_m.group(1)}-${range_m.group(2)}", low, high

    hourly_m = HOURLY_RE.search(text)
    if hourly_m:
        val = float(hourly_m.group(1).replace(",", ""))
        return f"${hourly_m.group(1)}/hr", val, val

    single_m = BUDGET_SINGLE_RE.search(text)
    if single_m:
        val = float(single_m.group(1).replace(",", ""))
        return f"${single_m.group(1)}", val, val

    return "", None, None


def _detect_tone(text_lower: str) -> str:
    urgent_hits = sum(1 for w in URGENT_WORDS if w in text_lower)
    formal_hits = sum(1 for w in FORMAL_WORDS if w in text_lower)
    casual_hits = sum(1 for w in CASUAL_WORDS if w in text_lower)
    exclamations = text_lower.count("!")

    if urgent_hits >= 1:
        return "urgent"
    if formal_hits >= 2:
        return "formal"
    if casual_hits >= 1 or exclamations >= 2:
        return "casual"
    return "neutral"


def _guess_title(text: str) -> str:
    for line in text.strip().splitlines():
        line = line.strip()
        if line:
            # Strip a leading "Title:" style label if present.
            line = re.sub(r"^(job\s*title|title|project)\s*:\s*", "", line, flags=re.IGNORECASE)
            return line[:90]
    return "your project"


def _hook_sentence(text: str) -> str:
    """Grab the first substantial sentence to reference specifically."""
    body = re.sub(r"\s+", " ", text).strip()
    sentences = re.split(r"(?<=[.!?])\s+", body)
    for s in sentences:
        s = s.strip()
        if len(s) >= 25:
            return s[:220]
    return body[:160]


def analyze_job_post(text: str) -> JobSignals:
    text = text or ""
    text_lower = text.lower()
    niche, matches = _detect_niche(text_lower)
    budget_hint, low, high = _detect_budget(text)
    tone = _detect_tone(text_lower)

    return JobSignals(
        raw_text=text,
        title_guess=_guess_title(text),
        niche=niche,
        matched_skills=matches,
        budget_hint=budget_hint,
        budget_low=low,
        budget_high=high,
        tone=tone,
        hook_sentence=_hook_sentence(text),
    )


# ---------------------------------------------------------------------------
# Proposal generation (template / heuristic "mock mode")
# ---------------------------------------------------------------------------

def _skills_list(profile: Profile) -> list[str]:
    return [s.strip() for s in re.split(r"[,/]| and ", profile.skills) if s.strip()]


def _shared_skills(job: JobSignals, profile: Profile) -> list[str]:
    prof_skills_lower = [s.lower() for s in _skills_list(profile)]
    shared = []
    for term in job.matched_skills:
        for ps in prof_skills_lower:
            if term in ps or ps in term:
                shared.append(term)
                break
    # De-dupe, preserve order.
    seen = set()
    out = []
    for s in shared:
        if s not in seen:
            seen.add(s)
            out.append(s)
    return out or job.matched_skills[:3]


def _rate_number(profile: Profile) -> float | None:
    m = re.search(r"(\d[\d,]*(?:\.\d+)?)", profile.rate or "")
    if m:
        return float(m.group(1).replace(",", ""))
    return None


def _short_title(job: JobSignals, max_len: int) -> str:
    title = job.title_guess.strip()
    if len(title) <= max_len:
        return title
    return title[: max_len - 1].rsplit(" ", 1)[0] + "..."


def build_subject_lines(job: JobSignals, profile: Profile) -> list[str]:
    first_name = profile.name.split()[0] if profile.name else "Quick"
    lines = [
        f"Re: {_short_title(job, 45)} -- a quick fit check",
        f"{first_name}'s note on your {job.niche} post",
        f"Proposal: {_short_title(job, 40)} (with samples)",
    ]
    return lines


def build_price_anchors(job: JobSignals, profile: Profile) -> list[dict]:
    rate = _rate_number(profile)

    if job.budget_low is not None and job.budget_high is not None and job.budget_low != job.budget_high:
        span = job.budget_high - job.budget_low
        low = job.budget_low + span * 0.15
        mid = job.budget_low + span * 0.5
        high = job.budget_high - span * 0.05
    elif job.budget_low is not None:
        base = job.budget_low
        low, mid, high = base * 0.85, base, base * 1.25
    elif rate is not None:
        # No budget on the post -- anchor off the freelancer's own rate,
        # framed as a small package (roughly a 10-15 hour first phase).
        low, mid, high = rate * 8, rate * 12, rate * 20
    else:
        low, mid, high = 250.0, 500.0, 900.0

    def money(v: float) -> str:
        return f"${v:,.0f}"

    return [
        {
            "label": "Low anchor",
            "price": money(low),
            "note": "Fixed scope, single deliverable, no revisions beyond one round. Good if budget is the objection.",
        },
        {
            "label": "Mid anchor (recommended)",
            "price": money(mid),
            "note": "Full scope as posted, two revision rounds, async check-ins. Default offer -- lead with this one.",
        },
        {
            "label": "Premium anchor",
            "price": money(high),
            "note": "Full scope plus a fast turnaround or an extra deliverable (e.g. source files, a short handoff call).",
        },
    ]


def build_ps_line(job: JobSignals, profile: Profile) -> str:
    if job.tone == "urgent":
        return (
            f"P.S. -- I know timeline is the pressure point here. I can start within "
            f"24 hours of getting the go-ahead, so the clock isn't the risk."
        )
    if job.budget_low is not None or job.budget_hint:
        return (
            f"P.S. -- If {job.budget_hint or 'the budget'} is tight, tell me the number and I'll "
            f"scope the low-anchor version above so it fits. No hard feelings either way."
        )
    return (
        "P.S. -- If price is the hold-up, the low anchor above covers the core deliverable "
        "with no extras. We can always add scope later once you've seen the work."
    )


def _opening_hook(job: JobSignals, profile: Profile, shared: list[str]) -> str:
    skill_phrase = shared[0] if shared else job.niche
    first_name = profile.name.split()[0] if profile.name else None
    lane_owner = f"{first_name}'s" if first_name else "my"
    return (
        f'You wrote: "{job.hook_sentence}" -- that\'s squarely {lane_owner} '
        f"lane. I work in {skill_phrase} day to day, and this reads like a project I could start on "
        f"this week, not next month."
    )


def _relevant_experience(profile: Profile, job: JobSignals, shared: list[str]) -> str:
    exp = profile.experience or "several years doing this kind of work"
    skills_text = ", ".join(shared[:4]) if shared else (profile.skills or "the core skills this needs")
    return (
        f"{profile.experience and exp or exp}. Recent work covers {skills_text}, which lines up with "
        f"what you listed in the post ({job.niche})."
    )


def _approach(job: JobSignals, profile: Profile) -> str:
    if job.niche == "web development":
        steps = [
            "Confirm scope and any existing code, repo, or hosting access.",
            "Build in short milestones so you can review progress, not just a final drop.",
            "Test against the cases you care about before calling it done.",
        ]
    elif job.niche == "content writing":
        steps = [
            "Send a 1-paragraph outline first so we agree on angle before I write.",
            "Draft the full piece, matched to the tone in your post.",
            "One revision round included, turned around within 48 hours.",
        ]
    elif job.niche == "data & admin support":
        steps = [
            "Confirm the exact fields, format, and source for the data.",
            "Process in a batch you can spot-check before I run the rest.",
            "Deliver in the file format you actually use (sheet, CSV, or CRM import).",
        ]
    else:
        steps = [
            "Confirm scope and deliverable format in a short kickoff message.",
            "Work in checkpoints so you see progress, not a single end-of-project drop.",
            "Deliver, then one revision round to close any gaps.",
        ]
    return "\n".join(f"{i+1}. {s}" for i, s in enumerate(steps))


def _call_to_action(job: JobSignals, profile: Profile) -> str:
    if job.tone == "urgent":
        return "Reply and I can start today -- no need to wait on a formal kickoff call."
    return "Reply with a yes and I'll send a short kickoff message with next steps -- no call required unless you want one."


@dataclass
class Proposal:
    subject_lines: list[str]
    body: str
    price_anchors: list[dict]
    ps_line: str
    signals: JobSignals
    profile: Profile


def generate_proposal(job_text: str, profile_text: str) -> Proposal:
    job = analyze_job_post(job_text)
    profile = parse_profile(profile_text)
    shared = _shared_skills(job, profile)

    hook = _opening_hook(job, profile, shared)
    experience = _relevant_experience(profile, job, shared)
    approach = _approach(job, profile)
    cta = _call_to_action(job, profile)

    body = (
        f"{hook}\n\n"
        f"{experience}\n\n"
        f"How I'd approach it:\n{approach}\n\n"
        f"{cta}\n\n"
        f"-- {profile.name}"
        + (f"\n{profile.portfolio}" if profile.portfolio else "")
        + (f"\n{profile.rate}" if profile.rate else "")
    )

    subject_lines = build_subject_lines(job, profile)
    price_anchors = build_price_anchors(job, profile)
    ps_line = build_ps_line(job, profile)

    return Proposal(
        subject_lines=subject_lines,
        body=body,
        price_anchors=price_anchors,
        ps_line=ps_line,
        signals=job,
        profile=profile,
    )


def format_proposal_markdown(p: Proposal) -> str:
    lines = []
    lines.append(f"# Proposal for: {p.signals.title_guess}")
    lines.append("")
    lines.append(f"Detected niche: **{p.signals.niche}**  ")
    lines.append(f"Detected tone: **{p.signals.tone}**  ")
    if p.signals.budget_hint:
        lines.append(f"Budget hint found in post: **{p.signals.budget_hint}**  ")
    lines.append("")
    lines.append("## Subject line options")
    for i, s in enumerate(p.subject_lines, 1):
        lines.append(f"{i}. {s}")
    lines.append("")
    lines.append("## Proposal body")
    lines.append("")
    lines.append(p.body)
    lines.append("")
    lines.append("## Price anchors")
    for a in p.price_anchors:
        lines.append(f"- **{a['label']}: {a['price']}** -- {a['note']}")
    lines.append("")
    lines.append("## Objection-handling P.S.")
    lines.append(p.ps_line)
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Optional LLM polish -- isolated, degrades to the template output on
# any failure. No API key required for the product to work.
# ---------------------------------------------------------------------------

def enhance_with_llm(markdown_text: str, job_text: str, profile_text: str) -> tuple[str, str]:
    """Try to polish the template output with an LLM if a key is present.

    Returns (text, status) where status is one of:
      "template"  -- no key set, or the call failed; `text` is unchanged.
      "enhanced"  -- the call succeeded; `text` is the model's rewrite.
    Never raises -- every failure path falls back to the original text.
    """
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")

    if not anthropic_key and not openai_key:
        return markdown_text, "template"

    prompt = (
        "Tighten and polish this freelance proposal draft. Keep every section "
        "(subject lines, proposal body, price anchors, P.S.), keep it concrete "
        "and specific to the job post below, do not add hype words, and keep "
        "roughly the same length.\n\n"
        f"JOB POST:\n{job_text}\n\nFREELANCER PROFILE:\n{profile_text}\n\n"
        f"DRAFT:\n{markdown_text}"
    )

    try:
        if anthropic_key:
            import anthropic  # type: ignore

            client = anthropic.Anthropic(api_key=anthropic_key)
            resp = client.messages.create(
                model="claude-3-5-haiku-latest",
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}],
            )
            text = "".join(
                block.text for block in resp.content if getattr(block, "type", "") == "text"
            ).strip()
            if text:
                return text, "enhanced"

        elif openai_key:
            from openai import OpenAI  # type: ignore

            client = OpenAI(api_key=openai_key)
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1500,
            )
            text = (resp.choices[0].message.content or "").strip()
            if text:
                return text, "enhanced"

    except Exception:
        # Any SDK/network/auth error -- silently degrade to the template.
        return markdown_text, "template"

    return markdown_text, "template"
