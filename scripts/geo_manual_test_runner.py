#!/usr/bin/env python3
"""Manual GEO / AI visibility test helper.

This helper is intentionally offline:
- reads the public v0.3 query suite
- creates a paste-ready answer template
- validates manually pasted answer samples
- calls the local deterministic visibility runner
- writes a compact Markdown summary

It does not browse, log in, call models, scrape platforms, or publish results.
"""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import subprocess
import sys
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SUITE = REPO_ROOT / "examples" / "ai-visibility-query-suite-v0.3.public.json"
DEFAULT_TEMPLATE = REPO_ROOT / "reports" / "geo-manual-answer-template-v0.3.json"
DEFAULT_OUTPUT = REPO_ROOT / "reports" / "geo-manual-report-v0.3.json"
DEFAULT_MARKDOWN = REPO_ROOT / "reports" / "geo-manual-report-v0.3.md"
RUNNER = REPO_ROOT / "scripts" / "geo_visibility_eval_runner.py"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def flatten_queries(suite: dict[str, Any]) -> list[dict[str, Any]]:
    queries: list[dict[str, Any]] = []
    for group in suite.get("query_groups", []):
        for query in group.get("queries", []):
            item = dict(query)
            item["group_id"] = group.get("group_id")
            item["group_purpose"] = group.get("purpose")
            queries.append(item)
    return queries


def build_template(suite: dict[str, Any], platforms: list[str]) -> dict[str, Any]:
    answers = []
    for platform in platforms:
        for query in flatten_queries(suite):
            answers.append(
                {
                    "query_id": query["query_id"],
                    "platform": platform,
                    "answer": "",
                    "source_refs": [],
                    "manual_scores": {},
                    "notes": "",
                }
            )
    return {
        "template_id": f"geo_manual_answer_template_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "suite_id": suite.get("query_suite_id"),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "data_safety": {
            "contains_secret": False,
            "contains_private_message": False,
            "contains_customer_data": False,
            "contains_personal_data": False,
            "safe_to_share": "review_required",
            "safe_to_train": False,
            "review_required": True,
        },
        "instructions": [
            "Paste public AI answer text only.",
            "Do not include cookies, tokens, account identifiers, private messages, local paths, or customer data.",
            "Keep source_refs empty unless the platform provides public http(s) links.",
            "Leave answer empty for queries you did not run.",
        ],
        "platforms": platforms,
        "answers": answers,
    }


def validate_answers(path: Path, suite: dict[str, Any]) -> list[str]:
    payload = load_json(path)
    answers = payload.get("answers") if isinstance(payload, dict) else payload
    if not isinstance(answers, list):
        return ["answers must be a list or an object with an answers list"]

    known_query_ids = {query["query_id"] for query in flatten_queries(suite)}
    errors: list[str] = []
    for index, answer in enumerate(answers, start=1):
        if not isinstance(answer, dict):
            errors.append(f"answers[{index}] must be an object")
            continue
        query_id = answer.get("query_id")
        if query_id not in known_query_ids:
            errors.append(f"answers[{index}].query_id is unknown: {query_id}")
        if not answer.get("platform"):
            errors.append(f"answers[{index}].platform is required")
        if "answer" not in answer:
            errors.append(f"answers[{index}].answer is required, even if empty")
        source_refs = answer.get("source_refs", [])
        if not isinstance(source_refs, list):
            errors.append(f"answers[{index}].source_refs must be a list")
    return errors


def run_visibility_runner(suite: Path, answers: Path, output: Path) -> None:
    command = [
        sys.executable,
        str(RUNNER),
        "--suite",
        str(suite),
        "--answers",
        str(answers),
        "--output",
        str(output),
        "--overwrite",
        "--ci-smoke",
    ]
    subprocess.run(command, check=True)


def markdown_report(report: dict[str, Any], output_path: Path) -> str:
    summary = report.get("summary", {})
    lines = [
        "# GEO Manual Test Report",
        "",
        f"- Runner: `{report.get('runner')}`",
        f"- Runner version: `{report.get('runner_version')}`",
        f"- Suite: `{report.get('suite_id')}`",
        f"- Created at: `{report.get('created_at')}`",
        f"- Query count: `{report.get('query_count')}`",
        f"- Answer count: `{report.get('answer_count')}`",
        f"- Decision: `{summary.get('decision')}`",
        f"- Ready for external claim: `{summary.get('ready_for_external_claim')}`",
        "",
        "## Summary",
        "",
        f"- Answered count: `{summary.get('answered_count')}`",
        f"- Average total score: `{summary.get('average_total_score')}`",
        f"- Grade counts: `{json.dumps(summary.get('grade_counts', {}), ensure_ascii=False)}`",
        f"- Safety blocked count: `{summary.get('safety_blocked_count', 0)}`",
        f"- Hallucination watch count: `{summary.get('hallucination_watch_count', 0)}`",
        f"- Unsupported claim count: `{summary.get('unsupported_claim_count', 0)}`",
        "",
        "## Track Summary",
        "",
        "| Track | Answered | Average | Grades | Hallucination Watch | Unsupported Claims |",
        "|---|---:|---:|---|---:|---:|",
    ]
    for track, item in sorted(summary.get("track_summary", {}).items()):
        lines.append(
            "| {track} | {answered} | {avg} | `{grades}` | {hallucinations} | {unsupported} |".format(
                track=track,
                answered=item.get("answered_count", 0),
                avg=item.get("average_total_score", 0),
                grades=json.dumps(item.get("grade_counts", {}), ensure_ascii=False),
                hallucinations=item.get("hallucination_watch_count", 0),
                unsupported=item.get("unsupported_claim_count", 0),
            )
        )
    lines.extend(
        [
            "",
            "## Results",
            "",
            "| Query | Platform | Track | Grade | Score | Expected Hits | Watch | Unsupported Claims |",
            "|---|---|---|---|---:|---|---|---|",
        ]
    )
    for item in report.get("results", []):
        lines.append(
            "| {query} | {platform} | {track} | {grade} | {score}/{max_score} | {hits} | {watch} | {unsupported} |".format(
                query=item.get("query_id"),
                platform=item.get("platform"),
                track=item.get("scoring_track"),
                grade=item.get("grade"),
                score=item.get("total_score"),
                max_score=item.get("max_total"),
                hits=", ".join(item.get("expected_hits", [])) or "-",
                watch=", ".join(item.get("hallucination_hits", [])) or "-",
                unsupported=", ".join(
                    hit.get("failure_class", "unsupported_claim")
                    for hit in item.get("unsupported_claim_hits", [])
                ) or "-",
            )
        )
    lines.extend(
        [
            "",
            "## Interpretation Rules",
            "",
            "- Treat scores as internal heuristics, not proof of ranking, citation frequency, or platform recognition.",
            "- Review `hallucination_watch` hits manually before making any claim.",
            "- Treat `unsupported_claim_hits` as hard negative signals that require human review.",
            "- `ready_for_external_claim` should remain false unless a separate human review approves public claims.",
            "- Empty answers mean the query was not run or no answer was pasted.",
        ]
    )
    text = "\n".join(lines) + "\n"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8")
    return text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite", type=Path, default=DEFAULT_SUITE)
    parser.add_argument("--answers", type=Path)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--write-template", type=Path, default=None)
    parser.add_argument(
        "--platforms",
        default="chatgpt,perplexity,doubao,kimi",
        help="Comma-separated platform names for generated templates.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    suite = load_json(args.suite)
    platforms = [item.strip() for item in args.platforms.split(",") if item.strip()]

    if args.write_template:
        write_json(args.write_template, build_template(suite, platforms))
        print(json.dumps({"template": str(args.write_template), "platforms": platforms}, ensure_ascii=False, indent=2))
        return

    if not args.answers:
        raise SystemExit("Pass --answers or --write-template.")

    errors = validate_answers(args.answers, suite)
    if errors:
        raise SystemExit("Invalid answer sample: " + "; ".join(errors))

    run_visibility_runner(args.suite, args.answers, args.output)
    report = load_json(args.output)
    markdown_report(report, args.markdown)
    print(
        json.dumps(
            {
                "json_report": str(args.output),
                "markdown_report": str(args.markdown),
                "summary": report.get("summary", {}),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
