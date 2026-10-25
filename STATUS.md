# STATUS

Project: The Prompt-Writing Handbook (missing companion to prompt-lab-cli)
Owner: Asdale Dynamics, LLC
State: complete and verified (October 2026)

## What was built

A beginner-facing manual on writing great AI prompts, written "like a friend
would": warm, plain English, never condescending — plus the tooling that turns
it into a static offline website.

- **docs/** (11 Markdown files: front matter + 10 numbered chapters):
  - `00-introduction.md` — front matter: audience, conventions, the "friend clause," a five-minute before/after experiment.
  1. Why Prompts Fail — the five failure habits (me-too, mind-reader, everything, vibe, no-examples) and the one diagnosis question.
  2. Role, Context, Format — the three-part skeleton, format tables, and "do NOT include" carve-outs.
  3. Iterate Like a Friendly Editor — the ask→diagnose→one-variable-tweak→re-run loop; when to scrap; how versioned drafts (Prompt Lab) persist the loop.
  4. Few-Shot Examples — one-shot / two-plus-one contrast examples, where examples help and where they don't.
  5. Pattern Cards — twelve fill-in-the-blank prompt recipes (Everyday Explainer, Reader-Friendly Rewrite, Tone Match, Table Builder, Pre-Mortem, Ruthless Editor, Interview-First, Study Buddy, Plain-Language Handout, Fix-My-Prompt, Role Playthrough, Fresh-Eyes Check).
  6. Before and After — six failing prompts (listing, patient teach-back, newsletter, budget, plan check, blame-the-reply) diagnosed and rewritten step by step.
  7. A Prompt Library in Plain Files — a no-tools folder system and the Prompt Lab workflow (add/update/versions/diff/meta/dry-run); library layout shown.
  8. Testing Safely Against a Local Model — Ollama + Prompt Lab in ~one evening; test runs, `--report` reading habits, version comparison, five safety rules (inputs as stand-ins, nothing private in saved prompts).
  9. Glossary — ~30 plain-English definitions.
  10. The One-Page Cheat Sheet — printable summary of the whole book.
- **scripts/pipeline.py**: standard-library-only static site builder. Zero dependencies, zero network. Produces a landing page, one chapter page per chapter with sidebar nav and prev/next pagers, a **cards.html** index of the twelve pattern cards (extracted automatically from Chapter 5 headings + "For:" lines), a single-page "whole book," and a stylesheet (light/dark aware, print styles). `00-` stems are front matter.
- **CLI flags**: build (`--docs/--out`), `--from-md FILE`, `--check` docs lint (links, anchors, duplicate headings, card completeness/count), and `--cards` (print the extracted card list).
- **tests/test_pipeline.py**: 50 tests covering the Markdown converter (headings, inline, links, lists, tasks, tables, fences, escaping), pattern-card extraction and lint rules, the site builder (including the cards page and an offline-reference check), the CLI, reproducible builds, chapter cross-reference auditing, and repo hygiene (secret-pattern scan, exact MIT LICENSE line, README credit, allowed top-level files).
- **README.md, LICENSE** (MIT, "Copyright (c) 2026 Asdale Dynamics, LLC"), **.gitignore**.

## How to run it

```bash
python3 scripts/pipeline.py            # build site/ from docs/
python3 scripts/pipeline.py --check    # lint docs (links, anchors, cards)
python3 scripts/pipeline.py --cards    # print the pattern-card list
python3 -m unittest discover -s tests  # run the test suite
```

Then open `site/index.html` in a browser — no server needed; the site makes
zero external requests, so it works offline and from `file://` (USB-stick
ready).

The companion tool (referenced throughout Chapters 3, 7, 8) is
`prompt-lab-cli` in the same workspace; its samples and commands are quoted
against its real README, with `python3 -m promptlab ...` forms matching its
no-install usage.

## Verification results (run in this folder)

- `python3 --version` → Python 3.13.5
- `python3 scripts/pipeline.py --check` → "Checked 11 markdown files: clean"
- `python3 scripts/pipeline.py` → "Built 15 files into .../site" (14 HTML pages + style.css)
- HTML structural check (html.parser tag balance over all 14 generated pages) → 0 problems
- `python3 -m unittest discover -s tests` → 50 tests, OK (0 failures, 0 errors)
- Pattern-card audit: exactly 12 cards extracted, all with a "For:" line; cards.html links resolve to real anchors on pattern-cards.html
- Reproducible-build test: two consecutive builds produce identical output manifests
- Secret-pattern scan (API keys, tokens, private-key blocks) across docs/scripts/tests/README/LICENSE → 0 matches
- Git initialized with the existing configured identity (Dylan Asdale); repo committed, nothing pushed, no remote

## Known gaps

- The book explains and quotes Prompt Lab but does not execute it; its own test suite (offline, mocked endpoints) lives in that repo. The two were verified side by side only by reading command syntax against `prompt-lab-cli`'s README and samples.
- No automated check that `site/` renders identically across browsers; structural balance + no-external-request tests are the proxy.
- The cards page is generated from Chapter 5 only. If another chapter grows card headings, `CARD_STEM` in `scripts/pipeline.py` is the single switch.
- Print styles target the whole-book and cheat-sheet pages; deeply nested tables on narrow phones may scroll horizontally (overflow-x is enabled) rather than reflow.
- No e-reader export (EPUB/PDF) yet — the one-page book.html is the stopgap for printing.
