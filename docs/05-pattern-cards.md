# Pattern Cards: Recipes You Can Reuse

A *pattern card* is a fill-in-the-blank prompt skeleton for one recurring
job — a recipe, not a one-off. Stop writing prompts from scratch once you
know the job. Keep the card, change the blanks.

This chapter is the book's recipe box: **twelve cards**. Skim the headings,
grab what you need, and skip the rest until the day it applies.

> How to read a card: the `text` block is the skeleton. UPPERCASE words in
> [SQUARE BRACKETS] are your blanks. The one-line note under each card says
> when to use it and which earlier chapters it leans on. Copy the text into
> your editor, fill the blanks, send.

## Card: The Everyday Explainer

For: any concept you want explained like a patient friend would —
drafting lessons, onboarding doc lines, party explanations. (Uses the
role trick from Chapter 2.)

```text
You are a patient teacher explaining [CONCEPT] to [AUDIENCE, e.g. someone
who has never used AI]. Explain it in one short paragraph of plain
English, in your own words. Include one small everyday comparison.
End with one short question that checks whether they followed along.
```

## Card: The Reader-Friendly Rewrite

For: making dense text readable — discharge paperwork, reports, long
emails. (Pairs with the audience line from Chapter 2.)

```text
Rewrite the text between the lines so a busy adult with an 8th-grade
reading level and two minutes gets it. Keep the meaning; cut everything
that does not change what the reader does.

---TEXT START---
[PASTE]
---TEXT END---

Reply as: [SHAPE, e.g. "two paragraphs, then a 4-step checklist"]. Keep
original numbers and names exactly. Do not add facts that are not in the
text.
```

The "do not add facts" line matters for medical and legal text: plain
English without invented content, always.

## Card: The Tone Match

For: any time the reply's voice keeps missing — newsletters, customer
emails, cards. (Best paired with a real example, Chapter 4.)

```text
Match the voice of this example I wrote:

[PASTE YOUR EXAMPLE]

Now write [NEW PIECE, e.g. "this week's intro"] about [TOPIC] in the
same voice. Same sentence length, same warmth, same bad jokes.
Under [WORD CAP] words.
```

## Card: The Table Builder

For: turning notes into comparison tables — plan comparisons, inventory
decisions, menu rotations. (Format-first, Chapter 2.)

```text
Here are my notes: [PASTE NOTES]

Organize them into a table with exactly these columns:
[COLUMN A] | [COLUMN B] | [COLUMN C]
One row per [ITEM]. Leave a cell blank rather than inventing a value.
After the table, add one line: the single biggest trade-off I should know.
```

"Leave a cell blank rather than inventing" quietly kills the model's
politeness reflex to fill every square.

## Card: The Pre-Mortem

For: plans worth double-checking before you commit — travel, launches,
big purchases, workflow changes.

```text
I am about to do this: [PLAN, 1-3 sentences]

You are a friendly but blunt reviewer who wants me to succeed. List the
five most likely ways this goes sideways — practical ones, from my own
details, not generic warnings. For each: the one thing I could change now
that removes the risk. Do not pad with disclaimers.
```

## Card: The Ruthless Editor

For: your own drafts that run long — newsletter intros, book blurbs,
essays. (The self-edit pass before anyone else sees it.)

```text
Here is my draft: [PASTE DRAFT]

Act as an editor with a red pen. Mark up my draft, not a rewrite of it:
1. List the 3 sentences that can be deleted entirely, with a one-word
   reason each.
2. Flag any sentence longer than 25 words.
3. Name the single sentence that most buries the point.
Do NOT rewrite the whole draft. Do not compliment me first.
```

## Card: The Interview-First Prompt

For: when *you* don't know what to ask yet — research briefs, trip plans,
preparing for doctor visits, hiring.

```text
I want help with [GOAL]. Before answering anything, ask me up to five
short questions, one at a time, in plain English — the minimum set you
need to do this well. After my answers, do the task.
```

This one is skipped too often and costs the most when skipped: it turns
"fifty silent assumptions" into five questions you actually answer.

## Card: The Study Buddy

For: learning anything from notes to a new tool — exam prep, a new piece of
software, chess openings. Low-energy friendly: it drives, you answer.

```text
I am learning [TOPIC]. Quiz me like a friendly tutor: one question at a
time, starting easy, slowly harder. After each of my answers: tell me if
I was right, give a one-sentence correction if not, then the next
question. After 10 questions, summarize my two weakest spots in plain
English.
```

## Card: The Plain-Language Handout

For: nurses, teachers, small nonprofits — turning any official material
into something people can actually read. (The education-only house rule
from the introduction applies: it drafts handouts; it never decides care.)

```text
You are a plain-English educator. Convert the material below into a
one-page handout for [AUDIENCE, e.g. "adults newly diagnosed..."].

Rules:
- 6th-grade reading level; short sentences; no unexplained jargon.
- Three sections, each with a 1-line heading in their words, not mine.
- End with the 3 questions patients most often ask, answered in 1-2 lines.
- Include this exact line, unmodified: "Questions? Ask your care team —
  this handout is education, not medical advice."

---MATERIAL---
[PASTE]
---END MATERIAL---
```

## Card: The Fix-My-Prompt

For: when a prompt is fighting you. Ask the model to help you repair the
prompt itself — models are usually good critics of prompts, and it's the
fastest diagnosis partner available (Chapter 3 pair).

```text
Here is a prompt I wrote and the reply I got. Diagnose my prompt, not
the AI: what is vague, what is missing, what is contradictory?

MY PROMPT: [PASTE]
REPLY I GOT: [PASTE, trimmed]

Reply with: the 1 most important fix, then 2 smaller ones, each as an
exact replacement sentence I could paste in. Be kind but do not soften
the criticism.
```

## Card: The Role Playthrough

For: preparing for conversations you're nervous about — raise reviews,
hard family talks, contesting a bill. You rehearse; it plays the other side.

```text
We'll rehearse a conversation. You play [THE OTHER PERSON, e.g. "my
manager, whose priorities are..."], described here: [CONTEXT]. Realistic,
not a cartoon villain, not a pushover. I play myself. Start the
conversation in character.

After 8 exchanges, stop and tell me: the one thing I said that worked,
the one thing that hurt my case, and what the first real move of the
actual talk should be.
```

## Card: The Fresh-Eyes Check

For: the final pass on anything about to matter — listings about to
publish, emails about to send, chapters about to upload.

```text
Here is the final version of [PIECE] before it goes out to [AUDIENCE]:
[PASTE]

Read it as one new reader who has never seen any earlier version and has
exactly 30 seconds. Reply with ONLY:
1. The one thing they think the piece is offering.
2. Anything that would make them stop trusting it.
3. One line that could move them to act, that isn't there yet.
```

## Building your own cards

Every card above came from three moves you can repeat:

1. **Find the recurrence.** If you have typed the *same kind* of request twice, that's a card. Name it.
2. **Extract the skeleton.** Strip all topic content; keep role lines, rules, format spec, and the "do NOT include" line.
3. **Test the blank version.** Fill the card for a *new* job and run it (Chapter 8). If it needed two extra instructions, those belong in the card.

Store cards exactly like prompts — next chapter, [Chapter 7](07-building-a-prompt-library.md), sets up the plain-file library that holds them.
