# ForgeResume

Paste a resume and a job description. Get a real match score, the exact
keywords you're missing, and stronger bullets. No account, no upload to a
server — it runs on your machine.

A ForgeKit product by Orynix Technologies.

## What it does

- **Match score** — real keyword overlap between your resume and the job
  description, computed by tokenizing both texts, stripping stopwords, and
  stemming (so "managed" and "managing" count as the same skill). No API
  call, no guesswork.
- **Missing keywords** — the exact terms in the job post that aren't in
  your resume, ranked by how often the job post uses them.
- **STAR bullet rewrite** — paste one weak bullet, get it rewritten as
  Situation / Task / Action / Result, with missing keywords worked in
  where they fit.
- **Tailored summary** — a 3-4 sentence professional summary built from
  what actually matches, ready to paste at the top of your resume.

The score and missing-keyword list work fully offline. The bullet rewrite
and summary work offline too, with a rule-based template — add an API key
and they get rewritten by an LLM instead. Either way, nothing you paste in
leaves your machine unless you add a key.

## Setup (3 steps)

1. Install Python 3.11+, then install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. (Optional) Copy `.env.example` to `.env` and add an `ANTHROPIC_API_KEY`
   or `OPENAI_API_KEY` if you want LLM-written bullet rewrites and
   summaries instead of the rule-based template. Skip this step entirely
   if you don't have a key — the app still works.
3. Run it:
   ```
   streamlit run app.py
   ```
   Opens at `http://localhost:8501`.

## Example

Using the sample files in `/samples`:

- `resume_1.txt` (marketing coordinator) against `jd_1.txt` (growth
  marketing manager posting) scores **25.0%** match, with 25 of 100
  distinct job-post keywords found in the resume.
- `resume_2.txt` (software engineer) against `jd_2.txt` (senior backend
  engineer posting) scores **29.2%** match, with 26 of 89 keywords found.

See `sample-output.md` for the full output, including the missing-keyword
list and a rewritten bullet.

Upload your own `.txt` files or paste text directly — either input method
works for both the resume and the job description.

## FAQ

**Do I need an API key?**
No. Scoring and missing-keyword detection are 100% offline. An API key
only upgrades the bullet rewrite and summary from a template to an
LLM-written version.

**Does my resume get uploaded anywhere?**
No, unless you add an API key and use the rewrite/summary features — in
that case, only the specific bullet or resume text you're rewriting is
sent to Anthropic or OpenAI's API for that one request. The scoring
engine never makes a network call.

**Why isn't my score higher — I clearly have this skill?**
The scorer matches on words that appear in your resume text, not skills
it infers. If the job post says "Kubernetes" and your resume says
"container orchestration," add the literal word if it's true of you.
That's the point of the missing-keywords list.

**Can I use this for more than one resume?**
Yes. No usage limits, no per-resume fee. Use it on every application.

**What format does it accept?**
Plain text (paste it in, or upload a `.txt` file). Export your resume and
the job posting to plain text first if they're in PDF or Word format.

**Can I edit the code?**
Yes — see LICENSE.txt for what's allowed. Short version: use and modify
it for yourself and clients, don't resell the source files.

## License

See `LICENSE.txt`. You can use this on unlimited resumes and client work.
You can't resell or redistribute the product files themselves.

---
A ForgeKit product by Orynix Technologies.
