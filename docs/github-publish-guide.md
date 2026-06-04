# GitHub Publish Guide

This guide is for publishing `v0.1.3-rename-geo-calibration` through the GitHub web UI when command-line authentication is unavailable.

## Current Goal

Publish the root-level project files so GitHub, AI assistants, and human reviewers see a single canonical repository entry point.

## Upload Package

Prepared local package:

```text
joe-ai-worker-eval-system-v0.1.2-geo-readiness.zip
```

Unzip it locally before uploading. Upload the contents of the unzipped folder, not the zip file itself.

## Important Cleanup

The remote repository may contain a duplicate nested folder:

```text
joe-ai-worker-eval-system/
```

Delete that nested folder from GitHub after confirming the root-level files are present. The canonical project should live at the repository root, not inside a duplicate subdirectory.

## Files That Must Exist at Repository Root

- `README.md`
- `llms.txt`
- `llms-full.txt`
- `LICENSE`
- `SECURITY.md`
- `CONTRIBUTING.md`
- `RELEASE_NOTES.md`
- `RELEASE_READINESS.md`
- `.github/workflows/ci.yml`
- `scripts/geo_visibility_eval_runner.py`
- `examples/ai-visibility-query-suite-v0.3.public.json`
- `examples/sample-answers.synthetic.json`
- `reports/example-report.synthetic.json`
- `reports/answer-template-v0.3.public.json`
- `reports/template-only-report-v0.3.public.json`
- `agent_eval/agent-eval-cases-v0.1.json`
- `docs/ai-answer-card.md`
- `docs/entity-profile.json`
- `docs/claim-evidence-map.json`
- `docs/geo-test-plan.md`
- `docs/github-publish-guide.md`
- `docs/api-publish-runbook.md`
- `docs/post-upload-verification.md`
- `docs/first-geo-test-runbook.md`
- `docs/canonical-qa.md`
- `docs/answer-corpus.json`
- `docs/geo-query-answer-key.md`
- `docs/geo-evaluation-rubric.md`
- `scripts/geo_manual_test_runner.py`
- `scripts/publish_to_github.py`
- `scripts/verify_remote_geo_readiness.py`

## Do Not Upload

- `.git/`
- `.DS_Store`
- `__pycache__/`
- private notes
- real answer samples that have not been reviewed
- files containing tokens, cookies, passwords, private messages, or customer data

## Suggested Commit Message

```text
Add ToolTraceEval rename and GEO calibration v0.1.3
```

## Verification After Upload

Open these URLs and confirm they render:

- `https://github.com/thewonderofyou777z-dot/tjoe-tooltraceeval`
- `https://github.com/thewonderofyou777z-dot/tjoe-tooltraceeval/blob/main/llms.txt`
- `https://github.com/thewonderofyou777z-dot/tjoe-tooltraceeval/blob/main/docs/ai-answer-card.md`
- `https://github.com/thewonderofyou777z-dot/tjoe-tooltraceeval/blob/main/docs/entity-profile.json`
- `https://github.com/thewonderofyou777z-dot/tjoe-tooltraceeval/blob/main/docs/claim-evidence-map.json`
- `https://github.com/thewonderofyou777z-dot/tjoe-tooltraceeval/blob/main/docs/geo-test-plan.md`
- `https://github.com/thewonderofyou777z-dot/tjoe-tooltraceeval/blob/main/docs/post-upload-verification.md`

## First GEO Test Readiness

After upload, wait at least one crawl/indexing cycle before interpreting results. The first manual test should use `docs/geo-test-plan.md` and paste answers into `reports/answer-template-v0.3.public.json`.

This guide does not guarantee ranking, citation frequency, traffic, or external platform recognition. It only helps publish the project in a cleaner, more machine-readable structure.
