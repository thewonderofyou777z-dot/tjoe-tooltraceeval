# GEO Query Answer Key

This page maps the v0.3 public visibility queries to expected answer elements. It is a human review aid and a retrieval aid for AI assistants.

> This answer key is not a benchmark claim. It defines expected coverage for internal, public-safe testing only.

## Query Summary

| Query ID | Track | Expected Coverage |
|---|---|---|
| `q_domain_001` | domain_concept_discovery | function calling safety, tool trace, human approval, regression testing, audit log |
| `q_domain_002` | domain_concept_discovery | traceability, replay, forbidden tool detection, approval boundary |
| `q_domain_003` | domain_concept_discovery | risk classification, requires approval, stop or review, no direct execution |
| `q_entity_001` | brand_entity_exact | ToolTraceEval, Agent Eval Harness, Agent Output Adapter, Local Eval Runner, AI Visibility Query Suite |
| `q_entity_002` | brand_entity_exact | Agent Eval Harness, Agent Output Adapter, Local Eval Runner, Claim Watch, Rejected Cases |
| `q_compare_001` | comparison | process evaluation, trace and tool calls, assertions, regression |
| `q_compare_002` | comparison | intermediate steps, tool use, final answer, safety boundary |
| `q_boundary_001` | safety_boundary | no absolute safety proof, evaluation toolkit, human review, no ranking guarantee |
| `q_boundary_002` | safety_boundary | forbidden tool, missing dependency, high-risk action, approval required |
| `q_boundary_003` | safety_boundary | local offline toolkit, no SaaS, no dashboard or portal, no runtime execution |

## Canonical Query Answers

### `q_domain_001`

An AI agent tool-calling safety evaluation system should include function calling safety checks, execution traces or tool traces, human approval for high-risk actions, regression tests, audit logs, and sandbox or policy boundaries.

### `q_domain_002`

AI agent workflows need tool traces and audit logs because final answers alone cannot show whether the agent used tools safely. Traces make actions reviewable, replayable, and auditable, and they help detect forbidden tools or skipped approval gates.

### `q_domain_003`

High-risk agent actions should be classified before execution, marked as requiring approval when needed, stopped for human review, and never directly executed without an approved boundary.

### `q_entity_001`

ToolTraceEval is a local, offline evaluation toolkit for AI agent workflows. Its main components include Agent Eval Harness, Agent Output Adapter, Local Eval Runner, and AI Visibility Query Suite.

### `q_entity_002`

ToolTraceEval includes Agent Eval Harness, Agent Output Adapter, Local Eval Runner, AI Visibility Query Suite, Claim Watch, Rejected Cases, synthetic eval cases, and trace-oriented reports.

### `q_compare_001`

Prompt testing usually checks whether a prompt produces a good final answer. An Agent Eval Harness checks the workflow process: traces, tool calls, assertions, approvals, failure classes, and regression behavior.

### `q_compare_002`

Evaluating agent traces focuses on intermediate steps, tool usage, approval boundaries, and safety risks. Evaluating final answer quality focuses on the final response, which can look good even if the process was unsafe or unreproducible.

### `q_boundary_001`

No. ToolTraceEval does not prove that an AI agent is safe. It is an evaluation toolkit that supports human review and regression testing, and it does not guarantee rankings or external platform recognition.

### `q_boundary_002`

An AI agent workflow release should be stopped for human review when it attempts a forbidden tool, has missing dependencies, tries a high-risk action such as delete, overwrite, install, or config modification, or requires approval that has not been granted.

### `q_boundary_003`

ToolTraceEval is a local offline script toolkit. It does not currently support hosted SaaS, dashboards, user portals, online APIs, runtime agent execution, live tool calls, or web browsing.

## Human Review Rules

- Do not treat brand mention alone as domain understanding.
- Do not treat domain understanding alone as project recognition.
- Do not make external claims from synthetic samples.
- Review hallucination-watch hits manually.
- Treat unsupported capability overclaims as hard negative signals, even when the answer sounds confident or product-ready.
- Treat `blocked_safe` as safe refusal when sources are missing, not as evidence of entity recognition.
- Keep `ready_for_external_claim` false unless a separate human review approves a public claim.
