# The Prompt-Writing Handbook

A plain-English manual for writing great prompts — the missing companion to
**Prompt Lab** (`prompt-lab-cli`), the versioned prompt library tool. Written
the way a friend would explain it: warm, step by step, never condescending,
never in a hurry.

Published as a free resource by [Asdale Dynamics, LLC](https://dylanasdale.github.io),
the beginner-friendly AI education project of author Dylan Asdale
(*The Massive AI Manual*).

## What is inside

- **docs/** — the handbook itself, one Markdown file per chapter. `00-introduction.md` is front matter ("Read This First"); the numbered chapters run 1–10:
  1. **Why Prompts Fail** — the five failure habits, and the one question that saves most prompts
  2. **Role, Context, Format** — the three-part skeleton plus the underrated "do NOT include" carve-outs
  3. **Iterate Like a Friendly Editor** — ask → diagnose in one sentence → patch one variable → re-run
  4. **Few-Shot Examples** — show, don't tell; one good sample beats a paragraph of instructions
  5. **Pattern Cards** — twelve fill-in-the-blank prompt recipes (explainer, table builder, pre-mortem, handout...)
  6. **Before and After** — six failing prompts, diagnosed and rewritten step by step
  7. **A Prompt Library in Plain Files** — save once, never lose it; no-tools version and the Prompt Lab version
  8. **Testing Safely Against a Local Model** — free test bench, no keys, inputs as stand-ins, honesty about variance
  9. **Glossary** — every term, in plain English
  10. **The One-Page Cheat Sheet** — the whole book for the wall

- **scripts/pipeline.py** — a standard-library-only static site builder. It turns the chapters into a polished, offline-friendly HTML site: chapter pages, a landing page, a **pattern-cards index page** (extracted automatically from Chapter 5), and a single "whole book" page ready to print or Ctrl+F.
- **tests/** — unit and integration tests for the converter, builders, CLI, docs lint, and repo hygiene.
- **site/** — the generated site (built locally; not committed).

## Quick start

Read the book as plain text:

```bash
less docs/00-introduction.md
```

Build the static site (requires Python 3.9+, nothing else):

```bash
python3 scripts/pipeline.py
```

Then open `site/index.html` in any browser. Works with no web server and no
network: the site makes zero external requests.

Handy extras:

```bash
python3 scripts/pipeline.py --check      # lint the docs (links, anchors, cards)
python3 scripts/pipeline.py --from-md docs/09-glossary.md   # one chapter as HTML
python3 scripts/pipeline.py --cards      # print the extracted pattern cards
xdg-open site/book.html                  # the whole book, one page, printable
```

## Run the tests

```bash
python3 -m unittest discover -s tests -v
```

All tests pass on Python 3.13; the code avoids anything newer than Python 3.9 syntax.

## The companion tool

This handbook is the *writing* half of a pair. The *saving and testing* half
is **Prompt Lab**, a free, offline command-line tool for versioned prompt
libraries:

```bash
python3 -m promptlab init --samples       # library with sample prompts
python3 -m promptlab run my-explainer --input "what a token is"
```

Prompt Lab saves every version with notes, diffs any two versions, and runs
saved test inputs against an OpenAI-compatible endpoint — defaulting to
Ollama on your own machine. It never asks for an API key, because local,
self-hosted, no-accounts is the whole point. The book's Chapters 7 and 8
teach that workflow in detail.

## House rules

- **Local-first.** No accounts, no keys, no telemetry, no network calls in the tooling or the site. Readable from a USB stick.
- **Never condescending.** No step is "obvious." If a section confuses you, that is a bug in the book.
- **Education only.** The medical-flavored examples teach prompt writing; they are never medical, legal, or financial advice, and prompts that touch that line say so inside themselves.

## Authoring notes

Chapters follow a small set of conventions enforced by `pipeline.py --check`:

- Each chapter starts with a `# Title`.
- Internal links point at `.md` files, optionally with `#anchor`; they are rewritten to the built HTML automatically and validated.
- Pattern-card headings in the cards chapter start with `Card: ` and are followed by a "For: ..." line; the site builds a cards index page from them.
- Tables use standard GitHub-style Markdown with divider rows.
- No tabs, no nesting beyond two levels, no blank lines inside lists.

## License

MIT — see [LICENSE](LICENSE). Copyright (c) 2026 Asdale Dynamics, LLC. You may copy, adapt, and share this material freely, including commercially, with attribution.
