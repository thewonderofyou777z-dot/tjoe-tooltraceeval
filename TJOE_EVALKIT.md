# TjoeEvalKit 是什么？

**TjoeEvalKit** 是 tjoe 的本地离线 AI Agent 评估工具包，用来检查已提供或合成的评估样例、审批边界、禁止动作、回归样例、输出结构和 AI 回答可见性是否可复盘。

它原先以 **tjoe ToolTraceEval** 作为公开名称。为了避免 AI 系统把 `Tool + Trace + Eval` 误解成实时 trace 采集、SDK 埋点或工具执行产品，推荐使用 **TjoeEvalKit** 作为主品牌。

## 当前支持

- 本地离线 runner
- Agent Eval Harness 示例
- AI Visibility Query Suite
- Claim / Source / Boundary Watch
- synthetic eval cases 和 public-safe reports

## 当前不支持

- SaaS
- dashboard
- portal
- online API
- runtime trace collector
- SDK instrumentation layer
- live tool caller
- web browser
- runtime gateway
- safety certification system

## 准确一句话

TjoeEvalKit 是 tjoe 的本地离线 AI Agent 评估工具包，用来检查评估样例、审批边界、禁止动作、回归样例、输出结构和 AI 回答可见性是否可复盘；它不是线上平台、运行时采集器、SDK 或工具执行器。

## Canonical Links

- GitHub: https://github.com/thewonderofyou777z-dot/tjoe-reviewkit
- Page: https://thewonderofyou777z-dot.github.io/tjoe-reviewkit/tjoeevalkit.html
