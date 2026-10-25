# A Prompt Library in Plain Files

Once a prompt works, you want to never lose it. The trick is embarrassingly
low-tech and quietly life-changing: **keep prompts as ordinary text files
on your own disk, versioned like code, in a folder you can back up.**

This chapter builds that habit both ways: a manual system anyone can use
with no tools at all, and the same system automated by **Prompt Lab**, the
companion command-line tool written by the same folks who made this book
(Asdale Dynamics, LLC — hi, Dylan here, I wrote both).

## Why plain files beat "I'll just scroll back"

Scrolling an old chat to find a prompt is not a library; it is an attic.
Plain files win because they are:

- **Yours.** Nothing syncs, phones home, or expires. Copy the folder, own it forever.
- **Searchable.** Ctrl+F works across everything, in any editor.
- **Versioned.** You keep every draft, so you can see what changed — and so a "worse" tweak is a fifth, not a catastrophe.
- **Portable.** Move them to a new computer with a USB stick. Open them in any editor on any OS, forever.

## Option A: the no-tools version

Any folder + your text editor + light discipline:

```text
prompt-library/
  _why-these-exist.md      <- two lines, for future you
  ask-the-doctor-questions.md
  ebay-listing-lead.md
  handout-plain-english.md
  listing-lead-v1.txt
  listing-lead-v2.txt  ...
```

Two small rules make Option A work:

1. **One prompt, one file**, named for the job: `listing-lead.txt`, not `stuff.txt`.
2. **Version history goes at the BOTTOM of the file**, as notes to yourself:

```text
--- history ---
v2: added "do not invent condition words" (reply stopped making up flaws)
v1: first draft, from rewrite 1 in the handbook
```

That two-line history habit is the whole skill. Six months from now,
"added the no-invention line" is a map of your own thinking.

## Option B: Prompt Lab (the same idea, automated)

Prompt Lab is a small, free, offline **command-line tool for versioned
prompt libraries**. Python 3.10 or newer; no third-party packages; no
account; no API key — it is designed for local servers and refuses any
config that includes a key.

Setting it up takes one minute:

```bash
python3 -m promptlab init --samples   # creates ~/.promptlab with 3 sample prompts
python3 -m promptlab list             # see what came in the box
```

The samples come with saved versions and test inputs, so you can watch
the full workflow before writing anything of your own.

### Saving and improving a prompt

```bash
echo 'Explain {{input}} in one friendly sentence.' \
  | python3 -m promptlab add my-explainer --tags writing,beginner --notes 'first try'

# ...later, after your diagnosis-tweak loop:
python3 -m promptlab update my-explainer --file v2.txt --notes 'ended with a check question'
```

Notes travel with each version, so `promptlab versions my-explainer` reads
like a changelog you wrote to your future self — Option A's bottom-of-file
history, done for you.

### The daily-ish commands

| You want to... | Run |
| --- | --- |
| See everything | `promptlab list` |
| Filter | `promptlab list --tag writing` |
| Read a prompt | `promptlab show my-explainer` |
| Read an old version | `promptlab show my-explainer 1` |
| See what changed | `promptlab diff my-explainer 1 2` |
| Save an ad-hoc test without sending | `promptlab run my-explainer --input "..." --dry-run` |

(`--dry-run` renders the prompt and shows what *would* be sent — a nice
place to proofread templates before anything goes near a model.)

### Where it all lives

```text
~/.promptlab/
  config.json              # endpoint defaults (base_url, model)
  prompts/
    my-explainer/
      meta.json            # description, tags, version notes
      versions/0001.md     # every version's full text, numbered
      versions/0002.md
      tests.json           # saved test inputs, one per line (optional)
```

Plain files all the way down. Back up the folder, sync it your way, open
`versions/0002.md` in Notepad — it is all just text. A different library
folder per project works too: `--library DIR` handles it.

### Fixing tags and descriptions without new copies

```bash
promptlab meta my-explainer --add-tag beginner --description 'patient-teacher explainer'
```

Small housekeeping, no new version: version bumps are for the *prompt
text*, not the metadata.

## The 80/20 of library habits

- **Save on exit, not on save-everything.** Add only prompts you have *used twice*. The other kind grows faster than you can prune it.
- **Name for the job, not the trick.** `handout-plain-english` beats `super-role-prompt`.
- **Notes are for your diagnosis.** Write the one-sentence diagnosis from Chapter 3, in the words you'd use.
- **Sort by area of life**, not by date: work, family listings, study, house admin. Future you knows the context, not the calendar.

## What versioning gives you later

Once versions exist, `promptlab diff` becomes a proper editor's view, and
Chapter 8's tester becomes the differentiator: run versions 1, 2, and 3
against the *same* saved test inputs and compare by behavior, not vibes.
That is the join between this chapter and the next one.

Continue with [Chapter 8](08-testing-safely.md).
