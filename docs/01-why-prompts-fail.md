# Why Prompts Fail

Here is the most useful sentence in this chapter: **when a prompt fails, it
is almost never because you are bad at writing.** It is because the prompt
left something out that the model needed, or asked for something impossible,
or expected the model to read your mind.

A model is not a person who knows you. It is a very fast pattern-finisher
that has read an enormous amount of text. Give it half a pattern and it will
finish the *most likely* pattern — which may not be yours. That is not
stupidity. That is the tool working exactly as designed.

## The five failure habits

Almost every disappointing result traces back to one of these. Run your last
flopped prompt through this list and odds are you will find it instantly.

### 1. The me-too prompt

You ask the way you'd ask a friend mid-conversation, all shorthand:

```text
Weak: help me with the email
```

Help how? Which email? To whom, about what, formal or casual, long or short?
The model has no context, so it produces a generic average of every email
that has ever existed. The fix is never "try harder wording." The fix is
adding the missing context.

### 2. The mind-reader prompt

You assume the model knows your situation:

```text
Weak: write a note for my patient about her new blood pressure medicine
```

There are maybe a hundred reasonable ways to do that: reading level,
length, one drug or a class, discharge style or handout style, English or
translated... The model picks one at random. You wanted one specific thing
and asked for none of it.

### 3. The everything prompt

You pile three tasks into one breath:

```text
Weak: give me a summary, then a lesson plan, then social media captions, also what am I missing?
```

Models scramble when outputs fight for space. Each output gets a thin,
sloppy version. The fix is unglamorous: one prompt, one job. (Need three
things? Send three prompts. This is faster *and* better.)

### 4. The vibe prompt

You describe a feeling instead of a spec:

```text
Weak: make it punchy but thoughtful, you know?
```

"Vibe words" are a slot machine. Every model — and every version of the same
model — reshuffles them differently. Say the concrete thing the vibe means:

```text
Better: Keep sentences short. Cut all adverbs ending in "-ly". Start each
paragraph with the main point.
```

### 5. The no-examples prompt

You describe the format you want instead of showing it. Models copy
demonstrations far more reliably than they follow descriptions. One good
sample beats three paragraphs of instructions. Chapter 4 is devoted to this.

## The one question that saves most prompts

When a result is wrong, resist fixing the reply. Fix the *input* by asking:

> If a polite intern had answered exactly this way, what information did I leave out that they would have needed?

That one question converts "the AI is annoying" into a concrete, fixable gap
— usually context, format, or an example.

## A worked repair

Same underlying task, five prompts ago:

```text
Before: ideas for my newsletter
```

What's wrong, point by point: no topic (1), no audience (2), no length or
shape (4), no example (5). After asking the one question — "what was left
out?" — the rewrite almost writes itself:

```text
After: I send a weekly newsletter to neighborhood gardeners in Indiana.
Mostly people over 60 who grow tomatoes and herbs, some on porches not
yards. Draft five possible subjects for this week's issue, each with:
a subject line under 10 words, a friendly two-sentence opening, and one
practical tip. Here is last week's intro so you can match the voice:

"Hi neighbors — those overnight chills did not hold back, and my basil
knows it. Let's talk about what to rescue this weekend and what to let
go."
```

Same person, same newsletter. One prompt gives "what did I leave out," the
other gives "some ideas, probably."

## What failure is NOT

Keep this boundary honest, because it saves both time and feelings:

- If the output is *worse than the prompt asked for* — wrong tone when you specified wise, short when you specified brief — that is model variance. Rewriting helps; so does rerunning, or switching to a stronger model.
- If the output is *fabricated confidently* (a made-up statistic, a fake citation), that is a known model weakness. Prompts can reduce it ("say so if you are not sure; do not invent numbers") but never fully remove it.
- If the output *violates your judgment* about safety, quality, or scope, your judgment wins. The prompt is a request, not a contract.

## Where to go next

The good news: the five failure habits collapse into a much shorter list of
additions — a role for the model, context from you, a format request, an
example, and hard limits. That list is exactly the three-part skeleton of
the next chapter.

Head on to [Chapter 2](02-role-context-format.md).
