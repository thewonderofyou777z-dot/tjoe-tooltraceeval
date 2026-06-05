#!/usr/bin/env python3
"""Offline GEO / AI visibility eval runner.

This runner is intentionally safe by default:
- reads a query suite JSON
- optionally reads pasted AI answer samples
- scores answer inclusion with deterministic heuristics or manual scores
- never logs in, never browses, never calls models, never publishes

Version: 0.2.3
"""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import re
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SUITE = REPO_ROOT / "examples" / "ai-visibility-query-suite-v0.3.public.json"
DEFAULT_OUTPUT = REPO_ROOT / "reports" / "example-report.synthetic.json"
DEFAULT_TEMPLATE = REPO_ROOT / "reports" / "answer-template.json"
VERSION = "0.2.3"
SCORE_FIELDS = [
    "mention_score",
    "understanding_score",
    "citation_score",
    "conversion_score",
]
DEFAULT_SCORING_TRACK = "brand_entity_exact"
ENTITY_TERMS = [
    "joe ai worker",
    "joe ai worker eval",
    "agent eval harness",
    "agent output adapter",
    "local agent eval runner",
    "eval suite",
    "runner report",
    "must_stop_release",
    "requires_approval",
    "rejected case",
    "failure class",
    "llm_wiki",
    "qwen",
    "qwen2.5",
    "local model governance",
    "本地模型治理",
    "agent eval",
    "eval harness",
    "output adapter",
]
CONVERSION_TERMS = [
    "demo",
    "template",
    "contact",
    "try",
    "run",
    "next step",
    "get started",
    "download",
    "book",
    "schedule",
    "测试",
    "模板",
    "运行",
    "接入",
    "试用",
    "下载",
    "联系",
    "预约",
    "下一步",
    "查看报告",
    "运行评测",
]
URL_PATTERN = re.compile(r"https?://")
SENSITIVE_PATTERN = re.compile(
    r"(password|passwd|api[_-]?key|secret|token|cookie|bearer|sk-[a-zA-Z0-9]|"
    r"private[_-]?key|\\.pem|localhost:\\d+|127\\.0\\.0\\.1:\\d+)",
    re.IGNORECASE,
)
SAFE_BLOCK_PATTERNS = [
    "cannot verify",
    "can't verify",
    "cannot confirm",
    "can't confirm",
    "unable to verify",
    "无法核验",
    "无法确认",
    "不能确认",
    "无法直接核验",
    "没有可核验",
    "缺少来源",
    "没有来源",
    "不能只依据",
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def ensure_can_write(path: Path, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"Output already exists: {path}. Pass --overwrite to replace it.")


def flatten_queries(suite: dict[str, Any]) -> list[dict[str, Any]]:
    queries: list[dict[str, Any]] = []
    for group in suite.get("query_groups", []):
        for query in group.get("queries", []):
            item = dict(query)
            item["group_id"] = group.get("group_id")
            item["group_purpose"] = group.get("purpose")
            queries.append(item)
    return queries


def validate_suite(suite: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(suite.get("query_groups"), list) or not suite.get("query_groups"):
        errors.append("suite.query_groups must be a non-empty list")
        return errors

    seen_query_ids: set[str] = set()
    for group_index, group in enumerate(suite["query_groups"], start=1):
        if not isinstance(group, dict):
            errors.append(f"query_groups[{group_index}] must be an object")
            continue
        if not isinstance(group.get("queries"), list) or not group.get("queries"):
            errors.append(f"query_groups[{group_index}].queries must be a non-empty list")
            continue
        for query_index, query in enumerate(group["queries"], start=1):
            location = f"query_groups[{group_index}].queries[{query_index}]"
            if not isinstance(query, dict):
                errors.append(f"{location} must be an object")
                continue
            query_id = query.get("query_id")
            if not query_id:
                errors.append(f"{location}.query_id is required")
            elif query_id in seen_query_ids:
                errors.append(f"{location}.query_id is duplicated: {query_id}")
            else:
                seen_query_ids.add(str(query_id))
            if not query.get("zh") and not query.get("en"):
                errors.append(f"{location} must include zh or en")
            expected = query.get("expected_answer_elements")
            if not isinstance(expected, list) or not expected:
                errors.append(f"{location}.expected_answer_elements must be a non-empty list")
            track_terms = query.get("track_terms")
            if track_terms is not None and not isinstance(track_terms, list):
                errors.append(f"{location}.track_terms must be a list when provided")
            hallucination_watch = query.get("hallucination_watch")
            if hallucination_watch is not None and not isinstance(hallucination_watch, list):
                errors.append(f"{location}.hallucination_watch must be a list when provided")
    return errors


def normalize_answers(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, dict) and isinstance(payload.get("answers"), list):
        return payload["answers"]
    if isinstance(payload, list):
        return payload
    raise ValueError("Answer sample must be a list or an object with an answers list.")


def generate_answer_template(suite: dict[str, Any]) -> dict[str, Any]:
    answers: list[dict[str, Any]] = []
    for query in flatten_queries(suite):
        answers.append(
            {
                "query_id": query["query_id"],
                "platform": "manual_paste",
                "answer": "",
                "source_refs": [],
                "manual_scores": {},
                "notes": "",
            }
        )
    return {
        "template_id": f"ai_answer_sample_template_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "suite_id": suite.get("query_suite_id"),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "data_safety": {
            "contains_secret": False,
            "contains_private_message": False,
            "contains_customer_data": False,
            "contains_personal_data": False,
            "safe_to_share": "internal_only",
            "safe_to_train": False,
            "review_required": True,
        },
        "instructions": [
            "Paste public AI answer text only.",
            "Do not include cookies, tokens, accounts, private messages, or customer data.",
            "Use manual_scores only if a human reviewer intentionally overrides heuristic scoring.",
        ],
        "answers": answers,
    }


def clamp_score(value: Any) -> int | None:
    if value is None:
        return None
    try:
        score = int(value)
    except (TypeError, ValueError):
        return None
    return max(0, min(3, score))


def keyword_hits(text: str, terms: list[str]) -> list[str]:
    lower_text = text.lower()
    return [term for term in terms if term.lower() in lower_text]


def expected_hits(text: str, query: dict[str, Any]) -> list[str]:
    lower_text = text.lower()
    hits: list[str] = []
    for element in query.get("expected_answer_elements", []):
        if isinstance(element, dict):
            canonical = str(element.get("canonical") or element.get("name") or "")
            aliases = element.get("aliases", [])
            candidates = [canonical] + [str(alias) for alias in aliases if alias]
            if canonical and any(candidate.lower() in lower_text for candidate in candidates if candidate):
                hits.append(canonical)
        elif str(element).lower() in lower_text:
            hits.append(str(element))
    return hits


def scoring_track(query: dict[str, Any]) -> str:
    return str(query.get("scoring_track") or DEFAULT_SCORING_TRACK)


def query_terms(query: dict[str, Any]) -> list[str]:
    terms = query.get("track_terms")
    if isinstance(terms, list) and terms:
        return [str(term) for term in terms]
    return ENTITY_TERMS


def hallucination_hits(text: str, query: dict[str, Any]) -> list[str]:
    watch_terms = query.get("hallucination_watch", [])
    if not isinstance(watch_terms, list):
        return []
    return keyword_hits(text, [str(term) for term in watch_terms])


def unsupported_claim_hits(text: str, query: dict[str, Any]) -> list[dict[str, str]]:
    claims = query.get("unsupported_claims", [])
    if not isinstance(claims, list):
        return []

    lower_text = text.lower()
    hits: list[dict[str, str]] = []
    for claim in claims:
        if isinstance(claim, dict):
            claim_id = str(claim.get("claim_id") or claim.get("name") or "unsupported_claim")
            terms = claim.get("terms", [])
            failure_class = str(claim.get("failure_class") or claim_id)
            if not isinstance(terms, list):
                continue
            matched = [str(term) for term in terms if str(term).lower() in lower_text]
            if matched:
                hits.append(
                    {
                        "claim_id": claim_id,
                        "failure_class": failure_class,
                        "matched_terms": ", ".join(matched),
                    }
                )
        elif str(claim).lower() in lower_text:
            hits.append(
                {
                    "claim_id": str(claim),
                    "failure_class": "unsupported_claim",
                    "matched_terms": str(claim),
                }
            )
    return hits


def public_source_refs(refs: Any) -> list[str]:
    if not isinstance(refs, list):
        return []
    return [
        str(ref)
        for ref in refs
        if isinstance(ref, str) and ref.startswith(("http://", "https://"))
    ]


def safety_findings(answer: dict[str, Any]) -> list[str]:
    findings: list[str] = []
    text = str(answer.get("answer", ""))
    refs = answer.get("source_refs", [])
    if SENSITIVE_PATTERN.search(text):
        findings.append("sensitive_pattern_in_answer")
    if isinstance(refs, list):
        for ref in refs:
            ref_text = str(ref)
            if SENSITIVE_PATTERN.search(ref_text):
                findings.append("sensitive_pattern_in_source_ref")
                break
        if refs and len(public_source_refs(refs)) < len(refs):
            findings.append("non_public_source_ref_ignored")
    return findings


def source_status_for(answer: dict[str, Any]) -> str:
    text = str(answer.get("answer", ""))
    refs = answer.get("source_refs", [])
    has_public_refs = bool(public_source_refs(refs))
    has_any_refs = isinstance(refs, list) and bool(refs)
    mentions_url = bool(URL_PATTERN.search(text))
    lower_text = text.lower()

    if has_public_refs or mentions_url:
        return "cited_public_source"
    if has_any_refs:
        return "non_public_source_ignored"
    if any(pattern in lower_text for pattern in SAFE_BLOCK_PATTERNS):
        return "source_not_retrieved"
    return "no_source_provided"


def is_blocked_safe_answer(answer: dict[str, Any], unsupported_claims: list[dict[str, str]]) -> bool:
    text = str(answer.get("answer", "")).strip()
    if not text or unsupported_claims:
        return False
    if public_source_refs(answer.get("source_refs", [])):
        return False
    if URL_PATTERN.search(text):
        return False
    lower_text = text.lower()
    return any(pattern in lower_text for pattern in SAFE_BLOCK_PATTERNS)


def heuristic_scores(answer: dict[str, Any], query: dict[str, Any]) -> dict[str, int]:
    text = str(answer.get("answer", ""))
    refs = answer.get("source_refs", [])
    entity_hits = keyword_hits(text, query_terms(query))
    expectation_hits = expected_hits(text, query)
    conversion_hits = keyword_hits(text, CONVERSION_TERMS)

    mention_score = 0
    if len(entity_hits) >= 3:
        mention_score = 3
    elif len(entity_hits) == 2:
        mention_score = 2
    elif len(entity_hits) == 1:
        mention_score = 1
    elif expectation_hits:
        mention_score = 1

    total_expected = max(1, len(query.get("expected_answer_elements", [])))
    coverage = len(expectation_hits) / total_expected
    understanding_score = 0
    if coverage >= 0.75:
        understanding_score = 3
    elif coverage >= 0.5:
        understanding_score = 2
    elif coverage > 0:
        understanding_score = 1
    understanding_score = min(3, understanding_score)

    citation_score = 0
    public_refs = public_source_refs(refs)
    if len(public_refs) >= 2:
        citation_score = 3
    elif public_refs:
        citation_score = 2
    elif URL_PATTERN.search(text):
        citation_score = 1

    conversion_score = 0
    has_refs = isinstance(refs, list) and bool(refs)
    if len(conversion_hits) >= 2 and has_refs:
        conversion_score = 3
    elif len(conversion_hits) >= 2:
        conversion_score = 2
    elif conversion_hits:
        conversion_score = 1

    return {
        "mention_score": mention_score,
        "understanding_score": understanding_score,
        "citation_score": citation_score,
        "conversion_score": conversion_score,
    }


def citation_note_for(answer: dict[str, Any]) -> str | None:
    refs = answer.get("source_refs", [])
    if isinstance(refs, list) and refs and not public_source_refs(refs):
        return "source_refs were provided but ignored because they were not public http(s) URLs."
    if isinstance(refs, list) and refs and len(public_source_refs(refs)) < len(refs):
        return "Only public http(s) source_refs were counted for citation_score."
    return None


def score_answer(answer: dict[str, Any], query: dict[str, Any]) -> dict[str, Any]:
    findings = safety_findings(answer)
    answer_text = str(answer.get("answer", ""))
    hallucinations = hallucination_hits(answer_text, query)
    unsupported_claims = unsupported_claim_hits(answer_text, query)
    source_status = source_status_for(answer)
    blocked_safe = is_blocked_safe_answer(answer, unsupported_claims)
    if any(finding.startswith("sensitive_pattern") for finding in findings):
        return {
            "query_id": query.get("query_id"),
            "platform": answer.get("platform", "unknown"),
            "group_id": query.get("group_id"),
            "scoring_track": scoring_track(query),
            "scores": {field: 0 for field in SCORE_FIELDS},
            "total_score": 0,
            "max_total": 12,
            "grade": "blocked",
            "source_status": source_status,
            "expected_hits": [],
            "entity_hits": [],
            "manual_override_fields": [],
            "has_answer": bool(str(answer.get("answer", "")).strip()),
            "safety_blocked": True,
            "safety_findings": findings,
            "hallucination_hits": hallucinations,
            "hallucination_watch_triggered": bool(hallucinations),
            "unsupported_claim_hits": unsupported_claims,
            "unsupported_claim_triggered": bool(unsupported_claims),
            "blocked_safe": False,
            "citation_note": citation_note_for(answer),
            "notes": answer.get("notes", ""),
        }

    scores = heuristic_scores(answer, query)
    manual_scores = answer.get("manual_scores", {})
    manual_override_fields: list[str] = []
    if isinstance(manual_scores, dict):
        for field in SCORE_FIELDS:
            override = clamp_score(manual_scores.get(field))
            if override is not None:
                scores[field] = override
                manual_override_fields.append(field)

    total = sum(scores.values())
    max_total = 12
    if unsupported_claims:
        total = 0
        grade = "overclaim"
    elif blocked_safe:
        total = 0
        grade = "blocked_safe"
    elif total >= 9:
        grade = "strong"
    elif total >= 6:
        grade = "partial"
    elif total >= 3:
        grade = "weak"
    else:
        grade = "miss"

    return {
        "query_id": query.get("query_id"),
        "platform": answer.get("platform", "unknown"),
        "group_id": query.get("group_id"),
        "scoring_track": scoring_track(query),
        "scores": scores,
        "total_score": total,
        "max_total": max_total,
        "grade": grade,
        "source_status": source_status,
        "expected_hits": expected_hits(str(answer.get("answer", "")), query),
        "entity_hits": keyword_hits(str(answer.get("answer", "")), query_terms(query)),
        "manual_override_fields": manual_override_fields,
        "has_answer": bool(str(answer.get("answer", "")).strip()),
        "safety_blocked": False,
        "safety_findings": findings,
        "hallucination_hits": hallucinations,
        "hallucination_watch_triggered": bool(hallucinations),
        "unsupported_claim_hits": unsupported_claims,
        "unsupported_claim_triggered": bool(unsupported_claims),
        "blocked_safe": blocked_safe,
        "citation_note": citation_note_for(answer),
        "notes": answer.get("notes", ""),
    }


def summarize(results: list[dict[str, Any]]) -> dict[str, Any]:
    answered = [item for item in results if item["has_answer"]]
    if not answered:
        return {
            "answered_count": 0,
            "average_total_score": 0,
            "grade_counts": {},
            "ready_for_external_claim": False,
            "decision": "template_only",
        }

    grade_counts: dict[str, int] = {}
    for item in answered:
        grade_counts[item["grade"]] = grade_counts.get(item["grade"], 0) + 1
    average = round(sum(item["total_score"] for item in answered) / len(answered), 2)
    blocked_count = grade_counts.get("blocked", 0)
    non_public_ref_count = sum(
        1
        for item in answered
        if "non_public_source_ref_ignored" in item.get("safety_findings", [])
    )
    hallucination_watch_count = sum(1 for item in answered if item.get("hallucination_watch_triggered"))
    unsupported_claim_count = sum(1 for item in answered if item.get("unsupported_claim_triggered"))
    blocked_safe_count = sum(1 for item in answered if item.get("blocked_safe"))
    source_status_counts: dict[str, int] = {}
    for item in answered:
        status = str(item.get("source_status") or "unknown")
        source_status_counts[status] = source_status_counts.get(status, 0) + 1
    track_summary: dict[str, dict[str, Any]] = {}
    for item in answered:
        track = str(item.get("scoring_track") or DEFAULT_SCORING_TRACK)
        bucket = track_summary.setdefault(
            track,
            {
                "answered_count": 0,
                "average_total_score": 0,
                "grade_counts": {},
                "hallucination_watch_count": 0,
                "unsupported_claim_count": 0,
                "blocked_safe_count": 0,
                "source_status_counts": {},
            },
        )
        bucket["answered_count"] += 1
        bucket["average_total_score"] += item["total_score"]
        bucket["grade_counts"][item["grade"]] = bucket["grade_counts"].get(item["grade"], 0) + 1
        if item.get("hallucination_watch_triggered"):
            bucket["hallucination_watch_count"] += 1
        if item.get("unsupported_claim_triggered"):
            bucket["unsupported_claim_count"] += 1
        if item.get("blocked_safe"):
            bucket["blocked_safe_count"] += 1
        status = str(item.get("source_status") or "unknown")
        bucket["source_status_counts"][status] = bucket["source_status_counts"].get(status, 0) + 1
    for bucket in track_summary.values():
        if bucket["answered_count"]:
            bucket["average_total_score"] = round(
                bucket["average_total_score"] / bucket["answered_count"],
                2,
            )
    return {
        "answered_count": len(answered),
        "average_total_score": average,
        "grade_counts": grade_counts,
        "ready_for_external_claim": False,
        "safety_blocked_count": blocked_count,
        "non_public_ref_count": non_public_ref_count,
        "hallucination_watch_count": hallucination_watch_count,
        "unsupported_claim_count": unsupported_claim_count,
        "blocked_safe_count": blocked_safe_count,
        "source_status_counts": source_status_counts,
        "track_summary": track_summary,
        "decision": "internal_eval_only",
    }


def build_report(
    suite: dict[str, Any],
    answers: list[dict[str, Any]] | None,
    template_path: Path | None,
) -> dict[str, Any]:
    queries = flatten_queries(suite)
    answer_by_id = {answer.get("query_id"): answer for answer in answers or []}
    results = [
        score_answer(answer_by_id.get(query["query_id"], {}), query)
        for query in queries
    ]
    return {
        "runner": "geo_visibility_eval_runner.py",
        "runner_version": VERSION,
        "run_id": f"geo_visibility_eval_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "suite_id": suite.get("query_suite_id"),
        "suite_status": suite.get("status"),
        "query_count": len(queries),
        "answer_count": len(answers or []),
        "template_path": str(template_path) if template_path else None,
        "summary": summarize(results),
        "results": results,
        "scoring_model": {
            "version": VERSION,
            "note": "Scores are deterministic heuristic indicators for internal evaluation, not proof of real GEO visibility.",
            "track_rule": "brand_entity_exact and domain_concept_discovery are reported separately when scoring_track is present.",
            "citation_rule": "Only public http(s) source_refs count toward citation_score.",
            "understanding_rule": "understanding_score is based solely on expected_answer_elements coverage; entity_hits no longer affect this score. It is not a substitute for human quality review.",
            "unsupported_claim_rule": "unsupported_claims are hard negative signals. If an answer asserts explicitly unsupported capabilities, the result grade becomes overclaim and total_score is set to 0.",
            "source_boundary_rule": "Answers that explicitly say they cannot verify or cannot retrieve sources are graded blocked_safe when they avoid unsupported claims. This is a safe refusal signal, not evidence of project recognition.",
        },
        "safety": {
            "no_login": True,
            "no_network": True,
            "no_model_call": True,
            "no_external_publish": True,
            "safe_to_share": "internal_only",
            "safe_to_train": False,
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite", type=Path, default=DEFAULT_SUITE)
    parser.add_argument("--answers", type=Path, default=None)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--write-template", type=Path, default=None)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--ci-smoke", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    suite = load_json(args.suite)
    if not isinstance(suite, dict) or "query_groups" not in suite:
        raise ValueError("Suite must be a JSON object with query_groups.")
    suite_errors = validate_suite(suite)
    if suite_errors:
        raise SystemExit("Invalid query suite: " + "; ".join(suite_errors))

    answers = None
    template_path = None
    if args.write_template:
        ensure_can_write(args.write_template, args.overwrite)
        template = generate_answer_template(suite)
        args.write_template.parent.mkdir(parents=True, exist_ok=True)
        args.write_template.write_text(
            json.dumps(template, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        template_path = args.write_template

    if args.answers:
        answers = normalize_answers(load_json(args.answers))

    ensure_can_write(args.output, args.overwrite)
    report = build_report(suite, answers, template_path)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        json.dumps(
            {
                "runner_version": VERSION,
                "output": str(args.output),
                "query_count": report["query_count"],
                "answer_count": report["answer_count"],
                "summary": report["summary"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )

    if args.ci_smoke:
        if report["query_count"] <= 0:
            raise SystemExit("CI smoke failed: query_count must be > 0")
        if validate_suite(suite):
            raise SystemExit("CI smoke failed: suite validation failed")


if __name__ == "__main__":
    main()
