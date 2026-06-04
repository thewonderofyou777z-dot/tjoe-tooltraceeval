# Release Notes

## v0.1.5-practical-overclaim-watch

Adds a practical unsupported capability watch layer for AI visibility testing.

### Added

- `unsupported_claims` support in the public query suite.
- `unsupported_claim_hits` and `unsupported_claim_triggered` in runner output.
- `overclaim` grade for answers that assert explicitly unsupported capabilities.
- Public-safe synthetic negative sample: `examples/sample-answers.overclaim.synthetic.json`.
- New boundary query `q_boundary_003` for hosted SaaS, dashboard, portal, online API, runtime execution, live tool calls, and web browsing.

### Updated

- Runner version updated to `0.2.2`.
- Manual Markdown reports now show unsupported claim counts.
- Rubric, answer corpus, entity profile, and claim-evidence map now describe unsupported capability overclaims.

### Validation

```bash
python3 scripts/geo_visibility_eval_runner.py \
  --suite examples/ai-visibility-query-suite-v0.3.public.json \
  --answers examples/sample-answers.synthetic.json \
  --output reports/example-report.synthetic.json \
  --overwrite --ci-smoke

python3 scripts/geo_visibility_eval_runner.py \
  --suite examples/ai-visibility-query-suite-v0.3.public.json \
  --answers examples/sample-answers.overclaim.synthetic.json \
  --output /tmp/tooltraceeval-overclaim-smoke.json \
  --overwrite --ci-smoke
```

## v0.1.3-rename-geo-calibration

Renames the public project identity to **ToolTraceEval**, adds `tjoe` as the creator/maintainer identity, and clarifies that real platform answer samples are local-only evidence.

### Updated

- Public-facing name changed from the internal tjoe AI worker workflow wording to `ToolTraceEval`.
- `README.md`, `llms.txt`, `llms-full.txt`, answer corpus, entity profile, FAQ, query suites, and GEO docs now use the new canonical name.
- `tjoe` is recorded as the creator/maintainer identity.
- `.gitignore` now blocks local manual GEO samples and local calibrated suites from being committed.

### Notes

- `ToolTraceEval` is easier for AI systems to parse than the previous internal name.
- Real ChatGPT / Perplexity / Doubao / Kimi answer samples are local-only review evidence by default.
- Public reports remain synthetic-only unless manually reviewed and intentionally promoted.

### Validation

```bash
python3 scripts/geo_visibility_eval_runner.py \
  --suite examples/ai-visibility-query-suite-v0.3.public.json \
  --answers examples/sample-answers.synthetic.json \
  --output reports/example-report.synthetic.json \
  --overwrite --ci-smoke
```

## v0.1.1-public-draft

Adds a public-safe Agent Eval Harness example so the repository is no longer only an answer-level visibility runner.

### Added

- `agent_eval/agent-eval-harness-schema.json`
- `agent_eval/agent-eval-cases-v0.1.json`
- `agent_eval/synthetic-agent-outputs-v0.1.json`
- `agent_eval/synthetic-eval-report-v0.1.json`
- `docs/agent-eval-harness-guide.md`

### Notes

- The Agent Eval Harness path is independent from the GEO / AI Visibility runner.
- `must_stop_release` is a declaration field, not an automatic release gate.
- All examples are synthetic and public-safe.

### Validation

```bash
python3 -m json.tool agent_eval/agent-eval-harness-schema.json > /dev/null
python3 -m json.tool agent_eval/agent-eval-cases-v0.1.json > /dev/null
python3 -m json.tool agent_eval/synthetic-agent-outputs-v0.1.json > /dev/null
python3 -m json.tool agent_eval/synthetic-eval-report-v0.1.json > /dev/null
python3 -m json.tool docs/faq.schema.json > /dev/null
```

## v0.1.0-public-draft

Initial GitHub-ready public draft.

### Included

- `README.md`
- `docs/details.md`
- `docs/faq.schema.json`
- `scripts/geo_visibility_eval_runner.py`
- `examples/ai-visibility-query-suite-v0.2.public.json`
- `examples/sample-answers.synthetic.json`
- `SECURITY.md`

### Boundaries

- No ranking promises.
- No absolute safety claims.
- No private data.
- No platform recognition claims.

### Validation

The synthetic example should pass with:

```bash
python3 scripts/geo_visibility_eval_runner.py \
  --suite examples/ai-visibility-query-suite-v0.2.public.json \
  --answers examples/sample-answers.synthetic.json \
  --output reports/example-report.synthetic.json \
  --overwrite --ci-smoke
```
