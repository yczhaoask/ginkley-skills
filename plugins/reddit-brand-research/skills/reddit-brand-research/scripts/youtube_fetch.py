#!/usr/bin/env python3
"""Fetch YouTube comment threads via the Data API v3.

A third instrument alongside hn_fetch.py. Where HN skews to long-form
technical argument, YouTube comments skew to short reactions from a much
less technical audience — which is exactly the demand-side population the
HN rounds kept failing to reach.

Output shape matches hn_fetch.py so the same analysis applies: a list of
"stories" (videos) each carrying a "comments" list.

Needs a free API key. Google Cloud Console -> enable "YouTube Data API v3"
-> create an API key. Pass it as --key or set YT_API_KEY.

  search    find videos for a query          (100 quota units per call)
  comments  fetch comment threads for videos (1 unit per 100 comments)

Daily quota is 10,000 units, so searches are the expensive part. Prefer
passing known video IDs to `comments` over searching repeatedly.

Examples:
  python3 youtube_fetch.py search --query "claude code skills" \\
      --limit 25 --comments 100 --out out/y1_skills.json
  python3 youtube_fetch.py comments --ids OdtGN27LchE,nbqqnl3JdR0 \\
      --comments 200 --out out/y2_seed.json
"""

import argparse
import html as _html
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://www.googleapis.com/youtube/v3"
DELAY = float(os.environ.get("YT_DELAY", "0.3"))
MAX_RETRY = 4
FAILURES = []
QUOTA = {"units": 0}


def get(path, params, cost):
    """One API call. Returns parsed JSON, or None after logging the failure.

    Never returns an empty dict on error — a caller that sees None knows the
    request failed, rather than silently treating it as "no results".
    """
    url = f"{BASE}/{path}?{urllib.parse.urlencode(params)}"
    shown = url.replace(params.get("key", "\0"), "***")
    for attempt in range(MAX_RETRY):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                QUOTA["units"] += cost
                time.sleep(DELAY)
                return json.load(r)
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")[:600]
            reason = ""
            try:
                errs = json.loads(body)["error"]["errors"]
                reason = errs[0].get("reason", "")
            except Exception:
                pass
            # Permanent failures: retrying cannot change the outcome.
            if e.code in (400, 401, 403) and reason not in ("rateLimitExceeded",):
                FAILURES.append((shown, f"HTTP {e.code} {reason}", body))
                return None
            if e.code == 404:
                FAILURES.append((shown, "HTTP 404 not found", body))
                return None
            FAILURES.append((shown, f"HTTP {e.code} {reason}", body))
        except Exception as e:  # network-level
            FAILURES.append((shown, f"{type(e).__name__}: {e}", ""))
        time.sleep(DELAY * (2 ** attempt))
    return None


def _clean(t):
    """Comment bodies come back as HTML fragments."""
    import re
    t = re.sub(r"<br\s*/?>", "\n", t or "")
    t = re.sub(r"<[^>]+>", "", t)
    return _html.unescape(t).strip()


def _video(v):
    sn = v.get("snippet", {})
    st = v.get("statistics", {})
    vid = v.get("id") if isinstance(v.get("id"), str) else v.get("id", {}).get("videoId")
    return {
        "id": vid,
        "source": "youtube",
        "community": sn.get("channelTitle", ""),
        "title": _clean(sn.get("title", "")),
        "author": sn.get("channelTitle", ""),
        "score": int(st.get("likeCount", 0) or 0),
        "views": int(st.get("viewCount", 0) or 0),
        "num_comments": int(st.get("commentCount", 0) or 0),
        "created": (sn.get("publishedAt") or "")[:10],
        "selftext": _clean(sn.get("description", ""))[:4000],
        "url": f"https://www.youtube.com/watch?v={vid}",
        "permalink": f"https://www.youtube.com/watch?v={vid}",
        "comments": [],
    }


def _comment(item, video_id):
    top = item["snippet"]["topLevelComment"]
    sn = top["snippet"]
    return {
        "author": sn.get("authorDisplayName"),
        "score": int(sn.get("likeCount", 0) or 0),
        "created": (sn.get("publishedAt") or "")[:10],
        "body": _clean(sn.get("textOriginal") or sn.get("textDisplay"))[:2000],
        "replies": item["snippet"].get("totalReplyCount", 0),
        "permalink": f"https://www.youtube.com/watch?v={video_id}&lc={top['id']}",
    }


def fetch_comments(video_id, key, limit):
    """Comment threads for one video, newest-relevance first, paginated."""
    out, token = [], None
    while len(out) < limit:
        params = {
            "part": "snippet", "videoId": video_id, "key": key,
            "maxResults": min(100, limit - len(out)),
            "order": "relevance", "textFormat": "plainText",
        }
        if token:
            params["pageToken"] = token
        d = get("commentThreads", params, cost=1)
        if not d:
            return out
        for it in d.get("items", []):
            try:
                out.append(_comment(it, video_id))
            except (KeyError, TypeError):
                continue
        token = d.get("nextPageToken")
        if not token:
            break
    return out


def hydrate(ids, key):
    """videos.list for full statistics — search results omit view counts."""
    vids = []
    for i in range(0, len(ids), 50):
        d = get("videos", {
            "part": "snippet,statistics", "id": ",".join(ids[i:i + 50]), "key": key,
        }, cost=1)
        if d:
            vids.extend(_video(v) for v in d.get("items", []))
    return vids


def collect(videos, key, n_comments):
    for v in videos:
        if not n_comments or not v["num_comments"]:
            continue
        print(f"  comments: {v['title'][:60]}", file=sys.stderr)
        v["comments"] = fetch_comments(v["id"], key, n_comments)
    return videos


def write(data, out):
    if not out:
        json.dump(data, sys.stdout, ensure_ascii=False, indent=1)
        print()
        return
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    nc = sum(len(v.get("comments", [])) for v in data)
    print(f"wrote {out}: {len(data)} videos" + (f", {nc} comments" if nc else ""),
          file=sys.stderr)


def finish(data, out, label):
    write(data, out)
    print(f"quota used: ~{QUOTA['units']} units (daily cap 10,000)", file=sys.stderr)
    if data and any(v.get("comments") for v in data):
        return 0
    if data:
        print(f"\n!! {label}: found videos but 0 comments.", file=sys.stderr)
        print("!! Comments may be disabled, or --comments was 0.", file=sys.stderr)
    else:
        print(f"\n!! {label} returned 0 videos.", file=sys.stderr)
    if FAILURES:
        print(f"!! {len(FAILURES)} request(s) failed:", file=sys.stderr)
        for url, why, body in FAILURES[:3]:
            print(f"     {why}\n       {url}\n       {body[:300]}", file=sys.stderr)
    else:
        print("!! No request errors — the query matched nothing.", file=sys.stderr)
    return 1


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--key", default=os.environ.get("YT_API_KEY"))
    sp = ap.add_subparsers(dest="cmd", required=True)

    p = sp.add_parser("search", help="find videos for a query")
    p.add_argument("--query", required=True)
    p.add_argument("--limit", type=int, default=25)
    p.add_argument("--after", help="only videos published after YYYY-MM-DD")
    p.add_argument("--comments", type=int, default=100)
    p.add_argument("--out")

    p = sp.add_parser("comments", help="fetch comments for known video IDs")
    p.add_argument("--ids", required=True, help="comma-separated video IDs")
    p.add_argument("--comments", type=int, default=200)
    p.add_argument("--out")

    a = ap.parse_args()
    if not a.key:
        print("!! No API key. Pass --key or set YT_API_KEY.", file=sys.stderr)
        print("!! Get one free: console.cloud.google.com -> enable "
              "'YouTube Data API v3' -> Credentials -> API key", file=sys.stderr)
        return 2

    if a.cmd == "search":
        print(f"[search] {a.query!r}", file=sys.stderr)
        params = {
            "part": "snippet", "q": a.query, "key": a.key, "type": "video",
            "maxResults": min(a.limit, 50), "order": "relevance",
            "relevanceLanguage": "en",
        }
        if a.after:
            params["publishedAfter"] = f"{a.after}T00:00:00Z"
        d = get("search", params, cost=100)
        if not d:
            return finish([], a.out, "search")
        ids = [i["id"]["videoId"] for i in d.get("items", [])
               if i.get("id", {}).get("videoId")]
        videos = hydrate(ids, a.key)
    else:
        ids = [s.strip() for s in a.ids.split(",") if s.strip()]
        print(f"[comments] {len(ids)} video(s)", file=sys.stderr)
        videos = hydrate(ids, a.key)

    videos = collect(videos, a.key, a.comments)
    return finish(videos, a.out, a.cmd)


if __name__ == "__main__":
    sys.exit(main())
