# ForgeQuiz — Copy Reference

Every piece of text in the quiz, in one place. Edit this file first to
draft your new niche, then copy the final text into `index.html` (see
"Where this lives in index.html" at the bottom).

## Page title / headline

- **Quiz title:** Which digital product should you sell this week?
- **Subheading (fixed, not in JS data):** 7 quick questions. Get a
  specific product idea, not generic advice.

## Questions and options

Each question has 3 options. Each option belongs to a bucket: A, B, or
C. The bucket with the most answers at the end decides the result.

### Q1. How much time can you put in this week?
- A — Under 2 hours
- B — A few evenings
- C — A full weekend or more

### Q2. What do you already have finished or half-finished?
- A — Notes, docs, or a spreadsheet template
- B — A skill people ask me to teach
- C — Code, a script, or a working tool

### Q3. Where do you want to sell?
- A — Gumroad or a simple storefront
- B — A cohort, community, or DMs
- C — Wherever developers hang out

### Q4. What's your comfort level with code?
- A — None, and I don't want any
- B — I can follow instructions and copy-paste
- C — I write code regularly

### Q5. What price point sounds right to start?
- A — $9-$29, low friction, high volume
- B — $49-$199, coaching or cohort-priced
- C — $19-$79, tool-priced for other builders

### Q6. What's your biggest asset right now?
- A — A messy pile of knowledge I haven't organized
- B — An audience or a network that trusts me
- C — A tool or script that already saves time

### Q7. What does "done" look like for you this week?
- A — One file or template someone can buy today
- B — One paid session or short course booked
- C — One tool live and listed for sale

## Results

### Result A — The Template Seller
- **Kicker:** Your result: The Template Seller
- **Title:** Sell a template or notion/spreadsheet kit
- **Description:** You've got scattered knowledge and limited hours.
  Package what you already know into one file. No code, no calls, no
  inventory.
- **Do this next:**
  1. Pick ONE process you already do well (budget tracker, content
     calendar, onboarding doc).
  2. Turn it into a clean template file today: Notion, Sheets, or a PDF.
  3. List it on Gumroad at $9-$29. Write the price and setup time on
     the sales page.
  4. Post one before/after screenshot where your audience already
     hangs out.

### Result B — The Knowledge Seller
- **Kicker:** Your result: The Knowledge Seller
- **Title:** Sell a short paid session or mini-course
- **Description:** People already ask you questions. Stop answering
  for free. Package the answer once, sell it on repeat.
- **Do this next:**
  1. Write down the 5 questions people ask you most.
  2. Turn the best one into a 45-minute paid session or a 20-minute
     recorded lesson.
  3. Price it at $49-$199. State exactly what they walk away with.
  4. Offer it to the next 3 people who ask you that question for free.

### Result C — The Tool Builder
- **Kicker:** Your result: The Tool Builder
- **Title:** Sell a small tool other builders will pay for
- **Description:** You can write code and you already have something
  working. Wrap it, price it, ship it — don't rebuild it from scratch.
- **Do this next:**
  1. Take the script or tool you already have and cut it down to one
     clear use case.
  2. Add a simple UI or README so a non-technical buyer can use it in
     under 5 minutes.
  3. Price it at $19-$79 and list it where developers or indie
     builders browse.
  4. Ship the first version this week, even if it only does one thing
     well.

## Downloaded result file copy

When a visitor submits their email, the browser generates a `.txt`
file with:

```
[Quiz title]
[Date]
Prepared for: [visitor's email]

[Result kicker]
[Result title]

[Result description]

Do this next:
1. [step]
2. [step]
3. [step]
4. [step]

--
A ForgeKit product by Orynix Technologies
```

This template lives in the JavaScript, inside the `capture-form`
submit handler. Edit the `lines.push(...)` calls there if you want to
change the file's layout — the content (title, description, steps)
automatically pulls from `RESULTS`, so you rarely need to touch this
part.

## Where this lives in index.html

Open `index.html` in a text editor and search for the comment
`// QUIZ DATA`. You'll find three JavaScript variables:

- `QUIZ_TITLE` — a single string. Matches "Quiz title" above.
- `QUESTIONS` — an array of 7 objects, each with `text` and an
  `options` array of `{ label, bucket }`. Matches "Questions and
  options" above, in order.
- `RESULTS` — an object with keys `A`, `B`, `C`, each with `kicker`,
  `title`, `desc`, and a `steps` array of 4 strings. Matches "Results"
  above.

To relaunch with a new niche: rewrite this document section by
section, then paste the matching strings into the JavaScript variables
in `index.html`. Keep the array lengths the same (7 questions, 3
options each, 3 results, 4 steps each) unless you're comfortable
adjusting the surrounding JavaScript.
