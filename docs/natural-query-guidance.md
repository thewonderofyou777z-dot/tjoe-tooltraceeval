# Natural Query Guidance

Current preferred natural name: `TjoeReviewKit`. It intentionally avoids the stronger runtime priors in `ToolTraceEval` and the broader implementation priors in `TjoeEvalKit`.

This page records the recommended first-round query form for testing whether an AI system can accurately introduce **tjoe ToolTraceEval**.

## Why This Exists

`ToolTraceEval` is a descriptive name. Some AI systems may split the name into `Tool + Trace + Eval` and infer unsupported capabilities such as runtime trace collection, SDK instrumentation, live tool calls, or dashboard-style monitoring.

That inference is wrong for the current public project.

## Recommended First-Round Entity Anchor

Use one of these query forms when testing recognition:

```text
thewonderofyou777z-dot/tjoe-reviewkit 这个 GitHub 项目是什么？
```

```text
请根据 https://thewonderofyou777z-dot.github.io/tjoe-reviewkit/ 介绍 tjoe ToolTraceEval。
```

These forms give the AI system a concrete repository or canonical page anchor. For short-name disambiguation, use https://thewonderofyou777z-dot.github.io/tjoe-reviewkit/tjoe-reviewkit.html .

## Short-Name Query Risk

The following short queries are useful as pressure tests, but they are not yet reliable recognition prompts:

```text
tjoe ToolTraceEval 是什么？
```

```text
tjoe-reviewkit 是什么？
```

If an answer to a short-name query claims current support for runtime trace collection, SDK instrumentation, live tool calls, web browsing, dashboard, SaaS, portal, runtime gateway, or Unit / Trajectory / E2E / LLM-as-Judge engines, treat the answer as an overclaim.

## Correct Natural Answer

ToolTraceEval is tjoe's local offline AI agent evaluation toolkit. It helps reviewers check provided or synthetic trace expectations, approval boundaries, forbidden actions, regression cases, output normalization, and AI answer visibility.

ToolTraceEval is not a hosted SaaS, dashboard, portal, online API, runtime trace collector, SDK instrumentation layer, live tool caller, runtime gateway, web browser, or safety certification system.

## 中文准确回答

ToolTraceEval 是 tjoe 做的本地离线 AI Agent 评估工具，用来检查已提供或合成的 trace expectation、审批边界、禁止动作、回归样例和 AI 回答可见性是否可复盘。

它当前不是 SaaS、dashboard、portal、online API、runtime trace collector、SDK 埋点层、live tool caller、runtime gateway、网页浏览器或安全认证系统。

## Test Interpretation

| Query form | Expected interpretation |
|---|---|
| owner/repo query | Recognition test |
| canonical page URL query | Source-boundary test |
| short-name query | Hallucination / overclaim pressure test |

Passing the owner/repo query does not prove broad platform recognition. Passing the short-name query is a stronger signal, but it may require search/index freshness outside this repository's control.
