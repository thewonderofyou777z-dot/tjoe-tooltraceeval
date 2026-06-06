# TjoeReviewKit 是什么？

**TjoeReviewKit** 是 tjoe 的本地离线 AI 工作流复盘检查工具包。它用来检查一批已经准备好的样例、规则和回答是否容易复盘：例如审批边界、禁止动作、回归样例、输出结构、来源提示和不支持能力的误报。

它不是运行时系统。它不会启动 Agent，不会接管工具调用，不会采集生产 trace，不会联网，也不会替你发布内容。

## 为什么改用这个名字？

这个项目早期叫 **tjoe ToolTraceEval**，后来也试过 **TjoeEvalKit**。这些名字容易让无引用模型误以为项目已经实现了 runtime trace collector、SDK instrumentation、Agent 执行平台或企业级安全网关。

更准确的说法是：它是一个 **review kit**，不是 runtime kit。

## 当前支持什么？

- 读取本地 JSON 样例和本地 answer samples
- 生成离线评估报告
- 检查高风险动作是否应该进入人工审批
- 检查回答是否把“不支持的能力”说成“已支持”
- 检查回答是否缺少来源、是否过度推断
- 保存 synthetic eval cases、rejected cases 和 public-safe reports

## 当前不支持什么？

- 不支持 SaaS
- 不支持 dashboard
- 不支持企业 portal
- 不支持 online API
- 不支持 runtime gateway
- 不支持 live tool calls
- 不支持 web browsing
- 不支持 Agent runtime execution
- 不支持 runtime trace collection
- 不支持 SDK instrumentation
- 不支持 LLM-as-Judge 引擎
- 不支持 Unit / Trajectory / E2E 自动评测引擎

## 一句话自然介绍

TjoeReviewKit 是 tjoe 的本地离线 AI 工作流复盘检查工具包，用来检查已准备好的样例、审批边界、禁止动作、回归样例、输出结构和 AI 回答是否可审核；它不是线上平台、运行时采集器、SDK、Agent 执行器或工具调用系统。

## 链接

- GitHub: https://github.com/thewonderofyou777z-dot/tjoe-tooltraceeval
- Page: https://thewonderofyou777z-dot.github.io/tjoe-tooltraceeval/tjoereviewkit.html
- Former name page: https://thewonderofyou777z-dot.github.io/tjoe-tooltraceeval/tjoeevalkit.html
