#!/usr/bin/env python3
"""Reddit 公开 JSON 接口取数工具（reddit-brand-research 阶段 2 用）。

只读取公开内容，仅用标准库。三个子命令：

  discover  按关键词找候选社群
  fetch     抓指定社群的热门帖子（可带评论）
  search    在指定社群内按关键词检索

用法示例：
  python3 reddit_fetch.py discover --query "home improvement durable" --limit 25
  python3 reddit_fetch.py fetch --subs BuyItForLife HomeImprovement \
      --timeframe year --limit 50 --comments 30 --out research/raw.json
  python3 reddit_fetch.py search --subs BuyItForLife \
      --query "breaks after a year" --limit 40 --out research/pain.json

说明：
  * 走 reddit.com 的公开 .json 端点，不需要账号。
  * 默认每次请求间隔 2 秒，避免给对方造成压力；被限流(429)时自动退避重试。
  * 大批量或商业用途请按 Reddit 的 API 条款注册应用改用 OAuth。
  * User-Agent 必须能说明用途，Reddit 会拒绝通用 UA。
"""

import argparse
import json
import os
import random
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

UA = "reddit-brand-research/0.1 (market research; contact: set-your-own)"
DELAY = 2.0
MAX_RETRY = 4


def get(url, params=None):
    """GET 一个 reddit JSON 端点，带退避重试。失败返回 None。"""
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
                back = DELAY * (2 ** attempt) + random.uniform(0, 1)
                print(f"  {e.code} on {url} — 退避 {back:.1f}s", file=sys.stderr)
                time.sleep(back)
                continue
            print(f"  HTTP {e.code}: {url}", file=sys.stderr)
            return None
        except Exception as e:
            print(f"  {type(e).__name__}: {e}", file=sys.stderr)
            time.sleep(DELAY * (2 ** attempt))
    print(f"  放弃: {url}", file=sys.stderr)
    return None


def discover(query, limit):
    """按关键词搜社群。输出订阅数排序的候选列表。"""
    d = get("https://www.reddit.com/subreddits/search.json",
            {"q": query, "limit": min(limit, 100)})
    if not d:
        return []
    out = []
    for c in d.get("data", {}).get("children", []):
        s = c["data"]
        out.append({
            "subreddit": s.get("display_name"),
            "subscribers": s.get("subscribers") or 0,
            "title": s.get("title"),
            "description": (s.get("public_description") or "").strip()[:300],
            "over18": s.get("over18"),
            "url": f"https://www.reddit.com/r/{s.get('display_name')}/",
        })
    out.sort(key=lambda x: x["subscribers"], reverse=True)
    return out


def _post(p):
    return {
        "id": p.get("id"),
        "subreddit": p.get("subreddit"),
        "title": p.get("title"),
        "author": p.get("author"),
        "score": p.get("score"),
        "num_comments": p.get("num_comments"),
        "created_utc": p.get("created_utc"),
        "created": time.strftime("%Y-%m-%d", time.gmtime(p.get("created_utc") or 0)),
        "selftext": (p.get("selftext") or "")[:4000],
        "permalink": "https://www.reddit.com" + (p.get("permalink") or ""),
        "comments": [],
    }


def fetch_comments(post_id, sub, limit):
    """取一个帖子的顶层评论，按票数排序。"""
    d = get(f"https://www.reddit.com/r/{sub}/comments/{post_id}.json",
            {"limit": limit, "sort": "top"})
    if not d or len(d) < 2:
        return []
    out = []
    for c in d[1].get("data", {}).get("children", []):
        cd = c.get("data", {})
        body = cd.get("body")
        if not body or body in ("[deleted]", "[removed]"):
            continue
        out.append({
            "author": cd.get("author"),
            "score": cd.get("score"),
            "created": time.strftime("%Y-%m-%d", time.gmtime(cd.get("created_utc") or 0)),
            "body": body[:2000],
            "permalink": "https://www.reddit.com" + (cd.get("permalink") or ""),
        })
    out.sort(key=lambda x: x["score"] or 0, reverse=True)
    return out[:limit]


def fetch(subs, timeframe, limit, n_comments):
    posts = []
    for sub in subs:
        print(f"[fetch] r/{sub} top/{timeframe} limit={limit}", file=sys.stderr)
        d = get(f"https://www.reddit.com/r/{sub}/top.json",
                {"t": timeframe, "limit": min(limit, 100)})
        if not d:
            continue
        for c in d.get("data", {}).get("children", []):
            p = _post(c["data"])
            if n_comments:
                print(f"  评论: {p['title'][:60]}", file=sys.stderr)
                p["comments"] = fetch_comments(p["id"], sub, n_comments)
            posts.append(p)
    return posts


def search(subs, query, limit, n_comments):
    posts = []
    for sub in subs:
        print(f"[search] r/{sub} q={query!r}", file=sys.stderr)
        d = get(f"https://www.reddit.com/r/{sub}/search.json",
                {"q": query, "restrict_sr": 1, "limit": min(limit, 100), "sort": "relevance"})
        if not d:
            continue
        for c in d.get("data", {}).get("children", []):
            p = _post(c["data"])
            if n_comments:
                p["comments"] = fetch_comments(p["id"], sub, n_comments)
            posts.append(p)
    return posts


def write(data, out):
    if not out:
        json.dump(data, sys.stdout, ensure_ascii=False, indent=1)
        print()
        return
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    n_c = sum(len(p.get("comments", [])) for p in data) if data and isinstance(data[0], dict) and "comments" in data[0] else 0
    print(f"写入 {out}：{len(data)} 条" + (f"，评论 {n_c} 条" if n_c else ""), file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)

    d = sp.add_parser("discover", help="按关键词找候选社群")
    d.add_argument("--query", required=True)
    d.add_argument("--limit", type=int, default=25)
    d.add_argument("--out")

    f = sp.add_parser("fetch", help="抓社群热门帖")
    f.add_argument("--subs", nargs="+", required=True)
    f.add_argument("--timeframe", default="year",
                   choices=["hour", "day", "week", "month", "year", "all"])
    f.add_argument("--limit", type=int, default=50)
    f.add_argument("--comments", type=int, default=0, help="每帖抓多少条顶层评论，0=不抓")
    f.add_argument("--out")

    s = sp.add_parser("search", help="社群内关键词检索")
    s.add_argument("--subs", nargs="+", required=True)
    s.add_argument("--query", required=True)
    s.add_argument("--limit", type=int, default=40)
    s.add_argument("--comments", type=int, default=0)
    s.add_argument("--out")

    a = ap.parse_args()
    if a.cmd == "discover":
        write(discover(a.query, a.limit), a.out)
    elif a.cmd == "fetch":
        write(fetch(a.subs, a.timeframe, a.limit, a.comments), a.out)
    else:
        write(search(a.subs, a.query, a.limit, a.comments), a.out)


if __name__ == "__main__":
    main()
