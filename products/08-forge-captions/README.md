# ForgeCaptions

Turn a product description into 10 captions, 10 hooks, 15 hashtags, 3 CTAs, and a first-comment line.

A ForgeKit product by Orynix Technologies. Ship today. Cash tomorrow.

## What it does

You type what you're selling, pick a platform (X, Instagram, LinkedIn, TikTok) and a tone (bold, friendly, professional, funny). ForgeCaptions returns:

- 10 captions
- 10 hooks (the first line, separate from the caption body)
- 15 hashtags
- 3 CTA variants
- 1 first-comment line — a comment to post right after you publish, written to get replies

It works by matching your platform and tone against 20 real caption/hook patterns in `samples/styles.json`, then filling in the slots with your product and a tone-matched word bank. That's the whole mechanism — a template engine, not a black box. Same input always gives you the same output, so you can tweak your product description and re-run it until it reads right.

No account. No API key. No internet connection required for the core feature.

## Setup — 3 steps

1. Install Python 3.11, then install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Run the app:
   ```
   streamlit run app.py
   ```
3. Open the URL Streamlit prints (usually `http://localhost:8501`), type your product description, pick a platform and tone, click Generate.

That's it. No `.env` file needed for the default path.

### Optional: AI polish pass

If you set `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` in a `.env` file (copy `.env.example` to `.env` and fill one in), a checkbox appears in the app to send the template output to that API for a light rewrite. This is optional. If the key is missing, invalid, or the request fails for any reason, the app falls back to the template output automatically — you always get a result.

### Prefer the command line?

The generator also runs without the UI:
```
python3 -c "from generator import generate; import json; print(json.dumps(generate('a 30-day fitness planner PDF for busy parents', 'Instagram', 'bold'), indent=2))"
```

## Example

Input: `a 30-day fitness planner PDF for busy parents`, platform `Instagram`, tone `bold`.

See `sample-output.md` for the full generated result — 10 captions, 10 hooks, 15 hashtags, 3 CTAs, 1 first comment, exactly as the app produces it.

## FAQ

**Do I need an API key?**
No. The core generator is template-based and runs fully offline. The API key only unlocks an optional polish pass.

**Will the captions sound generic?**
They're built from 20 real style patterns, not generated from a blank prompt. Swap in your own product description and the phrasing changes around it — the tone and structure stay consistent with what you picked.

**Can I add my own caption styles?**
Yes. `samples/styles.json` is plain JSON. Add an entry with the same fields (`platform`, `tone`, `hook`, `caption`, `cta`, `hashtags`, `first_comment`) and it joins the pool the next time you generate.

**Can I edit the output before posting?**
Yes, and you should. Treat this as a first draft that gets you 90% there in seconds, not a publish button.

**Does it post to social media for me?**
No. It generates text. You copy, paste, and post it yourself.

**What platforms are supported?**
X, Instagram, LinkedIn, TikTok. Each has its own hashtag conventions and CTA style baked into the templates.

## License

See `LICENSE.txt`. Short version: use it, modify it, sell what you make with it — don't resell the product files themselves.

---
A ForgeKit product by Orynix Technologies.
