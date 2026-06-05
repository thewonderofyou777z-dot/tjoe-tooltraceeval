#!/usr/bin/env python3
"""Verify remote GitHub GEO readiness after publishing.

This script uses public GitHub API endpoints first and falls back to a shallow
git clone when public API rate limits are hit. It does not need a token.
It verifies that the repository root exposes the expected AI-readable files and
that the old duplicated joe-ai-worker-eval-system/ subtree is gone.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import tempfile
from typing import Any
from urllib.error import HTTPError
from urllib.request import Request, urlopen


DEFAULT_REPOSITORY = "thewonderofyou777z-dot/tjoe-tooltraceeval"
DEFAULT_BRANCH = "main"
API_ROOT = "https://api.github.com"
REQUIRED_FILES = [
    "WHAT_IS_TOOLTRACEEVAL.md",
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
    "docs/entity-profile.json",
    "docs/claim-evidence-map.json",
    "scripts/geo_visibility_eval_runner.py",
    "scripts/geo_manual_test_runner.py",
]
REQUIRED_TEXT_MARKERS = {
    "WHAT_IS_TOOLTRACEEVAL.md": ["What is tjoe ToolTraceEval?", "not a runtime trace collector"],
    "README.md": ["English summary", "v0.1.10-search-snippet-anchor"],
    "llms.txt": ["ToolTraceEval", "machine-readable navigation aid"],
    "llms-full.txt": ["Canonical One-Sentence Answer", "Unsupported Claim Watch"],
    "docs/canonical-qa.md": ["What is ToolTraceEval?", "shortest accurate description"],
    "docs/answer-corpus.json": ["tooltraceeval_answer_corpus_v0_1_10", "canonical_questions"],
    "docs/geo-query-answer-key.md": ["q_domain_001", "q_boundary_002"],
    "docs/geo-evaluation-rubric.md": ["Review Dimensions", "Unsupported capability handling"],
    "docs/first-geo-test-runbook.md": ["Generate A Manual Answer Template", "Run The Offline Report"],
}


class GitHubApiError(RuntimeError):
    pass


def github_get(path: str) -> Any:
    request = Request(
        f"{API_ROOT}{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "joe-ai-worker-remote-verifier",
        },
    )
    try:
        with urlopen(request, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        text = error.read().decode("utf-8", errors="replace")
        raise GitHubApiError(f"GitHub API GET {path} failed: {error.code} {text}") from error


def raw_get(repository: str, branch: str, path: str) -> str:
    url = f"https://raw.githubusercontent.com/{repository}/{branch}/{path}"
    request = Request(url, headers={"User-Agent": "joe-ai-worker-remote-verifier"})
    try:
        with urlopen(request, timeout=60) as response:
            return response.read().decode("utf-8")
    except HTTPError as error:
        return ""


def collect_via_api(repository: str, branch_name: str) -> tuple[str, set[str], dict[str, str]]:
    branch = github_get(f"/repos/{repository}/branches/{branch_name}")
    tree_sha = branch["commit"]["commit"]["tree"]["sha"]
    tree = github_get(f"/repos/{repository}/git/trees/{tree_sha}?recursive=1")
    files = flatten_tree(tree.get("tree", []))
    contents = {
        path: raw_get(repository, branch_name, path)
        for path in REQUIRED_TEXT_MARKERS
    }
    return str(branch["commit"]["sha"]), files, contents


def collect_via_git(repository: str, branch_name: str) -> tuple[str, set[str], dict[str, str]]:
    url = f"https://github.com/{repository}.git"
    with tempfile.TemporaryDirectory(prefix="geo-remote-verify-") as temp_dir:
        clone_dir = Path(temp_dir) / "repo"
        subprocess.run(
            [
                "git",
                "clone",
                "--depth",
                "1",
                "--branch",
                branch_name,
                url,
                str(clone_dir),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
        )
        commit_sha = subprocess.check_output(
            ["git", "-C", str(clone_dir), "rev-parse", "HEAD"],
            text=True,
        ).strip()
        files = {
            path.relative_to(clone_dir).as_posix()
            for path in clone_dir.rglob("*")
            if path.is_file() and ".git" not in path.relative_to(clone_dir).parts
        }
        contents: dict[str, str] = {}
        for path in REQUIRED_TEXT_MARKERS:
            file_path = clone_dir / path
            contents[path] = file_path.read_text(encoding="utf-8") if file_path.exists() else ""
        return commit_sha, files, contents


def flatten_tree(items: list[dict[str, Any]]) -> set[str]:
    return {str(item.get("path")) for item in items if item.get("type") == "blob"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", default=DEFAULT_REPOSITORY)
    parser.add_argument("--branch", default=DEFAULT_BRANCH)
    parser.add_argument("--strategy", choices=["auto", "api", "git"], default="auto")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    strategy_used = args.strategy
    try:
        if args.strategy == "git":
            commit_sha, files, contents = collect_via_git(args.repository, args.branch)
        else:
            commit_sha, files, contents = collect_via_api(args.repository, args.branch)
            strategy_used = "api"
    except GitHubApiError as error:
        if args.strategy == "api":
            raise SystemExit(str(error)) from error
        commit_sha, files, contents = collect_via_git(args.repository, args.branch)
        strategy_used = "git_fallback"

    missing = [path for path in REQUIRED_FILES if path not in files]
    duplicated_nested = sorted(path for path in files if path.startswith("joe-ai-worker-eval-system/"))

    marker_failures: dict[str, list[str]] = {}
    for path, markers in REQUIRED_TEXT_MARKERS.items():
        content = contents.get(path, "")
        absent = [marker for marker in markers if marker not in content]
        if absent:
            marker_failures[path] = absent

    passed = not missing and not duplicated_nested and not marker_failures
    report = {
        "repository": args.repository,
        "branch": args.branch,
        "strategy": strategy_used,
        "commit_sha": commit_sha,
        "passed": passed,
        "required_file_count": len(REQUIRED_FILES),
        "missing_required_files": missing,
        "duplicated_nested_files": duplicated_nested[:50],
        "duplicated_nested_count": len(duplicated_nested),
        "marker_failures": marker_failures,
        "next_action": "ready_for_first_geo_test" if passed else "publish_or_cleanup_required",
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
