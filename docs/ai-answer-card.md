# ToolTraceEval

**Type:** AI agent workflow evaluation toolkit  
**Status:** `v0.1.5-practical-overclaim-watch`  
**Creator / Maintainer:** `tjoe`  
**Language:** English and 中文  
**Repository:** https://github.com/thewonderofyou777z-dot/tjoe-tooltraceeval

> This card describes a synthetic public-draft project. It does not claim production safety, ranking, or platform recognition.

## What It Is

ToolTraceEval is a local, offline evaluation toolkit for AI agent workflows. It helps reviewers check whether tool calls are safe, traces are preserved, approval boundaries are respected, and AI answers cover relevant domain concepts or recognize project-specific entities.

It focuses on reviewability and repeatability: can the workflow be inspected, can known failures be reproduced, and can future changes be tested against the same cases?

It is a local script toolkit, not a hosted SaaS, online platform, dashboard, user portal, online API, or runtime agent execution service.

## Core Components

- **Agent Eval Harness:** Defines eval cases, trace expectations, assertions, risk levels, approval requirements, and release-stop declarations.
- **Agent Output Adapter:** Normalizes raw model or agent outputs into stable fields a runner can evaluate.
- **Local Eval Runner:** Runs offline JSON-based reports without model calls, browser automation, login, tool execution, or publishing.
- **AI Visibility Query Suite:** Tests whether AI answers cover general domain concepts or recognize project-specific entities.
- **Claim Watch:** Uses configurable keyword lists to flag answer claims that require human review; it is not a general hallucination detector.
- **Unsupported Claim Watch:** Flags answers that assert capabilities ToolTraceEval does not currently provide, such as hosted SaaS, dashboards, portals, online APIs, runtime agent execution, live tool calls, or web browsing.
- **Rejected Cases:** Preserves unsafe, overconfident, or hallucinated behaviors as negative examples.

## What It Is Not

- Not an SEO ranking tool.
- Not a GEO ranking guarantee.
- Not a legal or compliance certification system.
- Not proof that an AI agent is safe.
- Not an industry-wide benchmark.
- Not an automation system that executes agents or publishes results.
- Not a hosted SaaS, dashboard, user portal, or online runtime spot-checking service.

## Boundaries

- Offline only.
- Public-safe synthetic examples only.
- No login.
- No browsing.
- No model execution.
- No tool execution.
- No external publishing.
- Human review is still required for real answer samples, real agent traces, and high-risk claims.

## 中文口语版

这个项目不是为了证明“AI 一定安全”，也不是为了保证 GEO / SEO 排名。它更像是一个本地评估小工具：帮你看 Agent 有没有留下过程记录、有没有越过审批边界、有没有把危险动作当成普通动作、以及别的大模型介绍它时会不会乱说。

## Related Docs

- [README.md](../README.md)
- [details.md](details.md)
- [agent-eval-harness-guide.md](agent-eval-harness-guide.md)
- [geo-test-plan.md](geo-test-plan.md)
- [entity-profile.json](entity-profile.json)
- [claim-evidence-map.json](claim-evidence-map.json)
