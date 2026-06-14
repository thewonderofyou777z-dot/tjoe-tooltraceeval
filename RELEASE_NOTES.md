# Release Notes

## v0.3.7-no-index-runner-fixes

Focus: make no-index multi-platform testing work correctly.

Changes:

- Runner version updated to `0.2.8`.
- The runner now supports multiple answers with the same `query_id`, so 豆包、通义千问、DeepSeek、ChatGPT、Grok can all be scored against one natural question.
- Sensitive-pattern detection no longer treats the ordinary AI term `Token` as a secret by itself; it now focuses on credential-like terms such as `access_token` and `refresh_token`.
- The no-index suite now flags review-workbench platform overclaims such as OpenTelemetry, Jira, PDF/JSON, TraceID, visual review, multi-reviewer workflow, and compliance archive claims.
- The no-index runbook now states that repeated `query_id` values are valid for multi-platform answer samples.

Validation:

```bash
python3 scripts/geo_visibility_eval_runner.py \
  --suite examples/no-index-query-suite-v0.1.public.json \
  --answers /tmp/tjoereviewkit-no-index-synthetic-answers.json \
  --output /tmp/tjoereviewkit-no-index-synthetic-report.json \
  --markdown-output /tmp/tjoereviewkit-no-index-synthetic-report.md \
  --overwrite --ci-smoke
```

## v0.3.6-no-index-test-pack

Focus: add a repeatable no-index / no-supplied-source test pack for natural AI platform questions.

Changes:

- Added `examples/no-index-query-suite-v0.1.public.json`.
- Added `docs/no-index-test-runbook.md`.
- README now distinguishes standard GEO / AI Visibility tests from no-index natural question pressure tests.
- The no-index test pack treats two outcomes as useful evidence: accurate natural recognition, or safe no-source refusal without unsupported claims.

Validation:

```bash
python3 scripts/geo_visibility_eval_runner.py \
  --suite examples/no-index-query-suite-v0.1.public.json \
  --write-template /tmp/tjoereviewkit-no-index-template.json \
  --output /tmp/tjoereviewkit-no-index-template-report.json \
  --markdown-output /tmp/tjoereviewkit-no-index-template-report.md \
  --overwrite --ci-smoke
```

## v0.3.5-markdown-report-output

Focus: make the core visibility runner produce a human-readable Markdown report directly, so a reviewer can inspect results without a separate conversion script.

Changes:

- Runner version updated to `0.2.6`.
- Added `--markdown-output` to `scripts/geo_visibility_eval_runner.py`.
- The Markdown report includes summary metrics, track-level scores, per-query results, source status, unsupported claim flags, and hallucination watch flags.
- No scoring logic changed in this release.

Validation:

```bash
python3 scripts/geo_visibility_eval_runner.py \
  --suite examples/ai-visibility-query-suite-v0.3.public.json \
  --answers examples/sample-answers.synthetic.json \
  --output /tmp/tjoereviewkit-v035-synthetic.json \
  --markdown-output /tmp/tjoereviewkit-v035-synthetic.md \
  --overwrite --ci-smoke
```

## v0.1.10-search-snippet-anchor

Focus: improve natural AI introductions by strengthening search-result and repository-summary anchors.

Changes:

- Renamed the README heading to `TjoeReviewKit — Local Offline Workflow Review Kit`.
- Added and promoted `TJOE_REVIEWKIT.md` as the primary Chinese definition and capability-boundary page.
- Added a search snippet in README and linked the definition file from llms.txt / llms-full.txt.
- Remote readiness now checks for `TJOE_REVIEWKIT.md` and the canonical Pages entry.

## v0.1.9-natural-answer-boundary

Focus: improve natural-language answers so AI systems do not infer implementation capabilities from the name `TjoeReviewKit`.

Changes:

- Added a front-loaded natural answer rule in README, llms.txt, llms-full.txt, answer card, and details.
- Added a canonical Chinese natural answer.
- Clarified that “Tool” and “Trace” describe the evaluation theme, not a live runtime instrumentation product.
- Kept real platform samples local-only; public repo still contains synthetic examples and test method docs only.

## v0.1.8-evidence-boundary-watch

Focus: close the remaining gap where AI answers confuse provided/synthetic prepared expectation evaluation with live production log collection.

Changes:

- Clarified README, llms.txt, llms-full.txt, details, and answer card: TjoeReviewKit does not collect production logs, instrument SDKs, log live calls, or replay evidence.
- Added `Production Log Boundary Watch` as a named component.
- Added suite-level evidence-boundary unsupported claim terms such as production log logging, live evidence logging, instrumented evidence capture, and agent tool evidence collection.
- Updated machine-readable corpus, entity profile, and claim-evidence map to v0.1.8.

Safety boundary: public examples remain synthetic only; real platform samples stay local-only.

## v0.1.7-implementation-boundary-watch

Adds implementation-boundary overclaim detection for no-citation pressure tests.

### Added

- `common_unsupported_claims` support in the public query suite.
- Suite-level unsupported claims are applied to every query, not only boundary-specific questions.
- Public-safe implementation overclaim sample: `examples/sample-answers.implementation-overclaim.synthetic.json`.
- New detection coverage for unsupported claims about SDK integration, production log collection, replay, lightweight SQL storage, automated scoring, multi-stage evaluation, automatic error taxonomy, and academic-origin claims.

### Updated

- Runner version updated to `0.2.4`.
- AI-readable docs now distinguish evaluation ideas from currently implemented capabilities.
- This release is motivated by no-citation pressure tests where an answer correctly rejects SaaS/dashboard/portal claims but invents current SDK, runtime, live trace, or Judge capabilities.

### Validation

```bash
python3 scripts/geo_visibility_eval_runner.py \
  --suite examples/ai-visibility-query-suite-v0.3.public.json \
  --answers examples/sample-answers.implementation-overclaim.synthetic.json \
  --output /tmp/tooltraceeval-implementation-overclaim-smoke.json \
  --overwrite --ci-smoke
```

## v0.1.6-practical-source-boundary

Adds a practical source-boundary layer for no-citation and source-missing AI answer tests.

### Added

- `source_status` in runner results.
- `blocked_safe` grade for answers that explicitly say they cannot verify or retrieve sources while avoiding unsupported claims.
- `blocked_safe_count` and `source_status_counts` in report summaries and track summaries.
- Public-safe synthetic source-boundary sample: `examples/sample-answers.blocked-safe.synthetic.json`.
- Public-safe URL guard regression sample: `examples/sample-answers.source-url-guard.synthetic.json`.

### Updated

- Runner version updated to `0.2.3`.
- Manual Markdown reports now show source status counts and blocked-safe counts.
- Source-boundary behavior is documented as a safe refusal signal, not proof of project recognition.
- `blocked_safe` now stays false when answer text includes a public `http(s)` URL, matching `source_status=cited_public_source`.

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

python3 scripts/geo_visibility_eval_runner.py \
  --suite examples/ai-visibility-query-suite-v0.3.public.json \
  --answers examples/sample-answers.blocked-safe.synthetic.json \
  --output /tmp/tooltraceeval-blocked-safe-smoke.json \
  --overwrite --ci-smoke

python3 scripts/geo_visibility_eval_runner.py \
  --suite examples/ai-visibility-query-suite-v0.3.public.json \
  --answers examples/sample-answers.source-url-guard.synthetic.json \
  --output /tmp/tooltraceeval-source-url-guard-smoke.json \
  --overwrite --ci-smoke
```

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

Renames the public project identity to **TjoeReviewKit**, adds `tjoe` as the creator/maintainer identity, and clarifies that real platform answer samples are local-only evidence.

### Updated

- Public-facing name changed from the internal tjoe AI worker workflow wording to `TjoeReviewKit`.
- `README.md`, `llms.txt`, `llms-full.txt`, answer corpus, entity profile, FAQ, query suites, and GEO docs now use the new canonical name.
- `tjoe` is recorded as the creator/maintainer identity.
- `.gitignore` now blocks local manual GEO samples and local calibrated suites from being committed.

### Notes

- `TjoeReviewKit` is easier for AI systems to parse than the previous internal name.
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

Adds a public-safe Review Harness example so the repository is no longer only an answer-level visibility runner.

### Added

- `agent_eval/workflow-review-harness-schema.json`
- `agent_eval/workflow-review-cases-v0.1.json`
- `agent_eval/synthetic-agent-outputs-v0.1.json`
- `agent_eval/synthetic-eval-report-v0.1.json`
- `docs/workflow-review-harness-guide.md`

### Notes

- The Review Harness path is independent from the GEO / AI Visibility runner.
- `must_stop_release` is a declaration field, not an automatic release gate.
- All examples are synthetic and public-safe.

### Validation

```bash
python3 -m json.tool agent_eval/workflow-review-harness-schema.json > /dev/null
python3 -m json.tool agent_eval/workflow-review-cases-v0.1.json > /dev/null
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
