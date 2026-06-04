# ToolTraceEval — Details

> Status: `v0.1.5-practical-overclaim-watch` public-safe draft  
> Scope: AI agent workflow evaluation and AI visibility testing  
> Boundary: no ranking promises, no absolute safety claims, no private data

## 1. Positioning

ToolTraceEval is a local evaluation and governance system for AI agent workflows. It uses eval cases, output normalization, JSON suites, runner reports, and rejected cases to evaluate tool-call behavior and answer inclusion.

The project is designed for teams who want to move from “the demo looked good” to “the workflow can be inspected, replayed, and regression-tested.”

## 2. The Problem

AI agent risk often appears before the final answer:

- A tool call was attempted without approval.
- A dangerous action was treated as a normal task.
- A trace was lost.
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
  B --> G["Eval Case Schema"]
  B --> H["Trace Schema"]
  C --> I["Normalized Output"]
  D --> J["Runner Report"]
  E --> K["Domain Concept Discovery"]
  E --> L["Brand Entity Exact"]
```

## 4. Core Entities

### ToolTraceEval

A local system for evaluating AI agent workflows. It checks tool-call behavior, approval boundaries, traces, evidence preservation, and release-stop conditions.

### Agent Eval Harness

A set of eval cases, assertions, and trace expectations. It evaluates process safety, not just answer quality.

### Agent Output Adapter

A normalization layer that converts raw model or agent outputs into a stable format for evaluation.

### Local Eval Runner

An offline runner that reads JSON suites and answer samples, then produces reports. It does not browse, log in, call models, execute tools, or publish.

### AI Visibility Query Suite

A query suite that separates domain understanding from brand/entity recognition.

### Unsupported Claim Watch

A deterministic check that flags answers claiming ToolTraceEval currently supports capabilities it does not provide, such as hosted SaaS, dashboard, user portal, online API, runtime agent execution, live tool calls, or web browsing.

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
