"""Collect frozen-system test evidence. Explicit live stages; no expected labels enter requests."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import shutil
import time

from ba_assistant import business_analysis as ba
from ba_assistant import ba_workflow as wf
ROOT = Path(__file__).resolve().parents[1]
COMPONENTS = ("requirements", "sources", "goals", "users", "team_roles", "conflicts",
              "questions", "answers", "specification", "tasks_and_criteria", "raci", "end_to_end")


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        handle.write(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verify(root):
    manifest = read(root / "collection.json")
    if sha(root / "dataset.json") != manifest["dataset_sha256"]:
        raise ValueError("Frozen test expectations changed")
    for name, expected in manifest["system"]["source_sha256"].items():
        # Publication edits to prose/config examples do not change the evaluated runtime.
        # Historical hashes remain intact; only executable files and web assets gate runs.
        if name in {"README.md", "SYSTEM.md", "AGENTS.md", ".env.example"}:
            continue
        migration_path = ROOT / "layout_migration.json"
        migration = read(migration_path)["files"] if migration_path.exists() else {}
        moved = migration.get(name)
        if moved:
            if moved["original_sha256"] != expected or sha(ROOT / moved["target"]) != moved["organized_sha256"]:
                raise ValueError(f"Organized implementation differs from its audited layout: {name}")
            continue
        if sha(ROOT / name) != expected:
            raise ValueError(f"Frozen implementation changed: {name}")
    return read(root / "dataset.json")


def prepare(dataset_path, root):
    dataset = read(dataset_path)
    if dataset.get("expectations_status") != "final" or any(c["expected"]["status"] != "final" for c in dataset["cases"]):
        raise ValueError("Final owner-approved expectations are required")
    ids = [c["case_id"] for c in dataset["cases"]]
    if len(ids) != len(set(ids)) or any(c["split"] != "test" for c in dataset["cases"]):
        raise ValueError("Use unique test case IDs")
    dev = read(ROOT / "dev/cases/ba_dev_cases.json")
    dev_groups = {c["group_id"] for c in dev["cases"]}
    dev_briefs = {c["input"]["initial_requirements"].strip() for c in dev["cases"]}
    if any(c["group_id"] in dev_groups or c["input"]["initial_requirements"].strip() in dev_briefs for c in dataset["cases"]):
        raise ValueError("Test/dev family or exact-brief overlap")
    root.mkdir(parents=True, exist_ok=False)
    shutil.copyfile(dataset_path, root / "dataset.json")
    system = read(ROOT / "dev/evaluation/final-system/v1.2-eval/manifest.json")
    write(root / "collection.json", {"started_at": wf.now(), "mode": "frozen_test_evaluation",
        "dataset_sha256": sha(root / "dataset.json"), "system": system,
        "rules": "No prompt tuning, no expected labels in input, no analysis retries, at most one RACI repair. Human approval is required before documents."})
    verify(root)
    write(root / "metrics.template.json", {"status": "awaiting_observations_and_human_review",
        "components": {key: {"numerator": None, "denominator": None, "value": None,
                              "status": "not_measured"} for key in COMPONENTS}})
    for case in dataset["cases"]:
        write(root / case["case_id"] / "expectations.json", case["expected"])
    return dataset


def sources_in(value, path="result"):
    if isinstance(value, dict):
        if "document" in value and "quote" in value:
            yield path, value
        for key, child in value.items():
            yield from sources_in(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from sources_in(child, f"{path}[{index}]")


def checks(analysis, sources, docs=None):
    quotes = [{"path": path, "source": source,
               "verbatim": isinstance(source.get("quote"), str) and bool(source["quote"].strip())
                    and source.get("document") in sources and source["quote"] in sources[source["document"]]}
              for path, source in sources_in(analysis)]
    if docs:
        quotes.extend({"path": path, "source": source,
                       "verbatim": isinstance(source.get("quote"), str) and bool(source["quote"].strip())
                           and source.get("document") in sources and source["quote"] in sources[source["document"]]}
                      for path, source in sources_in(docs, "documents"))
    result = {"quote_checks": quotes, "verbatim_quotes": {"numerator": sum(q["verbatim"] for q in quotes), "denominator": len(quotes)},
              "semantic_support": "requires_human_review", "extraction_recall_and_precision": "requires_semantic_matching",
              "counts": {key: len(value) for key, value in analysis.items() if isinstance(value, list)}}
    if docs:
        implementable = {r["id"] for r in analysis["requirements"] if r["kind"] != "constraint"}
        task_ids = {r["id"] for r in docs["tasks"]}
        roles = {r["id"] for r in analysis["team_roles"]}
        task_covered = {rid for task in docs["tasks"] for rid in task["requirement_ids"]}
        ac_covered = {ac["requirement_id"] for ac in docs["acceptance_criteria"]}
        result["document_coverage"] = {"implementable_ids": sorted(implementable),
            "task_covered_ids": sorted(implementable & task_covered), "criterion_covered_ids": sorted(implementable & ac_covered),
            "missing_task_ids": sorted(implementable - task_covered), "missing_criterion_ids": sorted(implementable - ac_covered)}
        result["raci_rows"] = [{"id": row["id"], "exactly_one_a": len(row["accountable"]) == 1,
            "at_least_one_r": bool(row["responsible"]), "task_links_exist": set(row["task_ids"]) <= task_ids,
            "role_links_exist": all(a["role_id"] in roles for code in ("accountable", "responsible", "consulted", "informed") for a in row[code])}
            for row in docs["raci"]]
    return result


def review_rows(analysis, sources, docs=None):
    rows = []
    for category in ("goals", "users", "team_roles", "requirements", "contradictions", "missing_information", "questions", "resolutions", "assumptions"):
        for item in analysis.get(category, []):
            rows.append({"category": category, "id": item.get("id", item.get("answer_id", "")), "output": item})
            for index, duty in enumerate(item.get("responsibilities", []), 1):
                rows.append({"category": category + "_responsibility", "id": f"{item['id']}.{index}", "output": duty})
    if docs:
        for category in ("tasks", "acceptance_criteria", "raci"):
            rows.extend({"category": category, "id": item["id"], "output": item} for item in docs[category])
    for row in rows:
        row.update(judgment="pending", source_support="pending", matched_expected_paths=[], notes="",
                   evidence=[{"path": p, **s} for p, s in sources_in(row["output"])])
    return {"status": "awaiting_human_review", "reviewer": None, "rows": rows,
            "missed_expectations": [], "unsupported_facts": [], "duplicate_questions": [],
            "end_to_end_mandatory_checks": [], "sources_available": list(sources)}


def run(root, case_id, stage, question_ids=(), reply_id=None, answers_file=None):
    dataset = verify(root)
    case = next(c for c in dataset["cases"] if c["case_id"] == case_id)
    case_root = root / case_id
    existing = sorted(case_root.glob("step-*"))
    step = case_root / f"step-{len(existing)+1:02d}-{stage}"
    step.mkdir(exist_ok=False)
    session_path = case_root / "current.session.json"
    session = read(session_path) if session_path.exists() else None
    if session and session["sources"]["brief"] != case["input"]["initial_requirements"].strip():
        raise ValueError("Session brief does not match the test case")
    if stage == "initial" and existing:
        raise ValueError("Initial run already attempted; do not cherry-pick a new response")
    if stage != "initial" and not session:
        raise ValueError("A validated initial session is required")
    if stage == "generate" and not session.get("approval"):
        raise ValueError("Review and approve the model requirements before generating documents")
    if stage == "generate" and (session.get("documents") or session.get("generation_progress", {}).get("raci_attempts", 0) >= 2):
        raise ValueError("This generation trajectory already ended; do not cherry-pick another output")
    ba.load_env()
    model = wf.ba.default_model()
    meta = {"case_id": case_id, "stage": stage, "origin": "live_api", "started_at": wf.now(),
            "model": session["model"] if session else model, "api_calls": 0, "status": "started"}
    request = ba.request_json
    captured = []
    def recorded(instructions, text, schema, requested_model, limit=6000):
        index = len(captured) + 1
        call = step / f"call-{index:02d}"
        call.mkdir()
        data = json.loads(text)
        # Auditable actual payload, never expected labels. It may contain only actual historical analysis.
        write(call / "input.json", data)
        write(call / "schema.json", schema)
        (call / "instructions.txt").write_text(instructions, encoding="utf-8")
        record = {"model": requested_model, "input_sha256": wf.digest(data), "started_at": wf.now()}
        captured.append(record)
        started = time.monotonic()
        try:
            result = request(instructions, text, schema, requested_model, limit)
            write(call / "output.raw.json", result)
            record["status"] = "response_received"
            return result
        except ValueError as exc:
            record.update(status="execution_failed", error=str(exc))
            raise
        finally:
            record["elapsed_seconds"] = round(time.monotonic() - started, 3)
            write(call / "run.json", record)
    ba.request_json = recorded
    try:
        if stage == "initial":
            updated = wf.start_session(case["input"]["initial_requirements"], model)
        elif stage == "clarify":
            if answers_file:
                if reply_id or question_ids:
                    raise ValueError("Use either explicit owner answers or prepared-reply routing")
                answers = read(answers_file)
                write(step / "routing.json", {"origin": "explicit_operator_supplied_answers", "answers": answers})
            else:
                prepared = next(a for a in case["conversation"]["prepared_answers"] if a["reply_id"] == reply_id)
                if not question_ids:
                    raise ValueError("Explicitly select actually asked question IDs; no automatic future-answer injection")
                write(step / "routing.json", {"prepared_reply_id": reply_id, "runtime_question_ids": question_ids,
                    "operator_selected": True, "text": prepared["text"]})
                answers = [{"question_id": q, "text": prepared["text"]} for q in question_ids]
            updated = wf.reply_many_to_session(session, answers)
        else:
            updated = wf.generate_documents(session)
            if updated.get("generation_progress", {}).get("raci_attempts") == 1:
                write(step / "first-attempt.session.json", updated)
                updated = wf.generate_documents(updated)
        write(step / "session.json", updated)
        wf.save_session(session_path, updated)
        write(step / "automatic-checks.json", checks(updated["analysis"], updated["sources"], updated.get("documents")))
        write(step / "manual-review.json", review_rows(updated["analysis"], updated["sources"], updated.get("documents")))
        meta.update(status="validated_result", blocking_reasons=wf.blocking_reasons(updated),
                    documents_present=bool(updated.get("documents")), generation_progress=updated.get("generation_progress"))
        if updated.get("documents"):
            (step / "documents.md").write_text(wf.render_documents(updated), encoding="utf-8")
    except ValueError as exc:
        meta.update(status="validation_failed" if isinstance(exc, ba.AnalysisValidationError) else "execution_failed",
                    errors=getattr(exc, "errors", [str(exc)]))
        # Invalid responses are still observations; retain quotes and manual-review rows when parseable.
        if captured:
            raw_path = step / f"call-{len(captured):02d}" / "output.raw.json"
            if raw_path.exists() and stage != "generate":
                output = read(raw_path)
                sources = read(raw_path.parent / "input.json")["sources"]
                if isinstance(output, dict):
                    write(step / "automatic-checks.json", checks(output, sources))
                    write(step / "manual-review.json", review_rows(output, sources))
    finally:
        ba.request_json = request
        meta.update(api_calls=len(captured), completed_at=wf.now())
        write(step / "run.json", meta)
    print(case_id, stage, meta["status"], f"calls={len(captured)}", flush=True)
    return meta


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["prepare", "initial", "clarify", "generate"])
    parser.add_argument("--directory", type=Path, required=True)
    parser.add_argument("--dataset", type=Path, default=ROOT / "tests/ba_test_cases.json")
    parser.add_argument("--case")
    parser.add_argument("--question", action="append", default=[])
    parser.add_argument("--prepared-reply")
    parser.add_argument("--answers-file", type=Path)
    args = parser.parse_args()
    if args.action == "prepare":
        data = prepare(args.dataset, args.directory)
        print(f"Prepared {len(data['cases'])} final test cases; no API calls")
    else:
        data = verify(args.directory)
        cases = [args.case] if args.case else [c["case_id"] for c in data["cases"]]
        if args.action != "initial" and not args.case:
            raise ValueError("Select one case for a clarification or document stage")
        for case_id in cases:
            run(args.directory, case_id, args.action, args.question, args.prepared_reply, args.answers_file)


if __name__ == "__main__":
    main()
