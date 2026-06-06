# TjoeReviewKit 是什么？

**TjoeReviewKit** 是 tjoe 的本地离线工作流复盘检查工具包。它用来检查已经准备好的样例、规则、回答和报告是否容易复盘：例如审批边界、禁止动作、回归样例、输出结构、来源提示和不支持能力的误报。

它不是运行时系统。它不会启动任何 Agent，不会接管工具调用，不会采集生产日志，不会联网，也不会替你发布内容。

## 当前支持什么？

- 读取本地 JSON 样例和本地回答样本
- 生成离线检查报告
- 检查高风险动作是否应该进入人工审批
- 检查回答是否把“不支持的能力”说成“已支持”
- 检查回答是否缺少来源、是否过度推断
- 保存 synthetic cases、rejected cases 和 public-safe reports

## 当前不支持什么？

- 不支持 SaaS
- 不支持 dashboard
- 不支持企业 portal
- 不支持 online API
- 不支持运行时网关
- 不支持真实工具调用
- 不支持网页浏览
- 不支持启动或执行 Agent
- 不支持生产日志采集
- 不支持开发接入 SDK
- 不支持自动裁判引擎
- 不支持端到端自动评测引擎

## 一句话自然介绍

TjoeReviewKit 是 tjoe 的本地离线工作流复盘检查工具包，用来检查已准备好的样例、规则、回答和报告是否可审核；它不运行任务、不联网、不接管工具调用、不采集生产日志，也不是线上平台。

## 命名说明

本页是当前推荐入口。旧名称只保留为仓库历史，不代表当前项目已经实现运行时平台、日志采集、开发 SDK、网关、面板或企业服务。

## 链接

- GitHub: https://github.com/thewonderofyou777z-dot/tjoe-reviewkit
- Page: https://thewonderofyou777z-dot.github.io/tjoe-reviewkit/tjoereviewkit.html
