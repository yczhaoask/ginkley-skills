# Instruments: picking one, checking it reaches, and what to do when it fails

Reddit is this skill's primary instrument, and usually the right one. This file covers
the two situations the rest of the skill assumes away: **Reddit cannot be reached**, and
**Reddit is reachable but the people you need are not in it.**

The second is the more dangerous of the two, because it produces plenty of output.

## 1. Every instrument returns answers shaped like itself

A community does not just host opinions — it selects who shows up and what register
they speak in. Run the same question through four pools and you get four different
answers, none of them wrong, all of them partial:

| Pool | Who is actually there | What it is good for | What it will never give you |
|---|---|---|---|
| **Reddit** | Semi-anonymous enthusiasts and practitioners, by narrow interest | Unprompted complaint, honest competitor talk | Enterprise buyers; anyone whose employer forbids posting |
| **Hacker News** | Technical readers, builders, long-form arguers | Reasoned argument, historical perspective | Non-technical buyers; anything consumer |
| **YouTube comments** | Learners, beginners, hobbyists, the price-sensitive | Reaction at volume; what confuses beginners | Purchase intent — people are there to learn, not shop |
| **X / search-indexed** | Whoever got amplified | Competitor narratives, launch messaging | Long-tail organic complaint; anything not amplified |
| **Trade press & professional forums** | Practitioners in regulated work | Purchasing criteria, compliance requirements | Volume, and candour about their own failures |

**The failure this table prevents:** running two rounds against the same pool with
different keywords, getting the same shape of answer twice, and concluding the answer is
robust. It was the instrument talking, not the market. If two rounds in one pool
disagree with your hypothesis in the same way, change pool before you change conclusion.

## 2. The reach test

Run this **after** the user confirms the community list and **before** you fetch
anything. Three questions, answered out loud:

1. **Are the people who would buy this actually in these communities?**
   Not people who *talk about the topic* — people who would **pay**.

2. **Is the speaker the buyer, or the buyer's customer?**
   A classic miss: researching AI for law firms and finding threads full of people
   angry at their lawyers' fees. Real, vivid, high-engagement, and the wrong side of
   the market entirely.

3. **Which side of the product is this pool on?**
   For a two-sided product, name it now — supply or demand — and carry the label
   through collection (see `references/evidence-standards.md`).

If any answer is unclear, **say so to the user before spending a round**:

> Before I collect from these: I think this set reaches <population>, but the people
> who'd actually pay look more like <other population>, who are probably in
> <other place>. Do you want me to run this anyway as a cheap first pass, or switch?

A round costs real time. One paragraph of doubt beforehand is cheap.

## 3. Preflight before every collection run

Never launch a batch without checking the tool works first. Confirm three things:

```bash
# 1. Reachable, and returning data rather than a block page
python3 scripts/reddit_fetch.py fetch --subs test --limit 1

# 2. Non-empty. A script that writes empty files and exits 0 is the worst
#    outcome — you will not notice until you try to analyse nothing.

# 3. Exit code is 0
echo $?
```

A fetcher that fails silently costs more than one that crashes. If a tool returns
nothing, it must say why — HTTP status, response body, the URL it called — and exit
non-zero. `reddit_fetch.py` behaves this way; hold any tool you add to the same bar.

## 4. When Reddit is unreachable

Reddit blocks datacentre IPs aggressively. Symptoms and what they mean:

| Symptom | Meaning | Fix |
|---|---|---|
| `403` with an HTML block page | Bot detection, not an API error | Use OAuth, below |
| Connection timeout on RSS | Network path blocked | Different network, or another source |
| API app registration rejected | New accounts hit the Responsible Builder Policy | Use an established account, or another source |

**Application-only OAuth** is the sanctioned path and often works where anonymous
requests do not:

```bash
export REDDIT_CLIENT_ID=...      # reddit.com/prefs/apps -> create "script" app
export REDDIT_CLIENT_SECRET=...
python3 scripts/reddit_fetch.py fetch --subs BuyItForLife --limit 50
```

**Do not spoof a browser User-Agent to get around bot detection.** A sanctioned path
exists; evading the block instead is both against Reddit's terms and unnecessary.

If Reddit stays unreachable, **switch instrument rather than abandoning the phase** —
and record the switch, because it changes what the evidence can support.

### Fallback fetchers

Both ship in `scripts/` and produce the same output shape as `reddit_fetch.py`, so
Phase 3 onwards is unchanged:

```bash
# Hacker News — no authentication, no gatekeeping
python3 scripts/hn_fetch.py search --query "<pain point>" \
    --limit 50 --comments 25 --out research/hn.json

# YouTube — needs a free key: console.cloud.google.com,
# enable "YouTube Data API v3", create an API key
export YT_API_KEY=...
python3 scripts/youtube_fetch.py search --query "<topic>" \
    --limit 50 --comments 200 --out research/yt.json
```

Pick by who you need to reach, using the table in section 1 — not by which one is
easiest to run.

### Sources to avoid

**LinkedIn** has no API for this. All access has required partner approval since 2015,
and research and scraping use cases are explicitly excluded. Scraping it violates their
terms. If you need practitioner voice, reach it through trade publications, professional
forums, or by talking to people directly.

## 5. When no public pool reaches them

Some populations barely exist in public discussion. Regulated professionals are the
clearest case — the higher the liability attached to someone's work, the less freely
they post about how they do it.

When you hit this, **say it plainly instead of substituting a reachable population and
hoping nobody notices.** The finding is real and it is useful:

- These buyers cannot be researched by collection. They need direct conversation —
  a handful of interviews beats another ten thousand comments.
- The same wall stands in front of competitors. A market you can only learn about by
  talking to people is one where relationships, not scraping, decide who wins.

Write it into the output as a scope limit on the whole study, not a footnote.
