# Before and After: Six Prompt Rewrites

Theory only gets you so far. This chapter shows six prompts that failed in
six different real-life-shaped ways, and rewrites each one in steps you can
follow with your own flops. Every rewrite uses moves you have already
learned — nothing new is pulled in.

Diagnosis first, rewrite second. Read the "before," try writing your own
better version *before* reading the fix. That self-test is the fastest way
to make this chapter permanent.

## Rewrite 1: The reseller's photo list

```text
Before: describe my item for a listing
```

Diagnosis: no item (context), no audience, no format, no length. The reply
was a paragraph of generic auction-desk prose. Chapter 1's failure habit:
the me-too prompt.

```text
After:
I sell vintage kitchenware on eBay. Here are my notes on this lot:
[NOTES: 6 stainless ladles, mixed sizes, some tarnish, no logo]

Write my listing description: 120 words max. First a 25-word lead
paragraph, then a 4-bullet flaws-and-conditions list (be specific, use
my notes, never invent condition words). Match the plain, honest tone
of this example I wrote last week: "[YOUR EXAMPLE]". No hype words, no
all-caps, no "vintage charm" nonsense.
```

Notice the moves: *context* (who, what lot), *format* (lead + bullets,
word cap), *example* (tone), *carve-outs* (no hype, no invented condition).
Four moves, one prompt, about ninety seconds.

## Rewrite 2: The nurse's read-back

```text
Before: write a teach-back script for my patients about insulin pens
```

Diagnosis: an audience line that means five different things and a task
word ("write") with no shape. Also: a health-adjacent task, so the
education-only boundary matters *in the prompt itself*.

```text
After:
You are a plain-English patient educator (education only — this is a
handout draft; my pharmacist and care plan are the source of truth).

TASK: Draft a 6-step teach-back conversation for adults starting
insulin pens. In each step, the patient does the talking; I mostly
listen.

FORMAT: numbered steps, 20 words max each, plain English, no jargon
without a same-sentence translation. End with two sentences I should
say if the patient cannot teach it back. Then a final line, exactly:
"Practice questions? Ask your care team — this is education, not
medical advice."
```

The material came from the pharmacist's sheet (pasted above the TASK line
in the real thing). The boundary line is *written into the prompt*, which
is how Chapter 5's handout card does it too.

## Rewrite 3: The newsletter nobody finished

```text
Before: punch up my newsletter intro, add some energy, keep it professional
```

Diagnosis: a vibe prompt. "Energy" and "professional" pulled against each
other, so the model split the difference into mush.

```text
After:
Here is my newsletter intro: [PASTE]

Go three rounds against it:
Round 1: the same intro with ALL sentences 12 words or fewer.
Round 2: the same but starting with the most concrete image in the piece.
Round 3: the same but addressing the reader as "you" throughout.
Send all three versions, then one line: which change made the most
difference and why.
```

Instead of asking for "energy" (undefined), it asked for three *countable
variations* and made the model show its work. You pick the one — and the
pickers become your tone instincts.

## Rewrite 4: The family budget that went fictional

```text
Before: make a budget for me
```

Diagnosis: no numbers, no reality. The reply invented an income, a rent,
even a city. Fabrication, the Chapter 1 habit the prompts fastest.

```text
After:
Here are my actual numbers for last month — use ONLY these, do not add
anything:
[TABLE: paychecks 2,340 total; rent 950; utilities 118; groceries 385;
fuel 95; other receipts: pasted below]
---RECEIPTS---
[PASTE]
---END RECEIPTS---

TASK: 1) Sort spending into 4 plain-English buckets. 2) Name the one
bucket most likely to shrink next month without changing my life much,
with the reason. 3) One sentence max of encouraging honesty, no lecture.
FORMAT: short table for the buckets, then two labeled paragraphs.
```

"Do not add anything" + pasted receipts = reality-anchored. The one nudge
request keeps optimism from becoming an intervention.

## Rewrite 5: The plan that needed a pre-mortem

```text
Before: is this a good idea?
```

Diagnosis: an unanswerable question — "good" compared to what, for whom,
with what constraints? A yes/no confabulation machine. Chapter 5's
Pre-Mortem card solves this whole class of prompts:

```text
After (the card, filled):
I am about to do this: convert my garage shelves to a small eBay
business. I have $400 to spend, 5 hours a week, and listings I have
sold before with mild success.

You are a friendly but blunt reviewer who wants me to succeed. List the
five most likely ways this goes sideways — practical ones, from my own
details, not generic warnings. For each: the one thing I could change
now that removes the risk. Do not pad with disclaimers.
```

Same hesitation as the original ("should I?"), but now the details
constrain the model, and the model's job is to break your plan kindly and
specifically, not to grade it.

## Rewrite 6: The chat that needed the meter

```text
Before: (after the fourth long reply that went sideways) you missed the point again
```

Diagnosis: this prompt blames the reply — the loop from Chapter 3 turned
into an argument. Two better prompts, sent in order:

```text
First: Diagnose my last message, not your last reply: what am I asking
for that my words don't actually specify? Ask me anything you need.
(The Interview-First card, Chapter 5.)

Then: Rewrite ONE thing in my prompt and try again. (The one-variable
tweak, Chapter 3.)
```

The difference between a bad chat session and a good one is often just
this pivot — from arguing with the output to editing the input.

## The pattern across all six

Three moves did 90% of the repair work:

- **Feed reality, forbid invention.** Real notes, real receipts, real examples + "do not add anything."
- **Specify shape.** Word caps, bullet counts, "exactly these sections."
- **Pick ONE thing to change.** Diagnose in a sentence, patch one variable, re-run.

Run your next flopped prompt against those three — one of them will almost
always be the fix.

Cleanup time. If any of your fixed prompts will ever be used again, they
belong somewhere retrievable. That's exactly what's coming: [Chapter 7](07-building-a-prompt-library.md).
