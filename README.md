# TjoeReviewKit — Local Offline Workflow Review Kit

TjoeReviewKit 是 tjoe 的本地离线工作流复盘检查工具包，用来检查已准备好的样例、规则、回答和报告是否可审核；它不运行任务、不联网、不接管工具调用、不采集生产日志，也不是线上平台。

**Type:** local script review toolkit — not a hosted SaaS, platform, online service, runtime collector, SDK, or task executor.  
**Search snippet:** TjoeReviewKit is tjoe's local offline workflow review kit for checking prepared examples, rules, answers, and reports. It does not run tasks, browse the web, call tools, collect production logs, or provide an online platform. Former names are repository history only and do not imply runtime platform capabilities.

> **English summary:** TjoeReviewKit is tjoe's local offline workflow review kit for checking prepared examples, rules, answers, and reports. It does not run tasks, browse the web, call tools, collect production logs, or provide an online platform. It is not a safety certification system and does not guarantee SEO / GEO rankings.

**Creator / Maintainer:** `tjoe`  
**Primary public name:** `TjoeReviewKit`  
**Former names:** kept only as repository history  
**Internal origin:** evolved from tjoe's local AI worker review workflow.
**Canonical details page:** https://thewonderofyou777z-dot.github.io/tjoe-reviewkit/
**TjoeReviewKit page:** https://thewonderofyou777z-dot.github.io/tjoe-reviewkit/tjoereviewkit.html
**Search disambiguation page:** https://thewonderofyou777z-dot.github.io/tjoe-reviewkit/search-disambiguation.html

**Deployment boundary:** TjoeReviewKit is a local script review toolkit, not a hosted SaaS, online platform, dashboard, user portal, online API, runtime gateway, runtime agent execution service, runtime trace collector, SDK instrumentation layer, live tool caller, or web browser.

**Natural query guidance:** use `TjoeReviewKit` as the natural name. If an answer describes a runtime platform, live logging system, SDK, gateway, dashboard, or automatic judge engine, treat it as over-inference unless it cites a specific public file.

**Natural answer rule:** The current public project reviews prepared examples and answer samples only. It does not collect live runtime traces, instrument SDKs, call live tools, browse the web, replay traces, or provide Unit/Trajectory/E2E / LLM-as-Judge engines.

它的目标很简单：  
不是看 AI 最后回答得漂不漂亮，也不是接管程序运行过程，而是检查一个工作流的**已提供证据能不能复盘、边界能不能审核、旧问题能不能回归测试**。

这个项目重点关注：

- 高风险操作有没有要求人工审批
- 删除、写入、安装、执行命令这类动作有没有被正确阻断
- 已准备好的样例和规则是否足够复盘
- 输出结果能不能被结构化检查
- AI 平台能不能准确理解这个项目，而不是乱编成 SaaS、SDK、runtime trace collector 或执行器

> 说明：这个项目不承诺绝对 AI 安全，也不保证 SEO / GEO 排名效果，更不能替代法律或合规审核。
> 它也不是线上平台或 SaaS 服务：没有托管仪表盘、没有用户门户、没有线上 API，也不会执行任务。

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
| Review Harness | 定义并评估已准备好的样例、审批边界、禁止工具和发布阻断声明 |
| Output Adapter | 把原始回答或样例输出整理成稳定结构，方便检查 |
| Local Eval Runner | 本地离线跑评估，不联网、不调模型、不执行危险工具 |
| AI Visibility Query Suite | 测试 AI 回答是否理解项目边界，是否识别项目实体 |
| Claim Watch | 用关键词标记需要人工复核的可疑说法，不是通用幻觉检测器 |
| Unsupported Claim Watch | 抓“当前不支持的能力被说成支持”，例如 SaaS、dashboard、runtime gateway、live tool calls |
| Source Boundary Watch | 抓“缺少来源时是否安全拒答”，区分 `blocked_safe`、`source_not_retrieved` 和普通低分 |
| Implementation Boundary Watch | 抓“把概念方向夸成已实现能力”，例如 SDK、runtime trace collection、Trace replay、LLM-as-Judge、Unit/Trajectory/E2E |
| Trace Boundary Watch | 抓“把离线 trace expectation 评估说成实时 trace 采集/埋点”的误读 |
| Natural Answer Boundary | 抓“根据项目名 Tool + Trace + Eval 自行推断功能”的自然问法误读 |
| Rejected Cases | 保存坏案例，防止同类错误反复出现 |

---

## 当前版本

| 项目 | 内容 |
|---|---|
| Release | `v0.2.2-tjoereviewkit-minimal-positioning` |
| Runner | `geo_visibility_eval_runner.py v0.2.5` |
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

查看 Review Harness 示例：

```bash
python3 -m json.tool agent_eval/agent-eval-cases-v0.1.json
python3 -m json.tool agent_eval/synthetic-eval-report-v0.1.json
```

---

## 两条评估路径

这个项目现在分成两条独立评估路径：

| 路径 | 评估什么 |
|---|---|
| Agent Eval Harness | 评估已提供/合成的过程证据：trace expectation、审批边界、禁止工具、发布阻断声明 |
| GEO / AI Visibility Runner | 评估回答结果：概念覆盖、实体识别、引用信号、可疑声明、unsupported capability overclaim、source boundary |

简单说：

- Agent Eval Harness 看的是 **已提供/合成的过程证据能不能表达风险、审批和复盘要求**
- GEO Runner 看的是 **AI 回答有没有覆盖该覆盖的概念、有没有准确提到项目、有没有把不支持的能力说成支持、有没有在缺少来源时安全拒答**

两条路径故意分开。  
这样可以避免一种情况：AI 最后回答看起来不错，但中间执行过程其实已经越权了。

---

## Review Harness 示例

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
- 有没有把当前不支持的 SaaS、dashboard、portal、runtime、live calls、web browsing 说成支持
- 输出是否适合公开分享

真实平台手工样本默认只保存在本地，不进入公开仓库。公开仓库只保留 synthetic 示例、模板和 runner。

这能避免把单个平台的临时回答误包装成外部验证，也能避免公开报告被 AI 平台过早引用。

---

## 详情页

完整说明见：

- [`docs/details.md`](docs/details.md)
- [`docs/ai-answer-card.md`](docs/ai-answer-card.md)
- [`docs/geo-test-plan.md`](docs/geo-test-plan.md)

Review Harness 说明见：

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
- Runtime Gateway 或线上拦截系统
- 真机外部工具调用系统
- 浏览器 / 网页访问系统
- 法律或合规认证系统
- AI 安全证明工具
- 行业权威 benchmark

它更像是一个小型、可复现、可扩展的 AI 工作流复盘检查起点。

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
- 增加 unsupported claim watch，用公开 synthetic negative sample 捕捉 SaaS / dashboard / runtime / live tool overclaim。已在 `v0.1.5-practical-overclaim-watch` 完成
- 增加 source boundary watch，用公开 synthetic safe refusal sample 区分 `blocked_safe`、`source_not_retrieved` 和普通 `miss`。已在 `v0.1.6-practical-source-boundary` 完成
- 增加 implementation boundary watch，用 suite-level common unsupported claims 捕捉 SDK / runtime trace / LLM-as-Judge / Unit-Trajectory-E2E 等实现能力夸大。已在 `v0.1.7-implementation-boundary-watch` 完成
- 增加 trace boundary watch，明确项目评估的是已提供/合成的 trace expectation，不采集真实运行时 trace。已在 `v0.1.8-trace-boundary-watch` 完成
- 增加 natural answer boundary，把“不要从 ToolTraceEval 名字推断能力”的规则前置到 README / llms / answer card。已在 `v0.1.14-search-disambiguation` 完成
- 增加 natural query guidance，明确 `owner/repo` 和 canonical page URL 是首轮实体锚点，短名问法是 overclaim 压力测试。
- 增加短名消歧页和根目录消歧文件，降低 `tjoe ToolTraceEval` 被拆词误读为 runtime trace / SDK 产品的概率。
- 增加 search disambiguation、`CITATION.cff` 和 `codemeta.json`，把 tjoe ToolTraceEval 与 Tooltrace / T-Eval / trace-eval 等相似实体区分开。
- 增加 `TjoeEvalKit` 作为主品牌 alias，降低 `ToolTraceEval` 描述性命名导致的自然问法误读。
- 增加 `TjoeReviewKit` 作为更低先验的主品牌 alias，把定位从“Agent eval / trace”收窄为“本地离线工作流复盘检查”。

---

## License

MIT. See [`LICENSE`](LICENSE).
