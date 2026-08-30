#!/usr/bin/env python3
"""
ForgePitch CLI -- paste a job post + your profile, get a proposal.

Usage:
    python cli.py
    python cli.py --job samples/job_post_1.txt --profile samples/sample_profile.txt
    python cli.py --job samples/job_post_1.txt --profile samples/sample_profile.txt --out out.md

No API key needed. If ANTHROPIC_API_KEY or OPENAI_API_KEY is set in the
environment (or a .env file), the CLI will try to polish the output and
falls back to the plain template automatically if that call fails.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from core import enhance_with_llm, format_proposal_markdown, generate_proposal


def _load_dotenv_if_present() -> None:
    """Minimal .env loader -- no extra dependency required."""
    env_path = Path(__file__).parent / ".env"
    if not env_path.exists():
        return
    import os

    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def _read_text(prompt_label: str, file_arg: str | None) -> str:
    if file_arg:
        return Path(file_arg).read_text(encoding="utf-8")
    print(f"\nPaste {prompt_label}, then press Enter and Ctrl-D (Ctrl-Z on Windows):")
    return sys.stdin.read()


def main() -> None:
    _load_dotenv_if_present()

    parser = argparse.ArgumentParser(description="Generate a freelance proposal from a job post.")
    parser.add_argument("--job", help="Path to a text file with the job post.")
    parser.add_argument("--profile", help="Path to a text file with your 5-line profile.")
    parser.add_argument("--out", help="Write the proposal to this file instead of stdout.")
    parser.add_argument(
        "--no-enhance",
        action="store_true",
        help="Skip the optional LLM polish step even if an API key is set.",
    )
    args = parser.parse_args()

    job_text = _read_text("the job post", args.job)
    if not job_text.strip():
        print("Job post is empty. Nothing to do.", file=sys.stderr)
        sys.exit(1)

    profile_text = _read_text(
        "your 5-line profile (Name / Skills / Experience / Rate / Portfolio)", args.profile
    )
    if not profile_text.strip():
        print("Profile is empty. Nothing to do.", file=sys.stderr)
        sys.exit(1)

    proposal = generate_proposal(job_text, profile_text)
    markdown = format_proposal_markdown(proposal)

    status = "template"
    if not args.no_enhance:
        markdown, status = enhance_with_llm(markdown, job_text, profile_text)

    if status == "enhanced":
        footer = "\n---\n_Polished with an LLM. Set no --no-enhance flag to use the free template mode._\n"
    else:
        footer = "\n---\n_Generated in template mode -- no API key used._\n"
    markdown = markdown + footer

    if args.out:
        Path(args.out).write_text(markdown, encoding="utf-8")
        print(f"Wrote proposal to {args.out} ({status} mode).")
    else:
        print("\n" + markdown)


if __name__ == "__main__":
    main()
