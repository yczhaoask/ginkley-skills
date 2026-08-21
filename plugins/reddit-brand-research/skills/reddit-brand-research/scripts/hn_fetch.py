#!/usr/bin/env python3
"""Fetch Hacker News discussion via the Algolia API.

A drop-in alternative source when Reddit is unavailable. No authentication,
no User-Agent gatekeeping, generous rate limits. Standard library only.

Output shape matches reddit_fetch.py so the same analysis applies.

  search   relevance-ranked stories for a query
  recent   date-ranked stories for a query
  comments fetch full comment trees for stories already collected

Examples:
  python3 hn_fetch.py search --query "monetize open source" \
      --limit 50 --comments 25 --out out/h1_monetize.json
  python3 hn_fetch.py recent --query "sell prompts" --limit 40 --out out/x.json
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://hn.algolia.com/api/v1"
UA = os.environ.get("HN_UA", "reddit-brand-research/0.1 (market research)")
DELAY = float(os.environ.get("HN_DELAY", "0.5"))
MAX_RETRY = 4
FAILURES = []


def get(url, params=None):
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    for attempt in range(MAX_RETRY):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                time.sleep(DELAY)
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503):
                back = DELAY * (2 ** attempt) + 1
                print(f"  {e.code} — backing off {back:.1f}s", file=sys.stderr)
                time.sleep(back)
                continue
            body = ""
            try:
                body = e.read().decode("utf-8", "replace")[:200]
            except Exception:
                pass
            print(f"  HTTP {e.code}: {url}\n    {body}", file=sys.stderr)
            FAILURES.append((url, f"HTTP {e.code}: {body[:120]}"))
            return None
        except Exception as e:
            print(f"  {type(e).__name__}: {e}", file=sys.stderr)
            time.sleep(DELAY * (2 ** attempt))
    FAILURES.append((url, "exhausted retries"))
    return None


def _story(h):
    oid = h.get("objectID")
    return {
        "id": oid,
        "source": "hn",
        "community": ", ".join(h.get("_tags") or []),
        "title": h.get("title") or h.get("story_title") or "",
        "author": h.get("author"),
        "score": h.get("points") or 0,
        "num_comments": h.get("num_comments") or 0,
        "created": (h.get("created_at") or "")[:10],
        "selftext": (h.get("story_text") or h.get("comment_text") or "")[:4000],
        "url": h.get("url") or "",
        "permalink": f"https://news.ycombinator.com/item?id={oid}",
        "comments": [],
    }


def _flatten(node, out, limit):
    """Depth-first walk of an Algolia item tree, collecting comment text."""
    for c in node.get("children") or []:
        if len(out) >= limit:
            return
        text = c.get("text")
        if text and c.get("author"):
            out.append({
                "author": c.get("author"),
                "score": c.get("points") or 0,
                "created": (c.get("created_at") or "")[:10],
                "body": _strip(text)[:2000],
                "permalink": f"https://news.ycombinator.com/item?id={c.get('id')}",
            })
        _flatten(c, out, limit)


def _strip(html):
    """Algolia returns comment bodies as HTML. Reduce to readable text."""
    import html as _h
    import re
    t = re.sub(r"<p>", "\n\n", html)
    t = re.sub(r"<[^>]+>", "", t)
    return _h.unescape(t).strip()


def fetch_comments(story_id, limit):
    d = get(f"{BASE}/items/{story_id}")
    if not d:
        return []
    out = []
    _flatten(d, out, limit)
    return out


def _search(path, query, limit, n_comments):
    print(f"[{path}] {query!r}", file=sys.stderr)
    d = get(f"{BASE}/{path}", {
        "query": query, "tags": "story", "hitsPerPage": min(limit, 100),
    })
    if not d:
        return []
    stories = [_story(h) for h in d.get("hits", [])]
    if n_comments:
        for s in stories:
            if s["num_comments"]:
                print(f"  comments: {s['title'][:60]}", file=sys.stderr)
                s["comments"] = fetch_comments(s["id"], n_comments)
    return stories


def write(data, out):
    if not out:
        json.dump(data, sys.stdout, ensure_ascii=False, indent=1)
        print()
        return
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    nc = sum(len(s.get("comments", [])) for s in data)
    print(f"wrote {out}: {len(data)} stories" + (f", {nc} comments" if nc else ""),
          file=sys.stderr)


def finish(data, out, label):
    write(data, out)
    if data:
        return 0
    print(f"\n!! {label} returned 0 items.", file=sys.stderr)
    if FAILURES:
        print(f"!! {len(FAILURES)} request(s) failed:", file=sys.stderr)
        for url, why in FAILURES[:3]:
            print(f"     {why}\n       {url}", file=sys.stderr)
    else:
        print("!! No request errors — the query matched nothing. Try broader terms.",
              file=sys.stderr)
    return 1


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    for name, help_ in (("search", "relevance-ranked stories"),
                        ("recent", "date-ranked stories")):
        p = sp.add_parser(name, help=help_)
        p.add_argument("--query", required=True)
        p.add_argument("--limit", type=int, default=50)
        p.add_argument("--comments", type=int, default=0,
                       help="comments per story; 0 = none")
        p.add_argument("--out")
    a = ap.parse_args()
    path = "search" if a.cmd == "search" else "search_by_date"
    return finish(_search(path, a.query, a.limit, a.comments), a.out, a.cmd)


if __name__ == "__main__":
    sys.exit(main())
