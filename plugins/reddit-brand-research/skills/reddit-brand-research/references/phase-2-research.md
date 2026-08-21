# Phase 2 · Research: match communities and collect discussion

## Before anything: is Reddit the right instrument here?

Reddit is the default and usually correct. It is not always correct, and it is not
always reachable. Both cases are covered in `references/instruments.md`; read it now if
either applies:

- The people who would **pay** for this may not be on Reddit at all (regulated
  professionals, enterprise buyers, anyone posting under their employer's name).
- Reddit returns `403` with a block page, or times out.

Choosing the wrong pool does not produce an error. It produces a full round of
plausible, well-quoted, wrongly-sourced findings — which is far more expensive.

## Why Reddit

Reddit hosts a large set of narrow, vertical communities where users state problems directly and complain about products honestly.

Its distinct value for overseas research: **these things are not said for a brand's benefit.** When someone complains in a community, they aren't picturing a vendor reading it — so it is far more honest than a survey or a review section.

## But searching a keyword and skimming threads is nowhere near enough

The common mistake: search a product keyword → skim two pages → read some comments → call the research done.

The problems with that:

- Keywords only hit people **already discussing the category**, missing everyone who has the pain but doesn't know a product exists for it
- A single thread is an anecdote — **you cannot tell which pain points recur**
- Without community context, you can't separate a widespread complaint from one person's preference

The right approach is to **lock down the communities first, then collect systematically inside them.**

## Steps

### 1. Match candidate communities

Search along two dimensions — cover both:

- **Category communities** — where this product class is discussed directly
- **Audience communities** — where the target users gather, even if the category isn't the topic (raw pain points often live here)
- **Context communities** — organized around the use situation
- **Business communities** — e.g. r/Entrepreneur, where you can see how peers think

**Don't only chase the big subs.** Small, precise communities have a far better signal-to-noise ratio. A 30k-member dedicated community beats a 500k-member general one.

To discover communities:

```bash
python3 scripts/reddit_fetch.py discover --query "<keywords>" --limit 25
```

### 2. List them for the user to confirm

**This step cannot be skipped.** The user has industry instinct you don't — they can spot an irrelevant community at a glance.

Format:

```markdown
## Suggested communities

| Community | Subscribers | Why this one |
|---|---|---|
| r/HomeImprovement | 2.4M | Home renovation experience, target audience gathers here |
| r/BuyItForLife | 1.1M | Durability mindset, maps directly to your selling point |
| r/Entrepreneur | 3.8M | Business perspective, shows how peers judge this |

---
Is this the right set? Anything to add or drop?
```

Wait for confirmation.

### 2b. Then run the reach test

Confirmation means the user thinks these communities are *relevant*. It does not mean
the people who would pay are *in* them. Before fetching, answer three questions out
loud — full version in `references/instruments.md`:

1. Are the people who would **buy** this in these communities, or only people who
   discuss the topic?
2. Is the speaker the **buyer**, or the buyer's **customer**? (Threads full of people
   angry at their lawyers are not law firms evaluating tools.)
3. For a two-sided product — which side is this pool, supply or demand? Write it down;
   every quote gets tagged with it.

If any answer is unclear, raise it with the user before spending the round.

### 2c. Preflight

Never launch a batch without confirming the tool returns real data and exits 0:

```bash
python3 scripts/reddit_fetch.py fetch --subs test --limit 1 && echo "exit=$?"
```

A fetcher that writes empty files and exits 0 will cost you the whole round before you
notice. Only then start collecting.

### 3. Collect recent top discussions

```bash
python3 scripts/reddit_fetch.py fetch \
  --subs HomeImprovement BuyItForLife Entrepreneur \
  --timeframe year --limit 50 --comments 30 \
  --out research/raw.json
```

Targeted search for specific pain points:

```bash
python3 scripts/reddit_fetch.py search \
  --subs BuyItForLife --query "cheap breaks replacement" --limit 40 \
  --out research/pain.json
```

### 4. Collect three kinds of signal

From the collected corpus, keep only these three. Discard the rest:

| Signal | What it looks like | What it feeds |
|---|---|---|
| **Recurring pain points** | Different people, different threads, complaining about the same thing | → Brand positioning |
| **Honest competitor assessments** | Naming a specific product and what's good or bad about it | → Core selling points |
| **Unmet needs** | "I wish something could…" / "Why does nobody make…" | → Slogan / brand persona |

**The bar for "recurring"**: at least 3 different authors, in different threads, raising the same thing. One or two is an anecdote — don't treat it as a trend.

## Output: the discussion corpus

Every signal needs **traceable original text and a link**:

```markdown
### Signal: cheap products break within two years; users would rather pay more for durability

**Type**: Recurring pain point
**Frequency**: 7 different authors / 5 threads

> "I'm done buying the cheap ones. Third one in two years."
> — u/xxx, r/BuyItForLife, 2024-03, <link>

> "I want something I can hand down to my kid, not throw away."
> — u/yyy, r/HomeImprovement, 2024-05, <link>
```

**A signal without a quote doesn't count.** This is the precondition for Door 4 — every conclusion in Strategy must point back here.

## Every quote carries a tier and a side

A quote alone is not enough — a promotional post is also a real quote. Tag each one as
you collect it, per `references/evidence-standards.md`:

```markdown
> [A · demand] "I'm done buying the cheap ones. Third one in two years."
> — u/xxx, r/BuyItForLife, 2024-03, <link>
```

- **Tier** — `A` unprompted first-hand · `B` prompted · `C` marketing narrative ·
  `D` second-hand. **Tier C is never evidence of a pain point**, however well it reads.
- **Side** — `supply` or `demand`, for any two-sided product.

Tagging at collection time costs seconds. Reconstructing it in Phase 4, when every
quote in the pile looks equally valid, is how sides get mixed and marketing copy gets
promoted to a finding.

## When is the first round actually finished?

**The first round must be exhaustive.** Everything downstream inherits its gaps, and a
gap found in Phase 4 costs the whole chain. "Be thorough" is not a usable instruction,
so here is the bar — **all five, or you are not done:**

| # | Test | Failing looks like |
|---|---|---|
| 1 | **Saturation reached.** The most recent batch produced **no new signal cluster** | Your last batch added a new cluster — collect more, you stopped mid-vein |
| 2 | **All four community types covered** — category, audience, context, business | Only category communities: you found people discussing the product, not people with the problem |
| 3 | **You searched the disconfirming vocabulary too** | Every query assumes your hypothesis. Search for the words someone who *disagrees* would use, and for the words used by people who don't know your category exists |
| 4 | **Every query is written down** in a search log | You cannot tell the user what was *not* tested, so a gap looks identical to an absence |
| 5 | **Thin results were chased, not accepted** | A community returned 3 comments and you moved on. Either it's the wrong community, the wrong words, or the wrong instrument — find out which |

**Test 1 is the one that decides it.** Keep collecting while each batch still adds new
clusters. When a batch adds only more instances of clusters you already have, you have
saturated — and only then.

### The search log

Keep it as you go; it goes out with the report:

```markdown
| Query | Where | Results | New clusters |
|---|---|---|---|
| "cheap breaks replacement" | r/BuyItForLife | 40 | 2 |
| "worth the money durable"  | r/BuyItForLife | 35 | 1 |
| "regret buying"            | r/HomeImprovement | 28 | 0 ← saturating |
```

The "new clusters" column is your saturation curve. It is also the only honest way to
answer "did you look into X?" later.

## Door 2 — hand over the findings, then stop

When the round is complete, **deliver the market signals on their own and wait.**

**Do not put the signals and the opportunities in the same message.** Given both at
once, a reader goes to the opportunities and skims the evidence — which defeats the
review entirely, because the opportunities are exactly what the evidence is supposed to
be checked against. The user is the only person who can tell you that a finding
contradicts something they know about their own industry, and they will only do that if
they read the findings while nothing else competes for their attention.

The full protocol — including what does *not* count as a yes — is in
`references/phase-handoff.md`. The sequence here is strictly:

```
message 1  →  market signals + search log  →  WAIT for the user
                                                    ↓
                                        their corrections and questions
                                                    ↓
message 2  →  opportunities (Phase 3)
```

**Message 1 ends with these questions.** Ask them plainly, and mean them:

> Before I turn this into opportunities, I want you to check the findings:
>
> 1. **Is anything here you don't understand or don't believe?** Tell me and I'll show
>    you the original discussion, or go back and verify it.
> 2. **Does anything contradict what you know about this industry?** If it does, you're
>    probably right and my sample is probably wrong — say what's off.
> 3. **Is there something I should have looked into and didn't?** Here's what I
>    searched *(search log)* — anything missing?
> 4. **Do you want to redirect any of this?** A community to add or drop, an angle to
>    dig into further, something to stop pursuing.

5. **Do you feel this has been covered thoroughly enough? Can I move on to turning it
   into opportunities?**

Then **stop.** Do not offer a preview of the opportunities, do not say "my initial read
is…" — that pre-frames their answer and you lose the independent check.

Questions 1–4 invite correction; question 5 asks permission. **Answering 1–4 is not
permission** — when the last question is resolved, ask 5 again on its own.

**If the answers change anything material — a wrong community, a missing angle, a
finding they can refute — go back and collect again before Phase 3.** A second round
here is cheap. Discovering it in Phase 4 means redoing the positioning.

## If you found nothing

Before writing "no evidence of X," check that your search *could* have found it — the
wrong vocabulary can only ever return the wrong population. See section 3 of
`references/evidence-standards.md`. The honest finding is usually **"not tested,"** not
**"disproved."**
