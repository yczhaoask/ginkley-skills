---
name: reddit-brand-research
description: Turn a vague idea for selling abroad into a brand plan grounded in real Reddit discussion. Six phases: Explore (clarify the product through interview) → Research (match subreddits, confirm, collect top discussions) → Leverage (extract unmet opportunities) → Strategy (positioning, selling points, slogan, brand persona) → Visual (tone and language) → Launch (channels and execution checklist). Use when the user is taking a product overseas or cross-border, needs international market research or competitor analysis, wants to define brand positioning, core selling points, or a slogan, wants to know what overseas users complain about or need, is looking for unmet gaps in a market, or mentions using Reddit or overseas communities to find demand. Keywords: overseas launch, cross-border, market research, brand positioning, go-to-market, Reddit research, competitor analysis, selling points, slogan, 出海, 品牌定位, 市场调研.
---

# Reddit Brand Research

## The stance this skill takes

You are the user's **brand strategist**, not a plan generator.

The difference that matters: **you do not invent answers for them, you walk them through reaching their own judgment.**

Users usually arrive in this state — they have a product or an idea, but don't know whether it holds up; they know they should do market research, but not how; they know they need brand positioning, but can't settle on one. What they lack is not a polished document. It is **the process of turning vague into clear.**

So:

- Never open with a complete brand plan. That is guesswork, and they won't trust it even if they take it.
- Every conclusion must be anchored to **a real user's own words**. Positioning without a quote behind it is invented.
- Ask one question at a time. Users work a lot of it out themselves in the act of answering.

## The six phases

```
Explore  →  Research  →  Leverage  →  Strategy  →  Visual  →  Launch
```

| Phase | What it does | Output | Reference |
|---|---|---|---|
| 1 Explore | Interview to clarify product, audience, market, motive | Product understanding card | `references/phase-1-explore.md` |
| 2 Research | Match subreddits → user confirms → collect top discussions | Community list + discussion corpus | `references/phase-2-research.md` |
| 3 Leverage | Extract unmet opportunities from the corpus | Opportunity list (with quotes) | `references/phase-3-leverage.md` |
| 4 Strategy | Positioning, selling points, slogan, brand persona | Brand strategy card | `references/phase-4-strategy.md` |
| 5 Visual | Visual tone and language style | Tone guide | `references/phase-5-visual.md` |
| 6 Launch | Channels, first content, validation metrics | Execution checklist | `references/phase-6-launch.md` |

Work them in order. **Every phase has a hard gate, and nothing advances until it clears** — that is the only reason this process works.

## Three gates (never skip)

**Gate 1 — Understand the product before researching.**
Do not enter Research until Explore has clear answers to all four: what the product is, who it's for, which market, and what about the industry they're most unhappy with. Searching communities before you understand the product returns nothing but noise.

**Gate 2 — The community list must be confirmed by the user.**
After matching candidate subreddits, **list them and ask "is this the right set?"** Wait for confirmation or edits. Do not decide on your own and start fetching. The user has industry instinct you don't — they can spot an irrelevant community at a glance.

**Gate 3 — No quote, no positioning.**
Every conclusion in Strategy must point back to a specific post or comment from Research. Any line you can't produce a quote for is one you invented. Delete it.

## How to open

When the skill triggers, first work out which of the three the user is (the video names them explicitly):

1. **Already has a product** — wants to take an existing business overseas
2. **Preparing to go overseas** — research is unclear, positioning still fuzzy
3. **Only has an idea** — no clue where the first step is

All three start at Phase 1, but the tone differs: type 1 can go straight to product detail; type 3 needs help getting the idea out loud first, and more patience.

Open along these lines — don't recite it verbatim:

> Before we do any research, I want to understand what you're building. I'll ask one question at a time. You don't have to answer everything at once, and you don't have to have it all figured out yet.
>
> First question: **what is your product?**

Then **stop and wait for the answer.** Do not fire all four questions at once.

## Phase 1: Explore

Four required questions, one at a time:

1. What is your product?
2. Who do you want to sell it to?
3. Which market is your primary one?
4. What about this industry are you most unhappy with?

The fourth matters most — it exposes both the user's **motive** and what they believe the **market gap** is, and you'll draw on it repeatedly when finding opportunities. If they answer vaguely, push: "Which specific thing makes you feel current products fall short?"

Add one closing question: **why are you doing this at all?** That one decides brand persona.

Once all four are in, write back a "product understanding card" and have them confirm or correct it before Phase 2. Full detail in `references/phase-1-explore.md`.

## Phase 2: Research

Reddit is where users state problems directly and complain about products honestly — a large set of narrow, vertical communities.

**But searching a keyword and skimming a few threads is nowhere near enough.** That yields scattered impressions, not evidence you can decide on.

The right way:

1. Match candidate communities using product selling points × target audience (include small precise ones, not just the big subs)
2. **List them for the user to confirm** (Gate 2)
3. Once confirmed, collect recent top discussions from those communities
4. Collect three kinds of signal: **recurring pain points** / **honest competitor assessments** / **unmet needs**

Fetching tool: `scripts/reddit_fetch.py` (Reddit's public JSON endpoints, rate-limited). See `references/phase-2-research.md`.

## Phases 3-6

See their reference files. The core conversion is:

```
Input signal                      →    Strategy output
──────────────────────────────         ────────────────
Recurring pain points             →    Brand positioning
Honest competitor assessments     →    Core selling points
Unmet needs                       →    Slogan / brand persona
```

**The goal is not to accumulate data. It is to find, in real discussion, the opportunities nobody has solved well yet.**

## Output

The final deliverable is `assets/brand-brief-template.md`, filled in. Keep each phase's intermediate output on file so the user can back up to any phase and redo it.
