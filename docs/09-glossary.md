# Glossary

Plain-English definitions, the way a friend would give them, in
alphabetical order. If a term confuses you here, check the chapter in
brackets for the full story.

## A–B

**API key** — A secret password that lets a program bill your cloud
account. This book's workflow uses none, on purpose; Prompt Lab refuses to
store one. [Chapter 8].

**Base URL** — The address (like `http://localhost:11434/v1`) where a model
server answers. Localhost means "this computer." [Chapter 8].

**Before/after rewrite** — A failing prompt, diagnosed and re-patched
step by step. Six live in Chapter 6. [Chapter 6].

**Blank (or slot)** — An UPPERCASE-OR-BRACKETED part of a prompt template
that you fill per use, like `[AUDIENCE]`. [Chapter 5].

**Build (site build)** — The scripts in this handbook's repo turn the
Markdown chapters into an offline HTML site. Nothing techy; you never need
it to read the book.

**Carve-out** — A "do NOT include ..." line. The underrated half of format
requests; kills unwanted disclaimers and summaries. [Chapter 2].

**Context** — What the model cannot guess: who you are, what you have, what
you already tried, what constraints matter. [Chapter 2].

## C–F

**Cloud model** — AI running on someone else's servers over the network.
Contrast: **local model**, running on your computer. [Chapter 8].

**Command line** — A terminal where you type commands. Prompt Lab is one;
it looks scary for one week and then it is just typing. [Chapter 7].

**Diff** — Side-by-side text showing what changed between two versions.
`promptlab diff my-explainer 1 2`. [Chapter 7].

**Dry run** — Rendering a prompt *without sending it* to any model.
`--dry-run`. Useful for proofreading a template with fresh eyes.

**Endpoint** — Same as Base URL. Where the requests go.

**Example (few-shot)** — A known-good sample pasted into a prompt so the
model can copy it rather than imagine one. One example is often the whole
fix. [Chapter 4].

## G–L

**Latency** — How long a reply took. In test reports it is a curiosity,
rarely an action item. [Chapter 8].

**Library** — Your folder of saved prompts and their versions. Plain files,
plain folder, yours. [Chapter 7].

**Local-first** — The house philosophy: your data and your work live on
your disk; nothing is required to send, sign up for, or key in.

**Local model** — AI running on your computer (via Ollama or LM Studio).
Safer for private material and free to run. [Chapter 8].

**Loop (the ask–diagnose–tweak loop)** — Send, diagnose in one sentence,
patch one variable, re-run. [Chapter 3].

## M–R

**Model** — Short for "language model," the AI engine. Llama 3.2 is one;
"the assistant" is how this book usually says it.

**Ollama** — Free software that runs models on your computer, popular
first-stop for local AI. `ollama run llama3.2`. [Chapter 8].

**One-variable tweak** — A revision that changes exactly ONE thing in the
prompt, so you know which change did what. [Chapter 3].

**Pattern card** — A fill-in-the-blank prompt skeleton for a recurring job,
stored with your library. Twelve ship in this book. [Chapter 5].

**Prompt** — The full text you send the model. Not just a question; the
role + context + task + format bundle. [Chapter 2].

**Prompt Lab** — The companion command-line tool for versioned prompt
libraries (`prompt-lab-cli`). Free, offline, no accounts, no keys.
[Chapter 7].

## S–V

**Template** — A prompt with blanks in it, ready to be filled. Pattern
cards are templates; so is `{{input}}` inside Prompt Lab, which means
"paste the test input here."

**Teach-back** — A patient-education technique where the patient explains
it back. Education support, never a substitute for the care team.
[Chapters 5 and 6].

**Test inputs** — Standing-in sample inputs saved with a prompt
(`tests.json`) so every version is measured on the same examples.
[Chapter 8].

**Variance** — The same prompt getting different replies on re-runs.
Bigger in local models. Why one bad reply is not automatically a bad
prompt. [Chapter 3].

**Version** — A numbered, noted snapshot of a prompt (`versions/0002.md`).
Diffing and test-running rely on versions existing. [Chapter 7].

## W–Z

**Word cap** — A hard maximum, like "under 120 words." Models are better at
*not exceeding* a cap than at hitting a target exactly. [Chapter 2].

**{{input}}** — Prompt Lab's template hole. Every test input is swapped in
there when a prompt runs. [Chapter 7].
