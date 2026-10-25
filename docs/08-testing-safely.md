# Testing Prompts Safely Against a Local Model

A prompt that works once is a coincidence worth checking. A prompt that
works three times in a row on the same inputs is a tool. This chapter is
about getting to "three times, same inputs" cheaply and safely: **run your
saved prompts against a model on your own computer** — no cloud, no keys,
no data leaving the house.

## Why a local model is the right test bench

- **Nothing to leak.** Your receipts, patient-education drafts, and half-written chapters stay on your disk. Locally run means locally handled.
- **Nothing to pay.** No API key, no per-token bill. A free model, free forever.
- **Nothing to sign up for.** Install, run, done.
- **Honest variance.** Small local models show *more* variation than big cloud ones. That sounds like a downside for testing, but it is a feature: a prompt that survives a modest local model has options, not luck.

## The two-installment tour

One evening, no experience needed:

1. **Install Ollama** (or LM Studio, if you like windows instead of terminals). Both are free, offline, and beginner-friendly — the sibling book *The Local AI Handbook* covers both in detail, so here is just enough:
   - Check that your machine has at least 8 GB RAM for the small models suggested here.
   - Install from `ollama.com` (macOS/Windows installers, or a one-line Linux command), then `ollama run llama3.2` and ask it anything. That is the whole install.
2. **Install Prompt Lab** per [Chapter 7](07-building-a-prompt-library.md). Prompt Lab already talks to Ollama by default — it expects a local OpenAI-style endpoint at `http://localhost:11434/v1` with model `llama3.2`, which is exactly where Ollama lives. No key needed; Prompt Lab refuses to configure one, on principle.

You now have a prompt library connected to a bill-free test bench. Time to
actually test.

## Your first saved test run

Each prompt in your library can carry a `tests.json` — saved input lines,
one per case. Three good test inputs make most diagnoses. For the
everyday-explainer sample:

```bash
# What the sample's saved tests look like:
#   "what a token is"
#   "why the sky is blue"
#   "how to play basic chess openings"

python3 -m promptlab run everyday-explainer
```

Every saved input goes through the prompt template, hits your local model,
and you see the reply and timing for each. Two minutes to run the whole
suite. Offline the entire time.

Flag tour for the run command you'll use most:

| Flag | What it does |
| --- | --- |
| (none) | run all saved tests |
| `--input 'text'` | one ad-hoc test, ignores saved ones |
| `--dry-run` | no network: shows the rendered prompt instead |
| `--report` | also writes a Markdown run report |
| `--base-url/--model` | point at a different local server/model |

## Reading results like a friendly editor

The report (from `--report`) records version, endpoint, input, output, and
latency per test. Compare across versions and a four-row reading habit:

- **Steady format?** If all three inputs got the shape you asked for (same structure, similar length) your format spec is being followed — that was likely your earlier weak spot.
- **Any invented facts?** A local model asked about a niche topic will make things up. That is not your prompt failing; it is the model *class*. Test against the truth you pasted, not against the model.
- **Length obeyed?** If you set "one sentence," did all three answers do it?
- **Latency spikes?** Purely a local-hardware note; interesting, rarely actionable.

## Version comparisons (the pay-off move)

```bash
python3 -m promptlab run everyday-explainer --input 'why the sky is blue'
python3 -m promptlab update everyday-explainer --file v2.txt --notes 'added check question'
python3 -m promptlab run everyday-explainer --input 'why the sky is blue'
python3 -m promptlab versions everyday-explainer
python3 -m promptlab diff everyday-explainer 1 2
```

That five-line sequence is the whole "tested" story: run, tweak, re-run,
*see the difference in what changed and what it did*. No memory required,
no "wait, was the old one better?" required.

## Rules of safe testing

Local-first removes most risk, and the rest deserves the respect of these
five house rules:

1. **Test inputs are stand-ins, not your real data.** "how to refinish a pine table" instead of your grandmother's address. Every time.
2. **Placeholder, queue.** Never put real patient, client, or family details in a prompt you will save, version, or re-run. Chapter 5's cards are all shaped so your private facts stay in the *blank-filling* moment, not in the stored template. This is the one rule with no exceptions.
3. **A local model is still a model.** It datalog nothing, but it also makes things up nothing-about-your-neighborhood confidently. You are the fact-check; the test run is not.
4. **Watch the endpoint.** The endpoint you point at is the world your prompts visit. Localhost is the safest bench; if you ever point Prompt Lab at a *remote* endpoint, that is exactly the moment privacy moves — so treat the content like you're sending it to a stranger.
5. **Step up to a stronger model when stakes rise.** Drafts for personal use: llama3.2-class is fine. Anything that prints, ships, or gets read by a client: test on the biggest model you can run locally (or, if nothing bigger, accept more manual review variance).

## The weekly-ish routine

```text
1. Pick ONE prompt you used this week and wished was better.
2. Update a version with one chapter-3 tweak.                       (2 min)
3. Run its saved tests locally with --report.                       (2 min)
4. Read the report with the four-row habit. (3 min)
5. Keep or revert. Update your version note with the verdict.       (1 min)
```

Eight-ish minutes, once a week, is enough to keep a library that compounds.

## Where this leaves you

You can write (Chapters 1–4), reuse (Chapter 5), repair (Chapter 6), store
(Chapter 7), and test (this chapter) prompts as an ordinary part of life —
on your own machine, at zero cost, with your data staying home. The last
two chapters are the maintenance wing: plain-English [glossary](09-glossary.md)
and a one-page cheat sheet for the wall.
