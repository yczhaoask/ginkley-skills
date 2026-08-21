# Evidence standards

Rules that apply in every phase. Phases 2, 3 and 4 all point here.

Every one of these exists because it was violated in a real run of this skill, and the
violation cost a round of work or produced a wrong conclusion.

## 1. Not all quotes are equal

Door 4 says "no quote, no positioning." That is necessary but not sufficient — a
marketing post is also a real quote. Grade every piece of evidence before you use it:

| Tier | What it is | How to spot it | Weight |
|---|---|---|---|
| **A · unprompted first-hand** | Someone raised the problem on their own, with nobody selling anything | Complaint in a thread about something else; no product named, or a competitor's named unkindly | Full |
| **B · prompted first-hand** | A real user, but answering a question you or someone else posed | Replies under "what do you struggle with?" | Discount — the question shapes the answer |
| **C · marketing narrative** | A real person, real words, but produced to sell | Coordinated phrasing across accounts; launch-window timing; the speaker benefits if you believe it | **Never** evidence of a pain point |
| **D · second-hand** | A summary, a screenshot, someone's recap of a source you cannot open | You are quoting a description of the thing, not the thing | Label it, or drop it |

### The two rules that follow

**Lower tier never overwrites higher tier.** If you hold a direct measurement and then
find a livelier number in a promotional post, the measurement still wins. Add the new
figure as a conflicting claim with its tier attached; do not replace.

**If you cannot open the primary source, say so in the same sentence you cite it.**
"According to a summary of X" is honest. Citing X directly when you only ever read a
summary is not, and it is the easiest way to end up quoting a superseded version.

### Tier C deserves its own warning

A marketing narrative can be *effective* and *wrong at the same time*. It offers people
a tidy reason for something they really do experience, and the reason can be false.

So a Tier C source is usable evidence of **what story is being told in this market** —
which is worth knowing, and useful for copy. It is never evidence of **why users
actually behave as they do.** Keep those two uses apart, explicitly.

## 2. Tag every quote with which side it came from

Any product with a supply side and a demand side (see Phase 1) needs every quote
labelled at the moment you collect it:

```
[demand] "I'd never pay for this when the free one works."  — u/xxx, <link>
[supply] "I stopped maintaining it because nobody paid."    — u/yyy, <link>
```

**Rules:**

- A supply-side pain never justifies a demand-side positioning claim, or the reverse.
- Phase 4 produces **one positioning per side.** If you find yourself writing a single
  positioning that serves both, you have merged two populations that do not overlap.
- When you notice you have mixed them, do not patch it — go back and re-sort the
  corpus by side. Mixed-up sides are hard to spot downstream precisely because every
  individual quote still looks valid.

## 3. Absence of evidence needs a competent search behind it

"We searched and found zero complaints about X" is only meaningful if the search
*could* have found them.

Before reporting a null result, check:

- **Would the people who have this pain use these words?** Searching
  `monetize open source` finds open-source maintainers. It cannot find a consultant
  sitting on private workflows, no matter how many results you read — that person
  never uses the phrase.
- **Would they be in this community at all?** See `references/instruments.md`.
- **Is this a thing people post about?** Some pains are felt constantly and discussed
  nowhere, because complaining about them is unflattering or professionally risky.

If any check fails, the honest finding is **"not tested,"** not **"disproved."** Write
it that way — those two get treated very differently later, and a "disproved" wrongly
recorded will quietly kill a good hypothesis.

## 4. Three-author bar, and what it does not cover

Phase 2 sets the bar for "recurring" at ≥3 different authors in different threads. Two
additions:

- **Three authors from one community is weaker than three across two.** Communities
  share vocabulary and grievances; the same view repeated inside one is closer to one
  data point than three.
- **A single quote can still matter** when it names a *mechanism* rather than a
  feeling — "I use community versions to read how they did it, not to run them" tells
  you something structural. Keep it, mark it `n=1`, and treat it as **a hypothesis to
  test, never a finding.** Write the test down.

## 5. What to write when evidence conflicts

Do not silently pick a winner. Put both in, with tiers:

```markdown
**Conflict: how big is the head of this market?**

| Source | Tier | Claim | Date |
|---|---|---|---|
| Direct scrape of the site | A | Top item shows 2,862 sold | 2026-08-17 |
| Promotional thread | C | Top item has 66 subscribers | 2026-05 |

Using the scrape. The promotional figure is three months older, hand-picked by
someone with an interest, and names different products entirely.
```

The reader needs to see that you knew about the other number and why you set it aside.
