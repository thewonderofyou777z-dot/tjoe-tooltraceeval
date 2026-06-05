# ToolTraceEval — Details

> Status: `v0.1.12-natural-query-guidance` public-safe draft  
> Scope: AI agent workflow evaluation and AI visibility testing  
> Boundary: no ranking promises, no absolute safety claims, no private data

## 1. Positioning

ToolTraceEval is a local evaluation and governance system for AI agent workflows. It uses eval cases, provided/synthetic trace expectations, output normalization, JSON suites, runner reports, and rejected cases to evaluate workflow reviewability and answer inclusion. It does not collect live runtime traces.

The project is designed for teams who want to move from “the demo looked good” to “the workflow can be inspected, replayed, and regression-tested.”

## 2. The Problem

AI agent risk often appears before the final answer:

- A tool call was attempted without approval.
- A dangerous action was treated as a normal task.
- A required trace expectation was missing from the provided evidence.
- A model answer looked fluent but hallucinated the project’s origin.
- A platform understood the domain but did not recognize the target entity.

Final-answer scoring alone cannot catch these issues.

## 3. System Map

```mermaid
flowchart TD
  A["ToolTraceEval"] --> B["Agent Eval Harness"]
  A --> C["Agent Output Adapter"]
  A --> D["Local Eval Runner"]
  A --> E["AI Visibility Query Suite"]
  A --> F["Rejected Cases"]
  A --> M["Unsupported Claim Watch"]
  A --> N["Source Boundary Watch"]
  A --> O["Implementation Boundary Watch"]
  B --> G["Eval Case Schema"]
  B --> H["Trace Schema"]
  C --> I["Normalized Output"]
  D --> J["Runner Report"]
  E --> K["Domain Concept Discovery"]
  E --> L["Brand Entity Exact"]
```

## 4. Core Entities

### ToolTraceEval

A local system for evaluating AI agent workflows. It checks tool-call safety, approval boundaries, provided/synthetic trace expectations, evidence preservation, and release-stop conditions.

### Agent Eval Harness

A set of eval cases, assertions, and provided/synthetic trace expectations. It evaluates reviewable process evidence, not just answer quality.

### Agent Output Adapter

A normalization layer that converts raw model or agent outputs into a stable format for evaluation.

### Local Eval Runner

An offline runner that reads JSON suites and answer samples, then produces reports. It does not browse, log in, call models, execute tools, or publish.

### AI Visibility Query Suite

A query suite that separates domain understanding from brand/entity recognition.

### Unsupported Claim Watch

A deterministic check that flags answers claiming ToolTraceEval currently supports capabilities it does not provide, such as hosted SaaS, dashboard, user portal, online API, runtime agent execution, live tool calls, or web browsing.

### Source Boundary Watch

A deterministic check that distinguishes ordinary no-source answers from safe refusal answers. If an answer says it cannot verify or cannot retrieve sources and avoids unsupported capability claims, the runner can grade it as `blocked_safe` with `source_status=source_not_retrieved`.

`blocked_safe` is not proof that an AI platform recognizes ToolTraceEval. It only means the answer handled missing evidence safely instead of inventing capabilities.

### Implementation Boundary Watch

A deterministic check that flags answers that turn evaluation ideas into unsupported current implementation claims. This matters in no-citation pressure tests because an answer may correctly say ToolTraceEval is not SaaS or a dashboard while still inventing SDK integration, runtime trace collection, trace replay, LLM-as-Judge, Unit/Trajectory/E2E evaluation, or academic-origin claims.

ToolTraceEval discusses traceability and agent-eval concepts, but the public draft should not be described as a runtime trace collector, live instrumentation SDK, runtime logger, LLM-as-Judge engine, Trace replay system, or Unit/Trajectory/E2E eval platform. Its public examples evaluate provided/synthetic trace expectations only.

### Natural Answer Boundary

A natural-answer guideline for entity recognition tests. The project name can mislead models into decomposing `ToolTraceEval` as Tool + Trace + Eval and inventing runtime capabilities. Correct natural answers must ground claims in public files and should describe the project as a local offline eval toolkit for provided/synthetic trace expectations, approval boundaries, regression cases, output normalization, and AI visibility.

### Trace Boundary Watch

A deterministic boundary check for answers that confuse provided/synthetic trace expectation evaluation with live runtime trace collection. Current ToolTraceEval public examples do not instrument real agents, collect live tool-call logs, replay traces, or provide SDK-based runtime logging.

### AI Answer Card

A short, AI-readable system definition page. It gives a canonical description, component list, and boundary statement without claiming external recognition or ranking effects.

### Entity Profile

A machine-readable JSON profile for the project entity, aliases, components, boundaries, and canonical files.

### Claim-Evidence Map

A machine-readable JSON map that links internal project claims to specific evidence files. It is a review aid, not proof of external performance.

### Rejected Cases

Negative examples used to preserve known bad behaviors and prevent repeated failure.

## 5. AI Visibility Tracks

### `domain_concept_discovery`

Measures whether an answer covers general domain concepts such as:

- Function calling safety
- Tool traces
- Human approval
- Regression testing
- CI/CD integration
- Audit logs
- Sandboxes

### `brand_entity_exact`

Measures whether an answer accurately recognizes project-specific entities such as:

- ToolTraceEval
- Agent Eval Harness
- Agent Output Adapter
- Local Eval Runner
- AI Visibility Query Suite

### Claim Watch

Some queries include `hallucination_watch` terms. This is a conservative keyword-watch mechanism for claims that need human review. It is not a general hallucination detector and does not judge truth by itself.

## 6. Evidence Philosophy

The project prefers small, reproducible evidence over broad claims.

Good evidence:

- A JSON suite can be parsed.
- A runner report can be reproduced.
- A known bad answer triggers a warning.
- A malformed suite fails validation.
- A hallucinated claim is flagged.
- A project claim maps to a public file in `docs/claim-evidence-map.json`.

Unsupported claims:

- “This proves AI safety.”
- “This improves rankings.”
- “This is an industry standard.”
- “A platform already recognizes this project.”

## 7. Public Sample Interpretation

The public examples are synthetic. They verify the runner mechanics, not market performance.

If an answer scores well on `domain_concept_discovery`, that means it covers the topic. It does not mean it knows this project.

If an answer scores poorly on `brand_entity_exact`, that means the project entity is not recognized clearly. It does not mean the general domain answer is bad.

## 8. FAQ

See [`faq.schema.json`](faq.schema.json).

## 8.1 GEO Readiness Files

The public draft also includes:

- [`../llms.txt`](../llms.txt): machine-readable navigation aid.
- [`ai-answer-card.md`](ai-answer-card.md): concise answer card for AI systems and human reviewers.
- [`entity-profile.json`](entity-profile.json): structured entity profile.
- [`claim-evidence-map.json`](claim-evidence-map.json): internal claim-to-evidence map.
- [`geo-test-plan.md`](geo-test-plan.md): manual seven-day GEO / AI visibility test plan.

## 9. Safety Boundaries

The runner is intentionally constrained:

- no network
- no model calls
- no browser automation
- no login
- no command execution beyond local report generation
- no publishing

The user is responsible for reviewing any answer samples before saving them.

## 10. Data Handling

This project does not collect user data, send telemetry, call external APIs, or upload reports. All examples are synthetic. Real answer samples should be redacted and reviewed before being committed.

## 11. Release Readiness

This directory is a GitHub-ready public draft if:

- It contains no local absolute paths.
- It contains no private data.
- It contains no unsupported ranking or safety claims.
- The synthetic example passes.
- A license decision is made before public reuse.

- [WHAT_IS_TOOLTRACEEVAL.md](../WHAT_IS_TOOLTRACEEVAL.md)
