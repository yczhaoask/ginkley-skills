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

## The six doors are the six phases

Each phase has an exit, the exit has conditions, and **you** open it — never the model.
There's no separate list of rules to remember: if you know which phase you're in, you
know which door is next.

| Door | You leave when |
|---|---|
| **1 Explore** | The model can state your product back to you — what it is, who for, which market, what frustrates you. Can't name an audience? It runs a short probe and brings back candidates instead of guessing |
| **2 Research** | The corpus is *saturated* — the last batch of collection turned up nothing new — and it came from a pool that actually contains your buyers, not just people discussing the topic |
| **3 Leverage** | Every opportunity survives its evidence test: a real recurring pain, existing solutions missing it, and quotes that aren't someone's marketing. Then: is the direction clear, and do you want a strategy built on it? |
| **4 Strategy** | Nothing in it was invented. Every conclusion points at a specific post or comment |
| **5 Visual** | The tone came from how users in the corpus actually talk — their words, not the model's taste |
| **6 Launch** | It can be checked against reality: real channels, and success thresholds written down *before* the test, so a weak result can't be talked up afterwards |

## How each door works

The phase delivers its output on its own, then asks two things: is anything unclear,
wrong, or worth redirecting — and is this step settled enough to move on? Those are
separate questions, and neither silence, nor interest, nor "you answered everything"
counts as a yes.

Findings and conclusions never arrive together: handed both at once, anyone skims the
evidence and reads the conclusions, which is exactly backwards.

Inside a phase it just works — no check-ins between searches.

## It offers you the report at the end

When the sixth phase clears it raises the final brand plan itself, rather than leaving
you to ask — what format (Markdown, HTML page, Word, PDF, slides), and full depth with
every supporting quote or a short version. Markdown always works; the rest depend on
what your environment has installed, and it will tell you rather than quietly producing
something lesser. Leaving it as separate per-phase notes is a valid answer too.

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
