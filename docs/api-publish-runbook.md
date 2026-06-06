# API Publish Runbook

Use this runbook when normal `git push` authentication is unavailable.

## What This Does

`scripts/publish_to_github.py` publishes the current package root to the GitHub repository through the Git Data API.

It publishes only root-level project files. This intentionally removes the old duplicated remote subtree:

```text
joe-ai-worker-eval-system/
```

The script rebuilds the remote tree from the local package root instead of preserving unknown remote-only files.

## Safety Defaults

- Dry-run by default.
- Does not print the token.
- Excludes `.git/`, `.DS_Store`, `__pycache__/`, `.pyc`, and secret-like filenames.
- Refuses to continue if required GEO readiness files are missing.

## Dry Run

```bash
python3 scripts/publish_to_github.py
```

Expected result:

- `mode` is `dry_run`
- `required_errors` is empty
- `file_count` is greater than zero

## Publish With Environment Variable

```bash
GITHUB_TOKEN="YOUR_TOKEN_HERE" \
python3 scripts/publish_to_github.py --publish
```

## Publish With Local Credential File

Create a local file outside the repository, then run:

```bash
python3 scripts/publish_to_github.py \
  --token-file /path/to/local/token-file \
  --publish
```

After publishing, delete the local token file.

## Verify Remote

```bash
git ls-remote https://github.com/thewonderofyou777z-dot/tjoe-reviewkit.git refs/heads/main
```

Then confirm these files render on GitHub:

- `README.md`
- `llms.txt`
- `llms-full.txt`
- `docs/ai-answer-card.md`
- `docs/canonical-qa.md`
- `docs/geo-query-answer-key.md`
- `docs/first-geo-test-runbook.md`
- `scripts/geo_manual_test_runner.py`

Or run:

```bash
python3 scripts/verify_remote_geo_readiness.py
```

## Important

Do not commit tokens, cookies, private messages, customer data, or local-only paths. If a token is pasted into chat or committed accidentally, revoke it immediately.
