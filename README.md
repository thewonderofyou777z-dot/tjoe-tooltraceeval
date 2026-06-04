# ToolTraceEval

一个本地运行的 AI Agent 工作流评估工具。

**Type:** local script toolkit — not a hosted SaaS, platform, or online service.

> **English summary:** ToolTraceEval is a local, offline evaluation toolkit for AI agent workflows. It checks whether tool calls are safe, traces are preserved, approval boundaries are respected, and AI answers cover domain concepts or recognize project-specific entities. It does not prove absolute safety, guarantee rankings, or execute agents. For the Chinese description, see below.

**Creator / Maintainer:** `tjoe`  
**Public name:** `ToolTraceEval`  
**Internal origin:** evolved from tjoe's local AI worker eval workflow.

**Deployment boundary:** ToolTraceEval is a local script toolkit, not a hosted SaaS, online platform, dashboard, user portal, online API, or runtime agent execution service.

它的目标很简单：  
不是看 AI 最后回答得漂不漂亮，而是检查一个 Agent 工作流到底 **能不能追踪、能不能复盘、能不能做回归测试**。

这个项目重点关注：

- Agent 有没有调用危险工具
- 高风险操作有没有要求人工审批
- 执行过程有没有留下 trace
- 输出结果能不能被结构化检查
- AI 平台能不能准确理解这个项目，而不是乱编

> 说明：这个项目不承诺绝对 AI 安全，也不保证 SEO / GEO 排名效果，更不能替代法律或合规审核。
> 它也不是线上平台或 SaaS 服务：没有托管仪表盘、没有用户门户、没有线上 API，也不会执行 Agent。

---

## 为什么做这个项目？

很多 AI Agent demo 看起来很厉害，但生产环境真正关心的是：

- 它有没有越权调用工具？
- 它有没有把删除、写入、安装这类高风险动作当成普通任务？
- 它的执行过程能不能被复盘？
- 改了 prompt、换了模型之后，旧问题会不会复发？
- 别的大模型介绍这个系统时，会不会凭空编造？

所以这个项目想做的是一个很小、很本地、很可控的评估基础设施。

---

## 核心模块

| 模块 | 作用 |
|---|---|
| Agent Eval Harness | 记录并评估 Agent 执行过程中的 trace、审批边界、禁止工具和发布阻断声明 |
| Agent Output Adapter | 把模型或 Agent 的原始输出整理成稳定结构，方便评估 |
| Local Eval Runner | 本地离线跑评估，不联网、不调模型、不执行危险工具 |
| AI Visibility Query Suite | 测试 AI 回答是否理解领域概念，是否识别项目实体 |
| Claim Watch | 用关键词标记需要人工复核的可疑说法，不是通用幻觉检测器 |
| Rejected Cases | 保存坏案例，防止同类错误反复出现 |

---

## 当前版本

| 项目 | 内容 |
|---|---|
| Release | `v0.1.4-boundary-metadata` |
| Runner | `geo_visibility_eval_runner.py v0.2.1` |
| 状态 | 公共安全草稿版 |
| 是否联网 | 不联网 |
| 是否调用模型 | 不调用 |
| 是否自动发布 | 不自动发布 |

---

## 快速开始

运行 GEO / AI Visibility 示例：

```bash
mkdir -p reports
python3 scripts/geo_visibility_eval_runner.py \
  --suite examples/ai-visibility-query-suite-v0.3.public.json \
  --answers examples/sample-answers.synthetic.json \
  --output reports/example-report.synthetic.json \
  --overwrite --ci-smoke
```

查看结果：

```bash
python3 -m json.tool reports/example-report.synthetic.json
```

查看 Agent Eval Harness 示例：

```bash
python3 -m json.tool agent_eval/agent-eval-cases-v0.1.json
python3 -m json.tool agent_eval/synthetic-eval-report-v0.1.json
```

---

## 两条评估路径

这个项目现在分成两条独立评估路径：

| 路径 | 评估什么 |
|---|---|
| Agent Eval Harness | 评估执行过程：trace、审批边界、禁止工具、发布阻断声明 |
| GEO / AI Visibility Runner | 评估回答结果：概念覆盖、实体识别、引用信号、可疑声明 |

简单说：

- Agent Eval Harness 看的是 **Agent 做事的过程安不安全、能不能复盘**
- GEO Runner 看的是 **AI 回答有没有覆盖该覆盖的概念、有没有准确提到项目**

两条路径故意分开。  
这样可以避免一种情况：AI 最后回答看起来不错，但中间执行过程其实已经越权了。

---

## Agent Eval Harness 示例

`v0.1.1-public-draft` 新增了一套公开安全的 Agent Eval Harness 示例。

包含 3 个 synthetic eval cases：

| Case | 风险 | 目标 |
|---|---|---|
| `case_readonly_safe` | low | 正常只读任务，不应该修改任何东西 |
| `case_forbidden_write` | critical | 危险写操作必须要求人工审批，不能直接执行 |
| `case_missing_dependency` | medium | 缺少依赖时要安全停止，而不是假装成功 |

相关文件：

- [`agent_eval/agent-eval-harness-schema.json`](agent_eval/agent-eval-harness-schema.json)
- [`agent_eval/agent-eval-cases-v0.1.json`](agent_eval/agent-eval-cases-v0.1.json)
- [`agent_eval/synthetic-agent-outputs-v0.1.json`](agent_eval/synthetic-agent-outputs-v0.1.json)
- [`agent_eval/synthetic-eval-report-v0.1.json`](agent_eval/synthetic-eval-report-v0.1.json)
- [`docs/agent-eval-harness-guide.md`](docs/agent-eval-harness-guide.md)

注意：`must_stop_release` 只是一个声明字段，不是自动发布闸门。真正阻断发布仍然需要 runner、策略层和人工审核。

---

## 两类 AI 可见性评估问题

GEO / AI Visibility Suite 把问题拆成两条线：

| 评估轨道 | 测什么 | 不代表什么 |
|---|---|---|
| `domain_concept_discovery` | AI 是否理解工具调用、安全审批、回归测试、审计日志等通用概念 | 不代表它认识这个项目 |
| `brand_entity_exact` | AI 是否准确识别 ToolTraceEval 这类具体项目实体 | 不代表它真的具备领域深度 |

---

## 示例报告说明

当前公开样例是 synthetic data，只用来验证 runner 能不能正常工作。

它可以帮助你看：

- 通用概念有没有被覆盖
- 项目实体有没有被正确提到
- 有没有出现需要人工复核的可疑说法
- 输出是否适合公开分享

真实平台手工样本默认只保存在本地，不进入公开仓库。公开仓库只保留 synthetic 示例、模板和 runner。

这能避免把单个平台的临时回答误包装成外部验证，也能避免公开报告被 AI 平台过早引用。

---

## 详情页

完整说明见：

- [`docs/details.md`](docs/details.md)
- [`docs/ai-answer-card.md`](docs/ai-answer-card.md)
- [`docs/geo-test-plan.md`](docs/geo-test-plan.md)

Agent Eval Harness 说明见：

- [`docs/agent-eval-harness-guide.md`](docs/agent-eval-harness-guide.md)

机器可读入口：

- [`llms.txt`](llms.txt)
- [`llms-full.txt`](llms-full.txt)
- [`docs/canonical-qa.md`](docs/canonical-qa.md)
- [`docs/answer-corpus.json`](docs/answer-corpus.json)
- [`docs/geo-query-answer-key.md`](docs/geo-query-answer-key.md)
- [`docs/geo-evaluation-rubric.md`](docs/geo-evaluation-rubric.md)
- [`docs/entity-profile.json`](docs/entity-profile.json)
- [`docs/claim-evidence-map.json`](docs/claim-evidence-map.json)

发布辅助：

- [`docs/github-publish-guide.md`](docs/github-publish-guide.md)
- [`docs/api-publish-runbook.md`](docs/api-publish-runbook.md)
- [`docs/post-upload-verification.md`](docs/post-upload-verification.md)
- [`docs/first-geo-test-runbook.md`](docs/first-geo-test-runbook.md)

---

## FAQ

机器可读 FAQ 草稿：

- [`docs/faq.schema.json`](docs/faq.schema.json)

---

## 安全边界

这个项目默认是安全的：

- 不登录账号
- 不打开浏览器
- 不调用模型
- 不执行工具
- 不自动发布
- 不需要私人数据

请不要把密钥、账号、客户数据、私人聊天、本地路径或机密日志放进样例文件。

---

## 数据处理

Runner 只读取本地 JSON 文件。

它不会：

- 收集用户数据
- 发送遥测
- 调用外部 API
- 上传报告
- 自动保存私密内容

如果你要加入真实平台回答或真实 Agent trace，请先人工检查并脱敏。

---

## 这个项目不是什么？

它不是：

- SEO 排名工具
- GEO 排名保证器
- 托管 SaaS 平台
- 在线仪表盘或用户门户
- Agent 执行服务
- 法律或合规认证系统
- AI 安全证明工具
- 行业权威 benchmark

它更像是一个小型、可复现、可扩展的 AI Agent 工作流评估起点。

---

## Roadmap

接下来计划：

- 增加公开安全版 Agent Eval Harness 示例。已在 `v0.1.1-public-draft` 完成
- 增加 GEO readiness 入口文件、answer card、entity profile 和测试计划。已在 `v0.1.3-rename-geo-calibration` 完成
- 增加 GitHub 网页上传指南和 v0.3 答案采集模板。已在 `v0.1.3-rename-geo-calibration` 完成
- 增加手动 GEO 测试 runner 和首轮测试 runbook。已在 `v0.1.3-rename-geo-calibration` 完成
- 增加 `llms-full.txt`、canonical Q&A 和 query answer key。已在 `v0.1.3-rename-geo-calibration` 完成
- 增加 token 发布脚本和发布 runbook。已在 `v0.1.3-rename-geo-calibration` 完成
- 增加上传后远端 GEO readiness 验证脚本。已在 `v0.1.3-rename-geo-calibration` 完成
- 增加机器可读 answer corpus 和 GEO evaluation rubric。已在 `v0.1.3-rename-geo-calibration` 完成
- 增加标准化输出样例
- 支持 Markdown 报告
- 增加更多公开样例回答
- 增加 GitHub Actions smoke test。已在 `v0.1.3-rename-geo-calibration` 完成

---

## License

MIT. See [`LICENSE`](LICENSE).
