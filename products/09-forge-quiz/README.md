# ForgeQuiz

A 7-question lead-magnet quiz. Visitors answer, get routed to one of 3
results, and download a result file with their email on it. No backend.
No database. No monthly fee.

Default niche: "Which digital product should you sell this week?"
Swap it for your own niche in about 15 minutes.

## What it does

- 7 multiple-choice questions, 3 answers each.
- Each answer scores toward one of 3 result buckets (A, B, C).
- The result screen shows a title, a description, and 4 next steps.
- The visitor enters their email and clicks "Download my result." The
  page builds a `.txt` file in the browser (via a Blob) and downloads it
  automatically — their result, their email, your branding, no server.
- A progress bar, back button, and retake button are built in.

## Setup — 3 steps

1. Unzip the folder.
2. Double-click `index.html`. It opens in your browser and works
   immediately — no install, no server, no internet required after the
   fonts load once.
3. Customize the quiz: open `QUIZ-COPY.md` to see every question,
   option, and result written out in plain text, then edit the matching
   block inside `index.html` (see "How to edit the copy" below).

## Example

Visitor answers 7 questions about time, skills, and price comfort.
Most of their answers land in bucket "C." They land on:

> **Your result: The Tool Builder**
> Sell a small tool other builders will pay for.
> Do this next: 1) Cut your script down to one use case. 2) Add a
> README. 3) Price it $19-$79. 4) Ship it this week.

They type their email, click download, and get `quiz-result-c.txt` —
their result, saved to their device, in under a second.

## How to edit the copy

Open `index.html` in any text editor and find the comment block:

```
// QUIZ DATA
// To change the niche or copy, edit this block.
```

- `QUIZ_TITLE` — the headline shown at the top of the page and in the
  browser tab.
- `QUESTIONS` — an array of 7 objects. Each has `text` (the question)
  and `options` (3 choices). Each option has a `label` (what the
  visitor sees) and a `bucket` (`"A"`, `"B"`, or `"C"` — which result it
  scores toward).
- `RESULTS` — an object with 3 keys (`A`, `B`, `C`). Each has `kicker`
  (small label), `title`, `desc`, and `steps` (an array of 4 strings).

You can add or remove options per question, but keep exactly 3 buckets
(A, B, C) so every question maps cleanly to a result. `QUIZ-COPY.md`
lists every string in the file so you can draft your new copy there
first, then paste it into `index.html`.

## Turning on real email capture

Out of the box, ForgeQuiz has no backend. The download button proves
the quiz works and gives the visitor something real, but it does not
add anyone to a mailing list. To actually collect emails:

1. Create a form in ConvertKit, Mailchimp, or any provider that gives
   you a plain HTML embed form with an `action` URL and an `<input
   name="email">` field.
2. Copy that provider's `<form>` tag.
3. In `index.html`, find `<form id="capture-form">` and either:
   - Replace its `action` attribute with the provider's URL and remove
     (or keep, as a fallback) the `submit` JavaScript listener, or
   - Add a second, hidden form using the provider's markup and submit
     it via JavaScript alongside the existing download logic, so the
     visitor still gets their file **and** lands on your list.
4. Test with your own email before sending traffic.

Full step-by-step is in `DEMO.md` under "Swapping in a real email
provider."

## FAQ

**Does this need a server?** No. Every file is static. Open
`index.html` directly, no `npm install`, no build step.

**Does it work offline?** Yes, after the first load. The only network
calls are to Google Fonts (optional) — everything else runs locally.

**Where do the emails go?** Nowhere by default. The quiz downloads a
file to the visitor's own device. See "Turning on real email capture"
above to connect a real list.

**Can I change the number of questions or results?** Yes. Add or
remove entries in `QUESTIONS` and keep 3 keys in `RESULTS` (A/B/C).
More than 3 buckets requires editing the `computeBucket()` function.

**Can I use this for a client?** Yes, see `LICENSE.txt`.

**Does it work on mobile?** Yes. Mobile-first CSS, tested down to
375px width.

## License

See `LICENSE.txt`. Short version: use it, modify it, sell what you
build with it — don't resell the template itself.

---
A ForgeKit product by Orynix Technologies.
