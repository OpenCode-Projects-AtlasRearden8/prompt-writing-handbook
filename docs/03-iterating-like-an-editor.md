# Iterate Like a Friendly Editor

Here is the secret: **good prompts are written the way good drafts are — by
revising, one small pass at a time.** Nobody nails the first try, including
the people who write AI documentation for a living. If you get a mediocre
reply, you were not wrong. You *learned*, the same way an editor learns from
a first reading.

This chapter gives you a revision loop that is kind to beginners, kind to
your schedule, and immune to that sinking "copy-rewrite my prompt from
scratch" feeling.

## The loop: ask, diagnose, tweak, export

```text
1. ASK       send a first-draft prompt
2. GLANCE    read the reply as an EDITOR, not as a stranger
3. NAME      one-sentence diagnosis: what's missing or off?
4. TWEAK     patch ONE thing in the prompt (not the reply)
5. KEEP      if the result improved, save the prompt (Chapter 7)
```

That loop is the whole chapter. The rest is teaching you how to do steps 3
and 4 well, because "tweak" done naively ("make it better!") is just copying
and pasting.

## Step 3, the diagnosis sentence

Editors write marginal notes like "needs sources here," not "bad." Practice
the one-liner. Put your finger on the exact bit that is off:

- "Reply is too formal for a neighborhood newsletter" — that's a **voice** diagnosis.
- "It answered the question I didn't ask and skipped the one I did" — that's a **task focus** gap: add the one-line task.
- "It froze after 2 sentences" — that's a **length** spec: give a range (or a direction) instead of nothing.
- "Made up a discount that doesn't exist" — that's a **fabrication** issue: add "don't invent offers, only use what's in the notes."
- "It says 'delve' four times to please me" — that's a **tell**: a phrase clipping or fad it can't shake; add a carve-out.

Diagnosis as a writing skill is exactly why "iterate like a friendly
editor" works. An editor says *what* failed, in a fit-into-a-column
footnote.

## Step 4, the one-variable tweak

The strongest tweak is one that changes exactly ONE thing. Give yourself the
guillotine: any tweak that touches more than one variable is too much. If
you batch five changes, you will not know which one helped (and that lesson
is for free from second grade onward — what did your science teacher call
it? yes, *variables*).

Common one-variable tweaks. Pick one, run, move on:

| It came out too... | Your single tweak |
| --- | --- |
| Formal | add "contractions welcome" or "write like you talk" |
| Fluffy | add "no adverbs ending in -ly" or "cut every sentence that doesn't change my mind" |
| Long | give a word cap: "under 120 words" |
| Repetitive | add "each point must be *different in kind*, not reworded" |
| Vague | add one concrete example of a good answer (Chapter 4) |
| Wrong audience | add one line: "the reader is __________" |
| Pavlovian "delve" | add a carve-out list of banned filler phrases |

The tweak-don't-debate rule: **the reply is evidence, not a dare.** When a
computer writes something you like by accident, do not treat the reply as
the treasure — treat it as feedback about what your prompt was missing.
The *prompt* is the durable thing; that's why Chapter 7 asks you to save it,
not the output.

## When to scrap instead of patch

The loop has one honest exit: an "official" rewrite-from-scratch
occasionally helps. Two signals say scrap:

1. Three one-variable tweaks in a row each made a *different* part worse (a prompt tug-of-war).
2. You cannot write the one-sentence diagnosis; the reply isn't "wrong," just... nothing.

Scrapping is a five-minute reset, not a failure of the loop.

## Small loop for the hands-on type: use versioned drafts

You will not always be in a chat window. When you build up real prompts and
save them, the ask-tweak loop becomes concrete — every version gets a note:

```bash
# First draft — the "worked in the moment" version
echo 'Explain {{input}} to someone who never used AI, one short paragraph.' \
  | python3 -m promptlab add explainer --notes 'first draft'

# read the reply, one-sentence diagnosis: needs a check of understanding

echo 'Explain {{input}} to someone who never used AI. One short paragraph,
plain English, end with a one-line check of understanding.' \
  | python3 -m promptlab update explainer --file v2.txt --notes 'added check question'
```

That is the loop, persisted. And `promptlab diff explainer 1 2` shows your
own writing improving, which is honestly a nice thing to see.

(How to install Prompt Lab and where that library lives: [Chapter 7](07-building-a-prompt-library.md); actually testing against the model: [Chapter 8](08-testing-safely.md).)

## Cold rolls: when the prompt is fine

Sometimes the prompt is *fine* and you simply got a bad roll. Two resets, in this order:

1. **Send it again.** Local models roll the dice each run; a fresh run is
   sometimes simply a warmer chair.
2. **Slightly reword one pivotal phrase.** Then re-run.

Not everything weak deserves a full revision pass. But if a prompt goes
*consistently* wrong across reruns, it is a real deficiency in the prompt.
Patch it.

## The friendly homework

Take your latest mediocre chat exchange and do this in five minutes:

1. Write the one-sentence diagnosis (Step 3). If you can't, skip to the scrap rule.
2. Make exactly one one-variable tweak (Step 4).
3. Send it again.
4. Say out loud whether the reply is a B-, B, or B+. That tiny numeric push
   will inform every chapter from here on, because iteration quality is 
   a *skill you can hear in your own diagnosis voice*.

Next goes deeper into the one tweak above that pays best of all — showing,
not telling, with examples: [Chapter 4](04-few-shot-examples.md).
