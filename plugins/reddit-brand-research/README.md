# Reddit Brand Research

> Turn a vague idea for selling abroad into a brand plan grounded in real social media discussion.

A Claude Code skill. It does not generate a plan for you — it **walks you to your own judgment**: clarifying the product through interview, matching and confirming communities, collecting real discussion, then converting the recurring signals into brand positioning.

**Every brand conclusion must point back to a real user's own words. Any claim you can't produce a quote for gets deleted, or sends you back to collect more.**

## Install

```
/plugin marketplace add yczhaoask/ginkley-skills
/plugin install reddit-brand-research@ginkley-skills
```

Then just say "I want to research taking my product overseas" or "help me define my brand positioning."

## The six phases

```
Explore  →  Research  →  Leverage  →  Strategy  →  Visual  →  Launch
```

| Phase | What it does | Output |
|---|---|---|
| Explore | Interview to clarify product, audience, market, motive | Product understanding card |
| Research | Match subreddits → you confirm → collect top discussions | Community list + discussion corpus |
| Leverage | Extract unmet opportunities from the corpus | Opportunity list (with quotes) |
| Strategy | Positioning, selling points, slogan, brand persona | Brand strategy card |
| Visual | Visual tone and language style | Tone guide |
| Launch | Channels, first content, validation metrics | Execution checklist |

## Five gates

The only reason this process works is that it won't let you skip steps:

1. **Understand the product before researching.** Four questions get answered before any research starts — search communities before you understand the product and everything you find is noise. If you genuinely don't know who your audience is yet, a bounded probe searches on your product description and brings back candidate populations to choose between.
2. **You confirm the community list.** Candidate subreddits get listed for you to approve or edit before anything is fetched. You have industry instinct the model doesn't.
3. **The pool has to contain your buyer.** Relevant is not the same as reachable. Before fetching: are the people who'd *pay* here, or only people discussing the topic — and is the speaker the buyer, or the buyer's customer?
4. **No quote, no positioning.** Every conclusion points back to a specific post or comment.
5. **A quote alone isn't enough.** Marketing copy is also a real quote. Every quote carries a tier — unprompted, prompted, marketing, second-hand — and for two-sided products, which side it came from. Marketing narrative never counts as evidence of a pain point.

## When Reddit doesn't work

Reddit blocks datacentre IPs hard, and some audiences aren't on it at all. The skill ships application-only OAuth support plus two fallback fetchers — Hacker News (no auth) and YouTube comments (free API key) — producing the same output shape, so the later phases don't change. It also tells you which pool reaches which population, because every source returns answers shaped like its own audience.

## The core conversion

| Input signal | → | Strategy output |
|---|---|---|
| Recurring pain points | → | Brand positioning |
| Honest competitor assessments | → | Core selling points |
| Unmet needs | → | Slogan / brand persona |

## Who it's for

1. **Already has a product** — wants to take an existing business overseas
2. **Preparing to go overseas** — research is unclear, positioning still fuzzy
3. **Only has an idea** — no clue where the first step is

## Included tooling

`skills/reddit-brand-research/scripts/reddit_fetch.py` — community discovery and post/comment collection through Reddit's public JSON endpoints. Standard library only, 2s between requests, backs off on 429.

```bash
python3 reddit_fetch.py discover --query "home improvement durable" --limit 25
python3 reddit_fetch.py fetch --subs BuyItForLife HomeImprovement \
    --timeframe year --limit 50 --comments 30 --out research/raw.json
python3 reddit_fetch.py search --subs BuyItForLife \
    --query "breaks after a year" --limit 40 --out research/pain.json
```

For heavy or commercial use, register an app and switch to OAuth per Reddit's API terms. Read a subreddit's rules before participating — posting ads outright gets you banned.

## Attribution

This methodology is not my own. It was distilled from a short video on the Chinese-language internet.

In that video the original author demonstrated a workflow tool of their own making that shares its name — this repository is not that tool, and has no affiliation with its author. What follows is an independent implementation that I wrote from the methodology as publicly described in the video.

The original video's author and link are not listed here at this time.

Note that the video explains four of the six phases in full: explore, research, leverage, and strategy. Visual and launch appear only as labels in its progress bar and are never elaborated; those two phases in this repository are reasoned extensions consistent with the rest of the methodology, and each of those files says so at the top.

If you are the original author and would like the credit adjusted, or want this taken down, please open an issue.

## License

MIT, see [LICENSE](LICENSE). The license covers the prose and code in this repository. It asserts no claim over the methodology itself.
