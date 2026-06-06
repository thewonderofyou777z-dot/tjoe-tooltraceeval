#!/usr/bin/env python3
"""Publish this package to GitHub using the Git Data API.

This script exists for environments where `git push` is not authenticated.
It reads a token from an environment variable or local token file, builds a
  root-level tree from this directory, and updates the target branch.

Safety defaults:
- dry-run by default unless --publish is passed
- never prints the token
- excludes .git, caches, pyc files, private reports, and secret-like filenames
- rebuilds the remote tree from root-level files only, which removes the old duplicated
  joe-ai-worker-eval-system/ subtree from the remote tree
"""

from __future__ import annotations

import argparse
import base64
import json
import os
from pathlib import Path
import sys
from typing import Any
from urllib.error import HTTPError
from urllib.request import Request, urlopen


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REPOSITORY = "thewonderofyou777z-dot/tjoe-reviewkit"
DEFAULT_BRANCH = "main"
API_ROOT = "https://api.github.com"
EXCLUDE_DIRS = {
    ".git",
    "__pycache__",
}
EXCLUDE_NAMES = {
    ".DS_Store",
}
EXCLUDE_SUFFIXES = {
    ".pyc",
}
EXCLUDE_NAME_FRAGMENTS = {
    "secret",
    "token",
    "cookie",
}
REQUIRED_ROOT_FILES = [
    "README.md",
    "llms.txt",
    "llms-full.txt",
    "docs/ai-answer-card.md",
    "docs/canonical-qa.md",
    "docs/answer-corpus.json",
    "docs/geo-query-answer-key.md",
    "docs/geo-evaluation-rubric.md",
    "docs/geo-test-plan.md",
    "docs/first-geo-test-runbook.md",
    "docs/api-publish-runbook.md",
    "scripts/geo_visibility_eval_runner.py",
    "scripts/geo_manual_test_runner.py",
    "scripts/verify_remote_geo_readiness.py",
]


def should_exclude(path: Path) -> bool:
    parts = set(path.parts)
    if parts & EXCLUDE_DIRS:
        return True
    if path.name in EXCLUDE_NAMES:
        return True
    if path.suffix in EXCLUDE_SUFFIXES:
        return True
    lower_name = path.name.lower()
    return any(fragment in lower_name for fragment in EXCLUDE_NAME_FRAGMENTS)


def collect_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if path.is_dir() or should_exclude(relative):
            continue
        files.append(relative)
    return sorted(files, key=lambda item: item.as_posix())


def read_token(args: argparse.Namespace) -> str:
    if args.token_file:
        token = Path(args.token_file).read_text(encoding="utf-8").strip()
    else:
        token = os.environ.get("GITHUB_TOKEN", "").strip()
    if not token:
        raise SystemExit("Missing token. Set GITHUB_TOKEN or pass --token-file.")
    return token


def github_request(
    token: str,
    method: str,
    path: str,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    body = None
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "joe-ai-worker-eval-system-publisher",
    }
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = Request(f"{API_ROOT}{path}", data=body, method=method, headers=headers)
    try:
        with urlopen(request, timeout=60) as response:
            data = response.read().decode("utf-8")
    except HTTPError as error:
        text = error.read().decode("utf-8", errors="replace")
        raise SystemExit(f"GitHub API {method} {path} failed: {error.code} {text}") from error
    return json.loads(data) if data else {}


def build_tree_entries(root: Path, files: list[Path]) -> list[dict[str, str]]:
    entries = []
    for relative in files:
        data = (root / relative).read_bytes()
        entries.append(
            {
                "path": relative.as_posix(),
                "mode": "100755" if os.access(root / relative, os.X_OK) else "100644",
                "type": "blob",
                "content": data.decode("utf-8"),
            }
        )
    return entries


def validate_file_set(files: list[Path]) -> list[str]:
    file_names = {path.as_posix() for path in files}
    errors = [f"missing required file: {item}" for item in REQUIRED_ROOT_FILES if item not in file_names]
    nested = [name for name in file_names if name.startswith("joe-ai-worker-eval-system/")]
    if nested:
        errors.append("package contains duplicated nested joe-ai-worker-eval-system/ paths")
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", default=DEFAULT_REPOSITORY)
    parser.add_argument("--branch", default=DEFAULT_BRANCH)
    parser.add_argument("--message", default="Add TjoeEvalKit public alias v0.2.0")
    parser.add_argument("--token-file")
    parser.add_argument("--publish", action="store_true", help="Actually update the remote branch.")
    parser.add_argument("--force", action="store_true", help="Force update the branch ref.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    files = collect_files(REPO_ROOT)
    errors = validate_file_set(files)
    summary = {
        "repository": args.repository,
        "branch": args.branch,
        "mode": "publish" if args.publish else "dry_run",
        "file_count": len(files),
        "required_errors": errors,
        "first_files": [path.as_posix() for path in files[:20]],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if errors:
        raise SystemExit("Refusing to continue because required file validation failed.")
    if not args.publish:
        return

    token = read_token(args)
    owner_repo = args.repository
    ref_path = f"/repos/{owner_repo}/git/ref/heads/{args.branch}"
    ref = github_request(token, "GET", ref_path)
    parent_sha = ref["object"]["sha"]
    parent_commit = github_request(token, "GET", f"/repos/{owner_repo}/git/commits/{parent_sha}")
    tree = github_request(
        token,
        "POST",
        f"/repos/{owner_repo}/git/trees",
        {"tree": build_tree_entries(REPO_ROOT, files)},
    )
    commit = github_request(
        token,
        "POST",
        f"/repos/{owner_repo}/git/commits",
        {
            "message": args.message,
            "tree": tree["sha"],
            "parents": [parent_sha],
        },
    )
    github_request(
        token,
        "PATCH",
        ref_path,
        {
            "sha": commit["sha"],
            "force": bool(args.force),
        },
    )
    print(
        json.dumps(
            {
                "published": True,
                "repository": args.repository,
                "branch": args.branch,
                "parent_sha": parent_sha,
                "commit_sha": commit["sha"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
