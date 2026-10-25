# Few-Shot Examples: Show, Don't Tell

Some old magic, with a fancy name. "Few-shot" just means **giving the model
one or more worked examples inside the prompt** — like showing a new hire a
finished report from last month instead of describing last month's report.

Describing is good. Showing is better. Describe *and* show, and most of the
guessing stops.

## Why showing beats telling

Models copy patterns. Asking for "a funny subject line" is asking the model
to imagine your sense of humor from three words. Asking with:

```text
Funny subject line example: "Chest freezer update: the mystery burrito
has been identified"
```

...now the model has your humor, your length, your topic mix. You just
handed it a drawing instead of a description — the same information,
twice as reliable.

Three reasons examples are the single highest-paid tweak in this book:

1. They pin down style **and** content **and** format at once.
2. They survive re-rolls — the same example keeps steering each new reply.
3. They are *cheaper* to write than format instructions. One good sample is shorter than the paragraph of instructions it replaces.

## One example changes everything (the one-shot)

Paste one known-good example, then mark exactly where the new work starts:

```text
Rewrite my listing titles in this style. Here is one I liked:

eBay example: "Vintage Pyrex Butterprint Casserole 1.5Q, lid, no
chips, tested oven-safe"

Now write 5 titles in the same style for: a lot of 6 vintage ladles,
some tarnished. Same structure: item name, quantity, short condition
note. No all-caps shouting.
```

That example is doing the work of four instructions (include condition,
include size, casual-but-precise voice, no hype). One paste, four fixes.

## Two or three examples (few-shot proper)

When output needs consistency — a bulletin repeated weekly, real labeling
work, handout classes — take two or three examples, not five. More is
not better; past two or three, small local models get bored and drift
toward blending them. The sweet spot, again:

```text
Example 1 (good): ...
Example 2 (good): ...
Example 3 (bad, for contrast): "..."   <- skip this mistake
```

That third slot — a deliberately wrong example, labeled wrong — is the
sneakiest tool in the kit. Models rarely need a full bad/good analysis;
they just see "!" — "do NOT do this."

Label your examples like the above. Plain "Example 1 / Example 2 / Do not
copy this" prompts let the model's natural pattern-learner shine.

## Where examples shine the most (and least)

| Best for examples | Weak fit |
| --- | --- |
| Formats with house rules (listings, notes, handouts) | Fresh creative work with no house style |
| Repetitive labeling / classification work | One-off questions, research |
| Voice-fixing, rewriting to match your tone | Anything where you can't yet say what "good" looks like |

That last row is the honest boundary: **if you cannot yet produce a "good"
example yourself, few-shot cannot save you.** You either get good by
iterating (Chapter 3), or by finding one decent sample somewhere and
starting from it.

## Where do the examples come from?

Three honest sources, in order:

1. **Your own past work.** The email you actually sent, the handout you actually made. Highest quality, zero fabrication risk.
2. **Your revision history.** If you use Prompt Lab (Chapter 7), the version notes become a mini-album of what you improved — often enough to seed example 1 for the next prompt.
3. **Asking the model itself.** "Give me two versions of what such a reply might look like; I'll pick the good one and use it as my example." Fine when you are starting from zero — just remember to keep editing. The model's idea of "good" or "seller voice" is *a* style, not necessarily *your* style.

## Example slotting discipline

Three habits that keep examples from backfiring:

- **Keep examples short.** Your example is a dollhouse of the output, not the mansion. 1–3 lines beats 8.
- **Differentiate.** Two identical examples teach "the exact wording matters"; two *differently-worded but structurally matched* examples teach "this structure matters, wording varies."
- **Match the task you're actually sending.** If your example is a blog voice but the task is a table, the model blends two formats into sludge.

## The two-sentence recap

One example pins the whole job. Two pinned examples plus one labeled "bad"
example nail it down. This is *also* why Pattern Cards (next chapter) hand
you an example slot: the practice in this chapter is exactly the blank in
every card template.

Continue with [Chapter 5](05-pattern-cards.md).
