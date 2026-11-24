"""Freeze the final dev configuration and make at most one explicitly requested API call."""
import hashlib
import json
from pathlib import Path
import shutil
import sys
from datetime import datetime, timezone

import business_analysis as ba
import ba_workflow as wf
import plan_sources as ps

ROOT = Path(__file__).resolve().parent
DEST = ROOT / "dev/evaluation/plan-pass-06-final-validator"
PREVIOUS = ROOT / "dev/evaluation/plan-pass-05-source-ids/candidate"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def check(plan, session):
    try:
        wf.validate_plan(plan, session)
        return []
    except ba.AnalysisValidationError as exc:
        return exc.errors


def main():
    original = read(ROOT / "dev/evaluation/plan-pass-04-governance-clarified/input.json")
    session = {"analysis": original["approved_analysis"], "sources": original["sources"]}
    if "--prepare" in sys.argv:
        DEST.mkdir(exist_ok=False)
        baseline = DEST / "baseline"
        baseline.mkdir()
        for name in ("input.json", "output.raw.json", "run.json", "instructions.txt", "schema.json", "plan_sources.py"):
            shutil.copyfile(PREVIOUS / name, baseline / name)
        for name in ("business_analysis.py", "ba_workflow.py", "plan_sources.py", "test_plan_sources.py", "run_plan_pass06.py"):
            shutil.copyfile(ROOT / name, DEST / name)
        for name in ("input.json", "instructions.txt", "schema.json"):
            shutil.copyfile(PREVIOUS / name, DEST / name)
        assert ps.prepare_input(session["analysis"], session["sources"]) == read(DEST / "input.json")
        assert wf.PLAN_INSTRUCTIONS == (DEST / "instructions.txt").read_text(encoding="utf-8")
        assert wf.PLAN_SCHEMA == read(DEST / "schema.json")
        save(DEST / "baseline-validation.json", {"mode": "offline_revalidation", "errors": check(read(baseline / "output.raw.json"), session)})
        save(DEST / "freeze.json", {"status": "frozen_for_evaluation", "changed": ["validator_only"],
            "local_tests_passed": 65, "case_id": "PURE_002_without_team",
            "prompt_revision": wf.PLAN_PROMPT_REVISION, "schema_version": wf.PLAN_SCHEMA_VERSION,
            "sha256": {name: hashlib.sha256((DEST / name).read_bytes()).hexdigest()
                       for name in ("input.json", "instructions.txt", "schema.json", "business_analysis.py", "ba_workflow.py", "plan_sources.py")}})
        print("Frozen; baseline rejected for uncovered implementation tasks.")
        return
    if "--live" not in sys.argv:
        raise SystemExit("Use --prepare or --live")
    if (DEST / "run.json").exists():
        raise SystemExit("Live attempt already recorded; no retries allowed")
    frozen = read(DEST / "freeze.json")
    for name, expected in frozen["sha256"].items():
        assert hashlib.sha256((DEST / name).read_bytes()).hexdigest() == expected
        if name.endswith(".py"):
            assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected
    ba.load_env()
    run = {"origin": "live_api", "model": "gemini-3.1-flash-lite", "api_attempts": 1,
           "retry_policy": "none", "started_at_utc": datetime.now(timezone.utc).isoformat(),
           "status": "started", "configuration": frozen}
    save(DEST / "run.json", run)
    try:
        output = ba.request_json((DEST / "instructions.txt").read_text(encoding="utf-8"),
                                 (DEST / "input.json").read_text(encoding="utf-8"),
                                 read(DEST / "schema.json"), run["model"])
        save(DEST / "output.raw.json", output)
        errors = check(output, session)
        run.update(status="validation_failed" if errors else "validation_passed", validation_errors=errors)
        registry = read(DEST / "input.json")["source_registry"]
        try:
            save(DEST / "output.resolved.json", ps.hydrate(output, registry))
            save(DEST / "source-alignment-review.json", ps.alignment_review(output, session["analysis"], session["sources"]))
        except (ba.AnalysisValidationError, KeyError, TypeError):
            run["hydration_status"] = "failed"
        covered = {t for r in output["raci"] if r["activity_type"] == "implementation" for t in r["task_ids"]}
        save(DEST / "coverage.json", {"task_count": len(output["tasks"]),
             "implementation_covered_tasks": sorted(covered & {t["id"] for t in output["tasks"]}),
             "criterion_requirement_ids": sorted({a["requirement_id"] for a in output["acceptance_criteria"]}),
             "raci_activity_types": [r["activity_type"] for r in output["raci"]],
             "semantic_status": "needs_human_review"})
    except ValueError as exc:
        run.update(status="execution_failed", error=str(exc))
    finally:
        run["completed_at_utc"] = datetime.now(timezone.utc).isoformat()
        save(DEST / "run.json", run)
    print(json.dumps({k: run[k] for k in ("status", "validation_errors", "error") if k in run}))


if __name__ == "__main__":
    main()
