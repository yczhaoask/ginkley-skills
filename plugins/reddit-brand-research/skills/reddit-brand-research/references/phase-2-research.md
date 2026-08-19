# Phase 2 · Research: match communities and collect discussion

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

### 2. List them for the user to confirm (Gate 2)

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

Wait for confirmation. Only then start fetching.

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

**A signal without a quote doesn't count.** This is the precondition for Gate 3 — every conclusion in Phase 4 must point back here.
