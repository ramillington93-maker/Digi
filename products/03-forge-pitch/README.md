# ForgePitch

Turn a job post into a proposal in 30 seconds.

Paste a freelance job post and your 5-line profile. Get a proposal body,
3 subject line options, 3 price anchors (low / mid / premium), and a
P.S. line that handles the price or timeline objection before it's
asked. Runs fully offline in template mode — no API key required.

A ForgeKit product by Orynix Technologies.

## What it does

ForgePitch reads the job post text and pulls out real signals:

- **Skills mentioned** (matched against a niche keyword list — web dev,
  content writing, data/admin, design, marketing)
- **Budget hints** (a `$X-$Y` range, an hourly rate, or a flat number)
- **Tone** (urgent, formal, casual, or neutral)

It uses those signals — not a fixed template string — to write an
opening line that quotes the job post, a relevant-experience paragraph
built from skills you and the client both mentioned, a 3-step approach
matched to the niche, subject lines, price anchors scaled off the
detected budget (or your rate if no budget was posted), and a P.S. that
addresses whichever objection the post signals (price or timeline).

If neither `ANTHROPIC_API_KEY` nor `OPENAI_API_KEY` is set, you get the
full template output above — that's the whole product, working. If one
of those keys is set, an optional "polish" pass can rewrite the draft
in nicer prose. If that call fails for any reason (no key, bad key, no
network), it silently falls back to the template output. You never see
an error, and you never need a key to use this product.

## 3-step setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Run one of the two entry points (they do the same thing):
   ```
   python cli.py --job samples/job_post_1.txt --profile samples/sample_profile.txt
   ```
   or
   ```
   streamlit run app.py
   ```
3. Read the output. Copy the subject line and proposal body into
   Upwork, LinkedIn, or email. Pick a price anchor. Done.

The Streamlit app ships with `.streamlit/config.toml` already set to
the ForgeKit dark theme — no extra setup needed there.

Optional: copy `.env.example` to `.env` and set `ANTHROPIC_API_KEY` or
`OPENAI_API_KEY` to turn on the AI-polish step. Not required.

## Your profile format

Five lines, in this order (labels optional but recommended):

```
Name: Jamie Rivera
Skills: Python, Django, REST APIs, PostgreSQL
Experience: 5 years building backend APIs for early-stage startups
Rate: $55/hr
Portfolio: jamierivera.dev
```

## Example

Run:
```
python cli.py --job samples/job_post_1.txt --profile samples/sample_profile.txt
```

See `sample-output.md` in this folder for the full, real output that
command produces — a proposal for a Django/API bug-fix job, generated
in template mode, no API key used.

## CLI flags

| Flag | Meaning |
|---|---|
| `--job PATH` | Path to a text file with the job post. Omit to paste via stdin. |
| `--profile PATH` | Path to your 5-line profile file. Omit to paste via stdin. |
| `--out PATH` | Write the proposal to a file instead of printing it. |
| `--no-enhance` | Skip the AI-polish step even if a key is set. |

## FAQ

**Do I need an API key?**
No. Template mode is the full product and needs nothing but Python.
An API key only unlocks an optional prose-polish pass.

**Does it work for niches outside the 3 sample categories?**
Yes. The keyword sets cover web dev, content writing, data/admin
support, design, and marketing. Anything else still gets a full
proposal — the niche label just falls back to "general freelance work"
and the approach section uses a generic 3-step template.

**Will the proposal claim skills I don't have?**
No. If your profile's skills don't overlap with what the job post
mentions, ForgePitch doesn't fabricate an overlap — it falls back to
listing your actual stated skills instead of pretending they match.

**Can I edit the templates?**
Yes. Everything is in `core.py` — the wording, the niche keyword lists,
and the price-anchor math are plain Python, not a hidden prompt.

**Is this connected to Upwork or any job board?**
No. It reads pasted text only. You copy the job post in, you copy the
proposal out.

## License

See `LICENSE.txt`. Buy-once license for personal or client use. No
resale or redistribution of the product files. Full terms in the file.
