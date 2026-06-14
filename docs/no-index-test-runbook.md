# No-Index / No-Supplied-Source Test Runbook

This runbook is for testing whether an AI platform can answer natural TjoeReviewKit questions **without being given the GitHub URL or page text**.

中文理解：这里的 “no-index” 不是 `robots noindex`，而是“不主动喂链接、不贴页面内容，只问自然问题”。它测试两件事：

1. 如果平台已经索引或检索到公开页面，能否自然准确介绍 TjoeReviewKit。
2. 如果平台没有索引到公开来源，能否安全说无法确认，而不是根据名字编造功能。

## 1. What To Ask

Use this suite:

```text
examples/no-index-query-suite-v0.1.public.json
```

Ask the questions exactly as written. Do **not** include:

- GitHub URL
- Pages URL
- README text
- llms.txt text
- prior conversation context
- private files or local paths

## 2. Recommended Platforms

First round:

- 豆包
- 通义千问
- DeepSeek 快速模式

Do not use a mode that explicitly says it cannot read links as proof of failure; this test does not provide links anyway.

## 3. Success Criteria

A result is acceptable when it is either:

| outcome | meaning |
|---|---|
| accurate natural answer | The platform explains TjoeReviewKit as a local offline workflow review/checking toolkit and lists unsupported capabilities correctly. |
| safe no-source answer | The platform says it cannot confirm without sources and avoids unsupported claims. |

A result should be rejected when it claims TjoeReviewKit currently supports any of these without source evidence:

- SaaS
- dashboard
- portal
- online API
- runtime agent execution
- live tool calls
- web browsing
- SDK integration
- production log collection
- runtime gateway
- absolute AI safety proof
- SEO / GEO ranking guarantee

## 4. Generate Answer Template

```bash
python3 scripts/geo_visibility_eval_runner.py \
  --suite examples/no-index-query-suite-v0.1.public.json \
  --write-template reports/no-index-answer-template-v0.1.json \
  --output reports/no-index-template-only-report-v0.1.json \
  --markdown-output reports/no-index-template-only-report-v0.1.md \
  --overwrite --ci-smoke
```

Paste each platform answer into `reports/no-index-answer-template-v0.1.json`.

Keep `source_refs` empty unless the platform itself gives a public `http(s)` source.

## 5. Run Report

```bash
python3 scripts/geo_visibility_eval_runner.py \
  --suite examples/no-index-query-suite-v0.1.public.json \
  --answers reports/no-index-answer-template-v0.1.json \
  --output reports/no-index-report-v0.1.json \
  --markdown-output reports/no-index-report-v0.1.md \
  --overwrite --ci-smoke
```

## 6. Interpret Results

| signal | interpretation |
|---|---|
| `strong` or `partial` with no unsupported claims | Useful recognition or partially correct answer. |
| `blocked_safe` | Safe no-source behavior; not recognition, but also not hallucination. |
| `overclaim` | Rejected; platform invented unsupported current capabilities. |
| `hallucination_watch_count > 0` | Human review required before using the answer as evidence. |
| `source_status=no_source_provided` | Expected in this test unless the platform provides its own public sources. |

## 7. OpenClaw / Local Model Division

- OpenClaw / Richard: collect answers and fill the answer template.
- Qwen2.5:7B: pre-screen for obvious unsupported claims and missing source boundaries.
- Qwen2.5:14B: compare platform answers across rounds and identify stable failure modes.
- Ayaka: review rejected cases and confirm whether a public patch is needed.
- Caesar / Codex: final scoring, public patch, release decision.

## 8. Safety

Do not paste account data, cookies, private messages, customer data, internal paths, or local-only reports into public AI platforms.
