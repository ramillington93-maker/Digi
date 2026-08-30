# ForgeQuiz — 20-Second Demo Recording Steps

Goal: show the quiz flow, a result page, and the email capture in
under 20 seconds. Record your screen (QuickTime, OBS, or your phone
pointed at your monitor works fine).

## Recording steps

1. Open `index.html` in a browser at a mobile-ish width (resize the
   window to about 400px wide, or use your browser's device toolbar
   set to a phone size). Start recording.
2. Click through questions 1-3 quickly, one click per option. Let the
   progress bar visibly move.
3. Skip ahead: click through questions 4-7 at a slightly faster pace
   (viewers get the idea after question 3).
4. Let the result screen load. Pause for 1 second so the title and
   "Do this next" list are readable on camera.
5. Click into the email field, type a sample address (e.g.
   `you@email.com`).
6. Click "Download my result." Show the success message
   ("Saved. Check your downloads folder...") appearing.
7. Optionally, show the downloaded `.txt` file opening for one second
   to prove it's a real file with the result inside.
8. Stop recording. Trim dead space at the start/end so the final clip
   is close to 20 seconds.

## What to have visible on screen

- The ForgeQuiz brand tag at the top ("ForgeQuiz · ForgeKit").
- At least one full question-and-answer click.
- The result title and "Do this next" list.
- The email field being filled and the download success message.

## Swapping in a real email provider

The demo above shows the built-in download flow, which works with no
setup. If you want the demo (or the live product) to also add
visitors to a real mailing list:

1. Sign up for ConvertKit, Mailchimp, or any provider that gives you a
   plain HTML form embed (an `action` URL plus an `<input
   name="email">` field). Most providers show this under
   "Landing Pages & Forms" → "Embed" → "HTML form."
2. Copy the `<form>` block the provider gives you.
3. Open `index.html` and find `<form id="capture-form">`.
4. Simplest option: add the provider's `action` URL and `method` to
   that form tag, and rename `email-input`'s `name` attribute to match
   what the provider expects (commonly `email` or `email_address`).
   The existing JavaScript still builds and downloads the result file
   on submit; the browser will also POST to the provider in the
   background if you set the form to submit via `fetch()` instead of
   the default full-page navigation (see the comment above the
   `capture-form` submit listener in `index.html` for where to add
   this).
5. Test it yourself first: submit with your own email, confirm it
   shows up in your ConvertKit/Mailchimp list, and confirm the file
   still downloads.
6. Re-record the demo if you want it to show the real provider's
   confirmation state instead of (or alongside) the built-in one.

This step is optional. The product works and delivers real value
(a downloadable result) with zero setup — this section is for anyone
who wants to build an actual list on top of it.
