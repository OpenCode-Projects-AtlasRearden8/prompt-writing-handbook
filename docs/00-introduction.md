# Read This First

Welcome. This handbook is about writing prompts — the text you type into an
AI chat window — and getting better results from fewer attempts.

It is written the way a friend would explain it: plain English, small steps,
no jargon left undefined. You never need to be a programmer here, and you
never need to feel silly for not knowing something. Nobody teaches this in
school; we all started from zero.

## Who this book is for

- Anyone who uses an AI chat and thinks "it almost understood me" more often than they'd like.
- Writers, small-business owners, nurses, teachers, resellers — people who have real work to do, not benchmarks to win.
- Readers of the companion tool, **Prompt Lab** (`prompt-lab-cli`), who want the *writing* half of the story to go with the *saving* half.
- Anyone who wants their prompts to live in plain files on their own computer, where nothing tracks them.

You do not need any AI account for most of this book. Nothing here requires
an API key, a subscription, or a credit card. Where the book mentions a
model, a free local one (run on your own machine) is fine.

## What you will learn

1. **Why prompts fail** — the handful of habits that cause almost every confusing result.
2. **Role, context, format** — the simple three-part skeleton that fixes most of them.
3. **Iterating like a friendly editor** — how to revise a prompt in short, sane passes instead of blaming yourself the first time.
4. **Few-shot examples** — how showing (rather than describing) gets you consistent output.
5. **Pattern cards** — twelve reusable, fill-in-the-blank prompt recipes.
6. **Before-and-after rewrites** — six real failing prompts, rewritten step by step.
7. **A prompt library in plain files** — keep every good prompt on disk, saved once, revisited forever.
8. **Testing safely** — check your prompts against a local model on your own computer, with no cloud and no keys.
9. **A glossary** — every term in the book, explained plainly.
10. **A cheat sheet** — the whole book on one printable page.

## What you need

Almost nothing:

- One open question. Think of an actual task you wanted AI to do badly. Keep it in mind and try each chapter's ideas on it.
- A text editor (Notepad, TextEdit, whatever came with your computer).
- Optional: the companion tool **Prompt Lab** (see [Chapter 7](07-building-a-prompt-library.md)) and a free local model (Chapter 8 shows how, using Ollama or LM Studio — no accounts).

## Conventions used here

- The word *model* or *assistant* means the AI you are chatting with.
- *Prompt* means the full text you send. *Reply* means what comes back.
- Blocks marked `bash` or `console` are commands you can run in a terminal.
- Blocks marked `text` inside a chapter are either a prompt to type or a fictional reply to study.
- Anything named `YOU` in a prompt example is a blank slot for your own words.
- All external links point to free, no-account resources. The book itself makes zero network requests and ships nothing to anyone.

## The friend clause

Two promises, so you know the tone is intentional and the limits are too:

1. **Never condescending.** No step is "obvious." If something in here confuses you, that is a bug in the book, not in you.
2. **Never medical, legal, or financial advice.** This book teaches *writing skills*. Health-care workers will find patient-education prompt patterns useful for drafting plain-language handouts, but every pattern here stays the education side of the line.

## A five-minute try-out

Do not take my word for anything yet. Try one micro-experiment:

```text
Weak: Tell me about chamomile tea for sleep.

Better: I'm a beginning herbalist writing a short blog post for adults
in my neighborhood who struggle to fall asleep. Write three friendly
sentences about how people have used chamomile tea for sleep, one
practical nudge to try it tonight, and one honest caution about what
research says. Plain text, no headings, no emoji.
```

Notice what changed: the second prompt says **who is asking, why, what
shape the answer should take, and what to leave out**. Everything after
this chapter is a version of that one idea, taken apart and put back
together carefully.

Start with [Chapter 1](01-why-prompts-fail.md) when you're ready.
