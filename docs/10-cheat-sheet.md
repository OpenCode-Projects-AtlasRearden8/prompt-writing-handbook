# The One-Page Cheat Sheet

The whole book, for the wall or the desk drawer. Print this page (the
built `site/cheat-sheet.html` prints cleanly). Every line here is a chapter
bending its knee.

## The skeleton (Chapter 2)

```text
You are a ___________ (role, specific not grand).
I am / here are ___________ (context: who, goal, materials, tried, limits).
TASK: ___________ (one job).
FORMAT: ___________ (shape + word cap).
DO NOT include: ___________ (carve-outs).
```

## The one question (Chapter 1)

> If a polite intern answered exactly this way, what information did I leave out?

Find that gap, not a better adjective.

## The loop (Chapter 3)

```text
ask -> diagnose in ONE sentence -> patch ONE thing -> run again -> save if better
```

Three one-variable tweaks in a row each made things worse? Scrap and rewrite fresh.

## Showing beats telling (Chapter 4)

- One good example pins style, format, and length at once.
- Two examples that differ in wording but match in structure teach structure.
- One deliberately bad example, labeled "do NOT copy this," nails down the list.
- No example yet? Then say the rules first — and expect to revise.

## Naming the moves (Chapters 2, 4, 6)

- Feed reality: real notes, real receipts, real past work.
- Forbid invention: "use ONLY what's pasted; if not sure, say so."
- Word caps: "under 120 words" beats "be concise."
- Carve-outs: no disclaimers, no closing summary, no "delve."

## Twelve cards to remember (Chapter 5)

```text
Everyday Explainer     Reader-Friendly Rewrite     Tone Match
Table Builder          Pre-Mortem                  Ruthless Editor
Interview-First        Study Buddy                 Plain-Language Handout
Fix-My-Prompt          Role Playthrough            Fresh-Eyes Check
```

All fill-in-the-blank skeletons live in the pattern cards chapter.

## Library habits (Chapter 7)

- Save prompts you have used twice; skip the one-offs.
- Name for the job: `handout-plain-english`, not `stuff2final`.
- Every version gets a one-line note: the diagnosis that led to the change.
- Prompt Lab in one line:

```bash
python3 -m promptlab update my-prompt --file v2.txt --notes 'added word cap'
```

## Testing, safely (Chapter 8)

```bash
python3 -m promptlab run my-prompt --report   # local model, saved inputs
```

- Local model = free bench; nothing leaves your machine.
- Inputs are stand-ins; never real (patient/client/family) data in saved prompts.
- Read results on four rows: format held? facts invented? length obeyed? latency?

## Boundaries, kept

- AI output is a draft for a human, not advice. Education support, never medical or other regulated advice; your care team, lawyer, or accountant decides.
- Your judgment outranks the model.
- When it stays wrong after a fair loop: different model, different task, or goodbye.

---

*The Prompt-Writing Handbook — a plain-English companion to Prompt Lab,
from Asdale Dynamics, LLC. Like a friend would explain it.*
