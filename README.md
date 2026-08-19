# Reddit Brand Research

> 把模糊的出海想法，用 Reddit 上的真实用户讨论，一步步收敛成有市场依据、可落地的品牌方案。

一个 Claude Code skill。它不生成方案，它**陪你把判断想清楚**——通过一问一答澄清产品，匹配并确认社群，抓取真实讨论，再把讨论里反复出现的信号转成品牌定位。

**每一条品牌结论都必须能指回一条真实的用户原话。写不出引用的结论，会被要求删掉或回去补调研。**

## 安装

```
/plugin marketplace add yczhaoask/ginkley-skills
/plugin install reddit-brand-research@ginkley-skills
```

装完直接说「我想做出海调研」或「帮我定品牌定位」就会触发。

## 六个阶段

```
探索  →  调研  →  杠杆  →  策略  →  视觉  →  落地
```

| 阶段 | 干什么 | 产出 |
|---|---|---|
| 探索 | 一问一答澄清产品、人群、市场、动机 | 产品理解卡 |
| 调研 | 匹配 Reddit 社群 → 你确认 → 抓热门讨论 | 社群清单 + 讨论语料 |
| 杠杆 | 从语料里提炼未被满足的机会点 | 机会点清单（带引用） |
| 策略 | 定位、核心卖点、Slogan、品牌人格 | 品牌策略卡 |
| 视觉 | 视觉调性与语言风格 | 调性说明 |
| 落地 | 渠道、首批内容、验证指标 | 执行清单 |

## 三道门禁

这套流程有效的唯一原因，是它不让你跳步：

1. **先理解产品，再开始调研。** 四个必答问题没答完，不进调研——产品没搞清楚就去搜社区，搜到的全是噪音。
2. **社群范围必须你确认。** 匹配出候选社群后会列给你看，等你确认或修改才开抓。你对自己的行业有它没有的直觉。
3. **没有引用，不出定位。** 每条结论都要能指回具体的帖子或评论。

## 核心转化关系

| 输入信号 | → | 策略输出 |
|---|---|---|
| 反复出现的痛点 | → | 品牌定位 |
| 对竞品的真实评价 | → | 核心卖点 |
| 尚未解决的需求 | → | Slogan / 品牌人格 |

## 适合谁

1. **已经有产品** —— 想把现有业务做到海外
2. **准备做出海** —— 调研不清晰，定位还模糊
3. **只有一个想法** —— 完全不知道第一步从哪里开始

## 附带工具

`scripts/reddit_fetch.py` —— 通过 Reddit 公开 JSON 接口做社群发现与帖子/评论收集，仅用标准库，带 2 秒请求间隔和 429 退避。

```bash
python3 reddit_fetch.py discover --query "home improvement durable" --limit 25
python3 reddit_fetch.py fetch --subs BuyItForLife HomeImprovement \
    --timeframe year --limit 50 --comments 30 --out research/raw.json
python3 reddit_fetch.py search --subs BuyItForLife \
    --query "breaks after a year" --limit 40 --out research/pain.json
```

大批量或商业用途请按 Reddit 的 API 条款注册应用改走 OAuth。参与社区讨论前先读该 subreddit 的 rules——直接发广告会被封。

## Attribution

This methodology is not my own. It was distilled from a short video on the Chinese-language internet.

In that video the original author demonstrated a workflow tool of their own making that shares its name — this repository is not that tool, and has no affiliation with its author. What follows is an independent implementation that I wrote from the methodology as publicly described in the video.

The original video's author and link are not listed here at this time.

Note that the video explains four of the six phases in full: explore, research, leverage, and strategy. Visual and launch appear only as labels in its progress bar and are never elaborated; those two phases in this repository are reasoned extensions consistent with the rest of the methodology, and each of those files says so at the top.

If you are the original author and would like the credit adjusted, or want this taken down, please open an issue.

## License

MIT，见 [LICENSE](LICENSE)。许可覆盖本仓库的文字与代码实现，不主张对上述方法论本身的任何权利。
