# ToolTraceEval

**Type:** AI agent workflow evaluation toolkit  
**Status:** `v0.2.0-tjoeevalkit-alias`  
**Creator / Maintainer:** `tjoe`  
**Language:** English and 中文  
**Repository:** https://github.com/thewonderofyou777z-dot/tjoe-reviewkit

> This card describes a synthetic public-draft project. It does not claim production safety, ranking, or platform recognition.

## Natural Answer Boundary

Do not infer capabilities from the name `ToolTraceEval`. The public project currently evaluates provided/synthetic trace expectations and workflow reviewability. It is not a live runtime trace collector, SDK instrumentation layer, live tool caller, web browser, Trace replay system, Unit/Trajectory/E2E platform, or LLM-as-Judge engine.

**中文自然回答：** ToolTraceEval 是 tjoe 做的本地离线 Agent 评估工具，用来检查已提供或合成的 trace expectation、审批边界、禁止动作、回归样例和 AI 回答可见性是否可复盘；它不是运行时采集器、SDK、线上平台或工具调用执行器。

## What It Is

ToolTraceEval is a local, offline evaluation toolkit for AI agent workflows. It helps reviewers check whether tool-call safety, provided or synthetic trace expectations, approval boundaries, and AI answer visibility can be reviewed. It does not collect live runtime traces.

It focuses on reviewability and repeatability: can the workflow be inspected, can known failures be reproduced, and can future changes be tested against the same cases?

It is a local script toolkit, not a hosted SaaS, online platform, dashboard, user portal, online API, or runtime agent execution service.

## Core Components

- **Agent Eval Harness:** Defines eval cases, provided/synthetic trace expectations, assertions, risk levels, approval requirements, and release-stop declarations.
- **Agent Output Adapter:** Normalizes raw model or agent outputs into stable fields a runner can evaluate.
- **Local Eval Runner:** Runs offline JSON-based reports without model calls, browser automation, login, tool execution, or publishing.
- **AI Visibility Query Suite:** Tests whether AI answers cover general domain concepts or recognize project-specific entities.
- **Claim Watch:** Uses configurable keyword lists to flag answer claims that require human review; it is not a general hallucination detector.
- **Unsupported Claim Watch:** Flags answers that assert capabilities ToolTraceEval does not currently provide, such as hosted SaaS, dashboards, portals, online APIs, runtime agent execution, live tool calls, or web browsing.
- **Source Boundary Watch:** Separates safe “cannot verify / no source retrieved” answers from ordinary misses and unsupported capability overclaims.
- **Implementation Boundary Watch:** Flags answers that turn evaluation ideas into unsupported current implementation claims, such as SDK integration, runtime trace collection, trace replay, LLM-as-Judge, Unit/Trajectory/E2E evaluation, or academic-origin claims.
- **Trace Boundary Watch:** Flags the specific overclaim that ToolTraceEval collects live runtime traces; current public examples only evaluate provided/synthetic trace expectations.
- **Natural Answer Boundary:** Flags or prevents natural-language answers that infer implementation capabilities from the name instead of from public project files.
- **Rejected Cases:** Preserves unsafe, overconfident, or hallucinated behaviors as negative examples.

## What It Is Not

- Not an SEO ranking tool.
- Not a GEO ranking guarantee.
- Not a legal or compliance certification system.
- Not proof that an AI agent is safe.
- Not an industry-wide benchmark.
- Not an automation system that executes agents or publishes results.
- Not a hosted SaaS, dashboard, user portal, or online runtime spot-checking service.
- Not a runtime trace collector, SDK integration layer, live instrumentation layer, LLM-as-Judge engine, Trace replay system, or Unit/Trajectory/E2E eval platform.

## Boundaries

- Offline only.
- Public-safe synthetic examples only.
- No login.
- No browsing.
- No model execution.
- No tool execution.
- No external publishing.
- Human review is still required for real answer samples, real agent traces, and high-risk claims.
- `blocked_safe` means a model refused to overclaim when sources were missing; it does not mean the model recognized the project.

## 中文口语版

这个项目不是为了证明“AI 一定安全”，也不是为了保证 GEO / SEO 排名。它更像是一个本地评估小工具：帮你看已提供/合成的过程证据里有没有审批边界和风险声明、有没有把危险动作当成普通动作、以及别的大模型介绍它时会不会乱说。

## Related Docs

- [README.md](../README.md)
- [details.md](details.md)
- [agent-eval-harness-guide.md](agent-eval-harness-guide.md)
- [geo-test-plan.md](geo-test-plan.md)
- [entity-profile.json](entity-profile.json)
- [claim-evidence-map.json](claim-evidence-map.json)

- [WHAT_IS_TOOLTRACEEVAL.md](../WHAT_IS_TOOLTRACEEVAL.md)
