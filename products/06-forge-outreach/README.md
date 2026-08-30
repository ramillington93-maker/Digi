# ForgeOutreach

Turn an offer, an ICP, and a proof point into a 5-email cold outreach
sequence in one click.

ForgeOutreach builds day 0, 2, 4, 7, and 12 emails — each with two
subject lines for A/B testing, a full body, and a matching LinkedIn DM.
Export a plain `.txt` copy or a `.csv` shaped for Instantly, Lemlist,
Smartlead, or any bulk-upload sequencer.

No API key required. No account. No SMTP. This tool generates text —
it never sends anything.

## What it does

- Takes three inputs: your offer, your ideal customer profile (ICP),
  and one proof point (a stat, testimonial, or result).
- Fills them into 5 pre-built angles: intro, value/proof, case study,
  objection handling, breakup.
- Gives you two subject lines per email (A and B) so you can split-test.
- Adds a short LinkedIn DM variant for each day.
- Leaves `{{first_name}}` and `{{company}}` in place as merge fields so
  your sending tool fills them in per contact.
- Exports to `.txt` (read it, paste it) and `.csv` (day, subject_a,
  subject_b, body, linkedin_dm — ready for bulk upload).
- Optional: if you set `ANTHROPIC_API_KEY` or `OPENAI_API_KEY`, a
  "Polish tone with AI" checkbox appears and can rewrite the bodies. If
  the call fails or you have no key, the app falls back to the template
  output — nothing breaks.

## 3-step setup

1. Install Python 3.11, then install the dependencies:
   ```
   pip install -r requirements.txt
   ```
2. (Optional) Copy `.env.example` to `.env` and add an API key only if
   you want the AI polish option. Skip this step entirely if you don't
   — the tool works fully without it.
3. Run the app:
   ```
   streamlit run app.py
   ```
   Your browser opens to `localhost:8501`. Fill in offer, ICP, and
   proof point, click **Generate sequence**, then download the `.txt`
   or `.csv`.

## Example

**Offer:** A done-for-you cold email sequence generator for freelance developers
**ICP:** Freelance web developers who land 1-3 client projects a month and hate writing outreach
**Proof point:** Beta users landed 3 replies from 40 sends in the first week

That produces a full 5-email sequence with day-appropriate angles and
LinkedIn DMs. See [`sample-output.md`](./sample-output.md) for the
complete, unedited output.

Tip: short, phrase-length offer and ICP fields ("a Notion template for
freelance designers") read tighter than full sentences.

## FAQ

**Do I need an API key?**
No. The core generator is template logic — offer, ICP, and proof point
get filled into 5 fixed angles. It runs with zero network calls.

**What's the optional AI polish for?**
If you set `ANTHROPIC_API_KEY` or `OPENAI_API_KEY`, a checkbox appears
to rewrite the email bodies for tone. It's optional. If the API call
fails, times out, or the key is missing, the app silently falls back to
the template version — you always get a usable sequence.

**Does this send emails?**
No. ForgeOutreach only generates text. Sending is on you — paste the
output into your own email client, or bulk-upload the `.csv` into
Instantly, Lemlist, Smartlead, or similar.

**What do `{{first_name}}` and `{{company}}` mean?**
They're merge fields, left untouched in the output on purpose. Most
sequencers (Instantly, Lemlist, Apollo, Smartlead) replace these
automatically from your contact list on import.

**Can I edit the templates?**
Yes. `app.py` has one function, `generate_sequence()`, with all 5 email
bodies as plain Python strings. Edit the wording directly.

**What Python version does this need?**
3.11. Dependencies are pinned in `requirements.txt`.

## License

See [`LICENSE.txt`](./LICENSE.txt). Short version: it's yours to run,
modify, and use for client work — you can't resell or redistribute the
product files themselves.

---

A ForgeKit product by Orynix Technologies
