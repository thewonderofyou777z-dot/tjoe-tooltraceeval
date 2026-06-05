# GEO Manual Test Report

- Runner: `geo_visibility_eval_runner.py`
- Runner version: `0.2.3`
- Suite: `ai_visibility_query_suite_v0_3_public_geo_readiness`
- Created at: `2026-06-05T15:51:28`
- Query count: `10`
- Answer count: `10`
- Decision: `internal_eval_only`
- Ready for external claim: `False`

## Summary

- Answered count: `10`
- Average total score: `6.2`
- Grade counts: `{"partial": 10}`
- Safety blocked count: `0`
- Hallucination watch count: `0`
- Unsupported claim count: `0`
- Blocked safe count: `0`
- Source status counts: `{"no_source_provided": 10}`

## Track Summary

| Track | Answered | Average | Grades | Hallucination Watch | Unsupported Claims | Blocked Safe | Source Status |
|---|---:|---:|---|---:|---:|---:|---|
| brand_entity_exact | 2 | 7.0 | `{"partial": 2}` | 0 | 0 | 0 | `{"no_source_provided": 2}` |
| comparison | 2 | 6.0 | `{"partial": 2}` | 0 | 0 | 0 | `{"no_source_provided": 2}` |
| domain_concept_discovery | 3 | 6.0 | `{"partial": 3}` | 0 | 0 | 0 | `{"no_source_provided": 3}` |
| safety_boundary | 3 | 6.0 | `{"partial": 3}` | 0 | 0 | 0 | `{"no_source_provided": 3}` |

## Results

| Query | Platform | Track | Grade | Source Status | Score | Expected Hits | Watch | Unsupported Claims |
|---|---|---|---|---|---:|---|---|---|
| q_domain_001 | synthetic | domain_concept_discovery | partial | no_source_provided | 6/12 | Function Calling Safety, Tool Trace, Human Approval, Regression Testing, Audit Log | - | - |
| q_domain_002 | synthetic | domain_concept_discovery | partial | no_source_provided | 6/12 | Traceability, Replay, Forbidden Tool Detection | - | - |
| q_domain_003 | synthetic | domain_concept_discovery | partial | no_source_provided | 6/12 | Risk Classification, Requires Approval, Stop or Review | - | - |
| q_entity_001 | synthetic | brand_entity_exact | partial | no_source_provided | 7/12 | ToolTraceEval, Agent Eval Harness, Agent Output Adapter, Local Eval Runner, AI Visibility Query Suite | - | - |
| q_entity_002 | synthetic | brand_entity_exact | partial | no_source_provided | 7/12 | Agent Eval Harness, Agent Output Adapter, Local Eval Runner, Claim Watch, Rejected Cases | - | - |
| q_compare_001 | synthetic | comparison | partial | no_source_provided | 6/12 | Trace and Tool Calls, Assertions, Regression | - | - |
| q_compare_002 | synthetic | comparison | partial | no_source_provided | 6/12 | Intermediate Steps, Tool Use, Final Answer | - | - |
| q_boundary_001 | synthetic | safety_boundary | partial | no_source_provided | 6/12 | Evaluation Toolkit, Human Review, No Ranking Guarantee | - | - |
| q_boundary_002 | synthetic | safety_boundary | partial | no_source_provided | 6/12 | Forbidden Tool, Missing Dependency, High Risk Action | - | - |
| q_boundary_003 | synthetic | safety_boundary | partial | no_source_provided | 6/12 | No SaaS, No Dashboard Or Portal, No Runtime Execution | - | - |

## Interpretation Rules

- Treat scores as internal heuristics, not proof of ranking, citation frequency, or platform recognition.
- Review `hallucination_watch` hits manually before making any claim.
- Treat `unsupported_claim_hits` as hard negative signals that require human review.
- Treat `blocked_safe` as a safe refusal / source-boundary signal, not evidence that the project is recognized.
- `ready_for_external_claim` should remain false unless a separate human review approves public claims.
- Empty answers mean the query was not run or no answer was pasted.
