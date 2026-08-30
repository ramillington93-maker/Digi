"""
ForgeCaptions generator engine.

Template-based caption generation. No API key needed for any of this.
Everything below draws on samples/styles.json — 20 real caption/hook
patterns spanning X, Instagram, LinkedIn, and TikTok across four tones
(bold, friendly, professional, funny). Product description, platform,
and tone are slot-filled into those patterns, not generated from
scratch by a model.

An optional LLM polish pass lives in llm_polish() below. It only runs
if ANTHROPIC_API_KEY or OPENAI_API_KEY is set, and any failure falls
back to the template output untouched.
"""

from __future__ import annotations

import hashlib
import json
import os
import random
import re
from pathlib import Path

PLATFORMS = ["X", "Instagram", "LinkedIn", "TikTok"]
TONES = ["bold", "friendly", "professional", "funny"]

STYLES_PATH = Path(__file__).parent / "samples" / "styles.json"

STOPWORDS = {
    "a", "an", "the", "for", "of", "to", "with", "and", "or", "your",
    "my", "our", "that", "this", "is", "are", "on", "in", "at",
}

# Word banks: the vocabulary the engine pulls from to fill {benefit},
# {pain}, {audience}, {emoji} slots inside each matched style pattern.
BENEFIT_BANK = {
    "bold": ["results, not excuses", "a real win this week", "proof it works", "your time back, no negotiation"],
    "friendly": ["one less thing to worry about", "a little breathing room", "something that actually helps", "a calmer week"],
    "professional": ["a measurable improvement", "a repeatable process", "consistent output", "a documented workflow"],
    "funny": ["less crying, more shipping", "a small miracle, honestly", "your sanity, mostly intact", "one fewer 2am panic session"],
}
PAIN_BANK = {
    "bold": ["doing this the slow way", "guessing and hoping", "wasting hours on busywork", "reinventing the wheel every week"],
    "friendly": ["staring at a blank page", "putting this off", "juggling too many tabs", "starting from scratch every time"],
    "professional": ["the manual back-and-forth", "the repetitive setup work", "inconsistent output across the team", "the process nobody documented"],
    "funny": ["procrastinating in the group chat", "rewriting the same thing five times", "pretending you have a system", "Googling this at midnight again"],
}
AUDIENCE_BANK = {
    "bold": ["people who ship", "founders who don't wait around", "small teams moving fast"],
    "friendly": ["small business owners", "solo founders", "busy creators"],
    "professional": ["operations teams", "small business owners", "growing teams"],
    "funny": ["tired founders", "people who Google everything at 1am", "small business owners running on coffee"],
}
EMOJI_BANK = {
    "bold": ["\U0001F525", "⚡", "\U0001F4AA"],
    "friendly": ["✨", "\U0001F44B", "\U0001F60A"],
    "professional": [""],
    "funny": ["\U0001F62D", "\U0001F480", "\U0001F91F"],
}
PLATFORM_ALLOWS_EMOJI = {"X": False, "Instagram": True, "LinkedIn": False, "TikTok": True}

GENERIC_HASHTAGS = {
    "X": ["#BuildInPublic", "#IndieHacker", "#SmallBiz", "#SideHustle"],
    "Instagram": ["#SmallBusinessOwner", "#ContentCreator", "#EntrepreneurLife", "#ShopSmall"],
    "LinkedIn": ["#Productivity", "#SmallBusiness", "#Entrepreneurship", "#Operations"],
    "TikTok": ["#fyp", "#SmallBusinessTok", "#ProductivityHack", "#foryoupage"],
}

GENERIC_CTAS = {
    "X": "More details: link in bio.",
    "Instagram": "Full details are in the link in bio.",
    "LinkedIn": "Details are in the comments below.",
    "TikTok": "It's linked in my bio, go check it out.",
}

GENERIC_FIRST_COMMENT = {
    "X": "Replying here with the link so it doesn't get buried.",
    "Instagram": "Link's in my bio — comment if you want the details.",
    "LinkedIn": "Link and pricing are in this first reply.",
    "TikTok": "Comment LINK and I'll send it your way.",
}


def load_styles() -> list[dict]:
    with open(STYLES_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["styles"]


def _seeded_rng(product: str, platform: str, tone: str) -> random.Random:
    seed = hashlib.sha256(f"{product}|{platform}|{tone}".encode("utf-8")).hexdigest()
    return random.Random(seed)


def extract_audience(product: str) -> str | None:
    """Pull an explicit audience out of phrasing like '... for freelancers'."""
    match = re.search(r"\bfor ([a-zA-Z][a-zA-Z\s]{2,30})$", product.strip())
    if match:
        return match.group(1).strip().rstrip(".")
    return None


def slugify_tag(product: str) -> str:
    """Turn a product description into a hashtag-safe PascalCase word."""
    words = re.findall(r"[A-Za-z0-9]+", product)
    words = [w for w in words if w.lower() not in STOPWORDS]
    words = words[:3] if words else ["Product"]
    return "".join(w.capitalize() for w in words)


def rank_pool(styles: list[dict], platform: str, tone: str) -> list[dict]:
    """Priority-order style entries: exact match first, then partial, then any."""
    exact = [s for s in styles if s["platform"] == platform and s["tone"] == tone]
    same_platform = [s for s in styles if s["platform"] == platform and s not in exact]
    same_tone = [s for s in styles if s["tone"] == tone and s["platform"] != platform]
    rest = [s for s in styles if s not in exact + same_platform + same_tone]
    return exact + same_platform + same_tone + rest


def fill_slots(template: str, product: str, platform: str, tone: str, rng: random.Random,
                audience: str | None) -> str:
    product = product.strip().rstrip(".")
    product_cap = product[:1].upper() + product[1:] if product else product
    benefit = rng.choice(BENEFIT_BANK[tone])
    pain = rng.choice(PAIN_BANK[tone])
    aud = audience or rng.choice(AUDIENCE_BANK[tone])
    emoji = rng.choice(EMOJI_BANK[tone]) if PLATFORM_ALLOWS_EMOJI[platform] else ""
    text = template.format(
        product=product, Product=product_cap,
        benefit=benefit, Benefit=benefit[:1].upper() + benefit[1:],
        pain=pain, Pain=pain[:1].upper() + pain[1:],
        audience=aud, Audience=aud[:1].upper() + aud[1:],
        emoji=emoji,
    )
    # tidy any double spaces left by an empty emoji slot
    text = re.sub(r"\s{2,}", " ", text).strip()
    # a {pain} slot at the very start of a sentence can land lowercase; fix it
    if text and text[0].islower():
        text = text[0].upper() + text[1:]
    return text


def _dedupe_keep_order(items: list[str], limit: int) -> list[str]:
    seen = set()
    out = []
    for item in items:
        key = item.strip().lower()
        if key and key not in seen:
            seen.add(key)
            out.append(item.strip())
        if len(out) >= limit:
            break
    return out


def generate(product: str, platform: str, tone: str, styles: list[dict] | None = None) -> dict:
    """Core template engine. Returns captions, hooks, hashtags, ctas, first_comment."""
    if not product or not product.strip():
        raise ValueError("Product description is required.")
    if platform not in PLATFORMS:
        raise ValueError(f"platform must be one of {PLATFORMS}")
    if tone not in TONES:
        raise ValueError(f"tone must be one of {TONES}")

    styles = styles if styles is not None else load_styles()
    pool = rank_pool(styles, platform, tone)
    rng = _seeded_rng(product, platform, tone)
    audience = extract_audience(product)
    product_tag = slugify_tag(product)

    captions: list[str] = []
    hooks: list[str] = []
    ctas: list[str] = []
    hashtags: list[str] = []
    first_comments: list[str] = []

    # Cycle through the ranked pool multiple passes so each entry gets
    # filled with a few different word-bank combos, giving real variety
    # instead of the same sentence repeated with one word swapped.
    passes = 4
    for _ in range(passes):
        for entry in pool:
            captions.append(fill_slots(entry["caption"], product, platform, tone, rng, audience))
            hooks.append(fill_slots(entry["hook"], product, platform, tone, rng, audience))
            ctas.append(fill_slots(entry["cta"], product, platform, tone, rng, audience))
            first_comments.append(fill_slots(entry["first_comment"], product, platform, tone, rng, audience))
            for tag in entry["hashtags"]:
                resolved = tag.replace("{ProductTag}", product_tag)
                hashtags.append(resolved)
        if len(_dedupe_keep_order(captions, 10)) >= 10 and len(_dedupe_keep_order(hooks, 10)) >= 10:
            break

    captions = _dedupe_keep_order(captions, 10)
    hooks = _dedupe_keep_order(hooks, 10)
    ctas = _dedupe_keep_order(ctas, 3)
    hashtags += GENERIC_HASHTAGS[platform]
    hashtags = _dedupe_keep_order(hashtags, 15)
    first_comment = _dedupe_keep_order(first_comments, 1)

    # Pad out to the promised counts if the matched pool ran short
    # (only happens for very short/odd product descriptions). Cap attempts
    # so an exhausted word bank can't loop forever.
    attempts = 0
    while len(captions) < 10 and attempts < 200:
        captions = _dedupe_keep_order(
            captions + [fill_slots(rng.choice(pool)["caption"], product, platform, tone, rng, audience)], 10
        )
        attempts += 1
    attempts = 0
    while len(hooks) < 10 and attempts < 200:
        hooks = _dedupe_keep_order(
            hooks + [fill_slots(rng.choice(pool)["hook"], product, platform, tone, rng, audience)], 10
        )
        attempts += 1
    while len(ctas) < 3:
        ctas = _dedupe_keep_order(ctas + [GENERIC_CTAS[platform]], 3)
        if len(ctas) < 3:
            break  # only one generic CTA per platform; avoid an infinite loop
    attempts = 0
    while len(hashtags) < 15 and attempts < 50:
        hashtags = _dedupe_keep_order(hashtags + [rng.choice(GENERIC_HASHTAGS[platform])], 15)
        attempts += 1
    filler_n = 1
    while len(hashtags) < 15:  # last resort: numbered platform tag, always unique
        hashtags = _dedupe_keep_order(hashtags + [f"#{platform.replace(' ', '')}Tip{filler_n}"], 15)
        filler_n += 1
    if not first_comment:
        first_comment = [GENERIC_FIRST_COMMENT[platform]]

    return {
        "product": product,
        "platform": platform,
        "tone": tone,
        "captions": captions[:10],
        "hooks": hooks[:10],
        "hashtags": hashtags[:15],
        "ctas": ctas[:3],
        "first_comment": first_comment[0],
    }


# ---------------------------------------------------------------------------
# Optional LLM upgrade. Off by default. Only runs if a key is present and the
# caller opts in; any error falls back to the template result untouched.
# ---------------------------------------------------------------------------

def available_llm_provider() -> str | None:
    if os.environ.get("ANTHROPIC_API_KEY"):
        return "anthropic"
    if os.environ.get("OPENAI_API_KEY"):
        return "openai"
    return None


def llm_polish(result: dict) -> tuple[dict, str | None]:
    """
    Rewrite the template output with an LLM for extra polish. Returns
    (result, error). On any failure, returns the original result and an
    error string so the caller can show a friendly fallback message.
    """
    provider = available_llm_provider()
    if provider is None:
        return result, "No ANTHROPIC_API_KEY or OPENAI_API_KEY set. Using template output."

    try:
        import requests
    except ImportError:
        return result, "The 'requests' package is not installed. Using template output."

    prompt = (
        f"Polish these social captions for {result['platform']} in a {result['tone']} tone. "
        f"Product: {result['product']}. Keep the same count and structure. Return plain text, "
        f"one item per line, in this order: 10 captions, then 10 hooks, then 15 hashtags, "
        f"then 3 CTAs, then 1 first-comment line. No numbering, no extra commentary.\n\n"
        f"Captions:\n" + "\n".join(result["captions"]) + "\n\n"
        f"Hooks:\n" + "\n".join(result["hooks"]) + "\n\n"
        f"Hashtags:\n" + " ".join(result["hashtags"]) + "\n\n"
        f"CTAs:\n" + "\n".join(result["ctas"]) + "\n\n"
        f"First comment:\n" + result["first_comment"]
    )

    try:
        if provider == "anthropic":
            resp = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": os.environ["ANTHROPIC_API_KEY"],
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": "claude-3-5-haiku-20241022",
                    "max_tokens": 1500,
                    "messages": [{"role": "user", "content": prompt}],
                },
                timeout=30,
            )
            resp.raise_for_status()
            text = resp.json()["content"][0]["text"]
        else:
            resp = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
                    "content-type": "application/json",
                },
                json={
                    "model": "gpt-4o-mini",
                    "max_tokens": 1500,
                    "messages": [{"role": "user", "content": prompt}],
                },
                timeout=30,
            )
            resp.raise_for_status()
            text = resp.json()["choices"][0]["message"]["content"]

        parsed = _parse_llm_output(text, result)
        return parsed, None
    except Exception as exc:  # noqa: BLE001 - any failure just degrades gracefully
        return result, f"LLM polish failed ({exc}). Showing template output instead."


def _parse_llm_output(text: str, fallback: dict) -> dict:
    """Best-effort split of a plain-text LLM response back into sections."""
    lines = [ln.strip("-* \t") for ln in text.splitlines() if ln.strip()]
    if len(lines) < 29:
        # Not enough lines to trust the split; keep the template result.
        return fallback
    out = dict(fallback)
    out["captions"] = lines[0:10]
    out["hooks"] = lines[10:20]
    out["hashtags"] = " ".join(lines[20:21]).split() if len(lines) > 20 else fallback["hashtags"]
    out["ctas"] = lines[21:24] if len(lines) >= 24 else fallback["ctas"]
    out["first_comment"] = lines[24] if len(lines) > 24 else fallback["first_comment"]
    return out


if __name__ == "__main__":
    result = generate("a 30-day fitness planner PDF for busy parents", "Instagram", "bold")
    print(json.dumps(result, indent=2))
