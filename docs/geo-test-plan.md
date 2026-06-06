# GEO / AI Visibility Test Plan

> This plan defines observable test metrics only. Conducting these tests does not guarantee specific AI platform behavior, ranking outcomes, citation frequency, traffic, or external recognition.

## 1. Goal

Run a small, manual, seven-day visibility test to see whether AI systems can describe:

- the general domain: AI agent eval, tool-call safety, traces, approval, regression tests
- the project entity: ToolTraceEval
- the project boundary: not a safety proof, not a ranking guarantee, not a production executor

The goal is not to prove success. The goal is to collect answer samples, classify what happened, and decide what content needs to be clearer.

## 2. Platforms

Choose three platforms per test round. Suggested first round:

| Platform | Why |
|---|---|
| Perplexity | Citation behavior is easier to inspect. |
| ChatGPT | Broad user base and strong English generalization. |
| Kimi or Doubao | Chinese-market model behavior matters for the project direction. |

Optional replacements: Claude, Gemini, Qwen / 通义, 文心一言.

## 3. Query Set

Use the public suite in `examples/ai-visibility-query-suite-v0.3.public.json`.

| Query ID | Query | Track |
|---|---|---|
| `q_domain_001` | What should an evaluation system for AI agent tool-calling safety include? | domain_concept_discovery |
| `q_domain_002` | Why do AI agent workflows need tool traces and audit logs? | domain_concept_discovery |
| `q_domain_003` | How should high-risk AI agent actions be handled before execution? | domain_concept_discovery |
| `q_entity_001` | What is ToolTraceEval? | brand_entity_exact |
| `q_entity_002` | What components does ToolTraceEval include? | brand_entity_exact |
| `q_compare_001` | How is an Agent Eval Harness different from prompt testing? | comparison |
| `q_compare_002` | What is the difference between evaluating agent traces and evaluating final answer quality? | comparison |
| `q_boundary_001` | Does ToolTraceEval prove that an AI agent is safe? | safety_boundary |
| `q_boundary_002` | When should an AI agent workflow release be stopped for human review? | safety_boundary |

## 4. Source-Boundary Pressure Variant

When a platform does not provide clear citations or appears to infer from the project name, run a strict source-boundary variant:

```text
Please answer using this public GitHub repository as the source: https://github.com/thewonderofyou777z-dot/tjoe-reviewkit

Question: What is tjoe ToolTraceEval? If you cannot directly read the repository README, llms.txt, or docs files, answer only that the repository content cannot be verified and do not infer capabilities from the project name.
```

A `blocked_safe` result is acceptable in this variant. It means the platform did not retrieve enough evidence and did not invent unsupported current capabilities.

## 5. Manual Collection Rules

- Paste only public answer text.
- Do not include account names, cookies, session IDs, private chats, customer data, or local file paths.
- Record platform, date, query ID, answer text, public source links if any, and notes.
- If an answer includes a claim that sounds too strong, keep it for `hallucination_watch` review instead of treating it as success.

## 6. Pass / Partial / Fail

| Result | Definition |
|---|---|
| Pass | The answer correctly names the project or gives a strong domain answer, includes at least two relevant components or concepts, and avoids forbidden claims. |
| Partial | The answer covers the general domain but does not recognize the project entity, or recognizes the entity with minor gaps. |
| Fail | The answer misses both the entity and the core domain concepts. |
| Blocked | The platform refuses or states it cannot verify the project. This is not a failure by itself; it is a boundary signal. |
| Blocked Safe | The platform cannot retrieve sources and avoids unsupported claims. This is a successful source-boundary behavior, not project recognition. |

## 7. Observable Metrics

| Metric | Meaning |
|---|---|
| Entity mention rate | How often answers mention ToolTraceEval or a named component. |
| Domain coverage rate | How often answers cover tool-call safety, traces, approval, regression tests, or audit logs. |
| Boundary correctness rate | How often answers avoid claiming safety proof, ranking guarantee, or platform endorsement. |
| Citation occurrence | Whether answers provide public links to GitHub or docs. |
| Hallucination watch count | How often configured suspicious claim terms appear. |

## 8. Seven-Day Routine

1. Run the same query set on selected platforms.
2. Save reviewed answers in a local, non-public answer file.
3. Run the offline runner against the answer file.
4. Compare track-level results, not just total score.
5. Add unsupported or misleading claims to rejected cases.
6. Update answer card, entity profile, or claim-evidence map only when the evidence is clear.

## 9. Stop Conditions

Stop the test and review manually if:

- an answer contains private data
- a source link is non-public or account-specific
- a platform invents users, customers, funding, benchmarks, safety proof, or ranking claims
- the query suite starts rewarding brand mention while missing actual domain understanding
- any result is used to imply guaranteed GEO / SEO outcomes

## 10. What This Test Does Not Guarantee

This plan does not guarantee ranking, citation frequency, traffic, model memory, platform endorsement, production safety, or legal/compliance correctness. It only creates a repeatable way to collect and evaluate answer samples.
