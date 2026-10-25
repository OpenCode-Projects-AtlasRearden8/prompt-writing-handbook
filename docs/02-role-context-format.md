# Role, Context, Format: the Three-Part Skeleton

Nearly every strong prompt in this book is some arrangement of three parts.
You can fix most failing prompts by asking three small questions:

1. **Who should the model be?** (role)
2. **What does the model need to know?** (context)
3. **What should the answer look like?** (format)

That is it. That is the skeleton. Everything else — honesty hints,
few-shot examples, length caps — hangs off of these three.

## The skeleton in one glance

```text
[ROLE] You are a ...                             <- who
[CONTEXT] I am ... / Here is the material ...     <- what the model must know
[TASK] Do this one job ...                       <- the single job
[FORMAT] Reply as ... ; do NOT include ...       <- the shape
```

You do not need the bracket labels in a real prompt — write it as flowing
sentences — but keep the parts distinct in your head. Here is a filled-in
example, a nurse drafting a patient-education handout (education only — the
model never makes clinical decisions):

```text
You are a plain-English patient educator (role).
I am an RN at a small clinic. Our patients often have a 6th-grade
reading level, and English is a second language for some. Here is the
material I must cover, straight from the drug sheet the pharmacist gave
me: (context + pasted text)
TASK: Rewrite it as a half-page handout with the three questions my
patients actually ask.
FORMAT: Three short sections, each with a 1-line heading; bullets with 6
to 10 words max; no jargon without a following phrase that explains it.
Leave out anything about dose changes — the pharmacist handles that.
```

One paragraph of setup, and the reply is on your page instead of needing
three rounds of re-asking.

## Part 1: Role

A role is a costume for perspective. "You are a tax-exemption researcher
writing for small resellers" primes different habits than "You are a witty
copywriter." Roles help because they compress hundreds of assumptions into
five words.

Rules of thumb:

- **Specific beats grand.** "Experienced grant reviewer for small nonprofits" produces deeper work than "expert in everything."
- **Role changes voice, not truth.** A "friendly doctor" role sounds better; it does not make the facts better. Never let a role costume instruct you on safety-critical matters (health, law, money).
- **One role per prompt.** "You are a scientist AND a comedian AND a CEO" muddles the voice. Pick the one that matters for this job.

Small role swaps you can feel:

```text
"Explain tokens to me."
"Explain tokens to me. You are a friendly librarian who has taught fifty
beginners, uses zero jargon, and checks the reader's understanding with
one small question at the end."
```

## Part 2: Context

Context is everything the model cannot guess: **who you are, what you
already have, what you already tried, and what constraints matter.** This is
the part people skip most, because to you it is obvious. To the model it is
invisible. Write the obvious.

Context worth writing, when it applies:

```text
- Nobody: who the output is for (audience, reading level, language)
- Goal: what success looks like (what you'll do with the output next)
- Materials: pasted raw text, notes, a sample, last week's version
- History: "I already tried X; it came out too formal"
- Constraints: real limits (one page, apartment kitchen, $15 total, must avoid dose changes)
```

A nugget worth taping to your monitor: **the model can only average your
situation. You have to hand it the situation.** A line of context is worth
ten rounds of re-asking.

Two techniques that stretch this part:

- **Batch materials as blocks.** Paste raw source between markers: `---NOTES START---` ... `---NOTES END---`. Keeps the model from blending your notes with its own opinions.
- **State what to IGNORE.** "The last paragraph of the notes is outdated; skip it." Models are polite, not psychic.

## Part 3: Format (and "leave out")

Format is a spec, in words, of the shape you want. The magic is in
**positive shape plus negative carve-outs**:

```text
FORMAT: numbered checklist, one step per line, 12 words max per step.
DO NOT include: a disclaimer, a closing summary, an apology, or
the words "furthermore" and "delve".
```

Format entries that consistently pay off:

| You want | Say it like this |
| --- | --- |
| Structure | "numbered list, 5 items, one line each" |
| Voice | "plain English, no corporate speak, contractions welcome" |
| Length | "under 120 words total" (counting is a model weakness; give a *cap*, not a target) |
| Structure you hate | "no headings, no closing summary, no 'here's your list'" |
| Names | "call the reader 'you'. Never say 'users'" |
| Rigor | "if you are not sure, say 'I'm not sure' — do not guess" |

The **negative carve-outs** ("do NOT ...") are the most underrated part of
format. Models over-offer: summaries, caveats, closing remarks, apologetic
openers. Carve those off in the prompt and your editing time halves.

## The one-blank exercise

Fill in the blanks out loud for your current task — this is most prompts, in
twenty seconds:

```text
You are a __________ who is __________ (one habit of theirs).
I need to produce __________ for __________ (audience).
Here are my materials: __________ (paste).
Reply should be __________ (shape) and must NOT include __________.
```

Say the first three aloud. If a line is blank, that line is what the model
will default for you, and defaulting is precisely what Chapter 1 taught us
to avoid.

Head on to [Chapter 3](03-iterating-like-an-editor.md).
