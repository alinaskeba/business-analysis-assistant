"""One live RACI-only repair of a preserved dev response. No hidden retries or approval."""
import copy
import hashlib
import json
from pathlib import Path
import shutil

import business_analysis as ba
import ba_workflow as wf
import plan_sources as ps
import staged_plan as st

ROOT = Path(__file__).resolve().parent
DEST = ROOT / "dev/evaluation/raci-repair-pass-01"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(name, value):
    (DEST / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def errors(plan, session):
    try:
        wf.validate_plan(plan, session)
        return []
    except ba.AnalysisValidationError as exc:
        return exc.errors


def main():
    DEST.mkdir(exist_ok=False)
    original = read(ROOT / "dev/evaluation/plan-pass-04-governance-clarified/input.json")
    baseline = read(ROOT / "dev/evaluation/plan-pass-06-final-validator/output.raw.json")
    # An experiment checkpoint, not a new user session or a claimed human approval.
    session = {"analysis": original["approved_analysis"], "sources": original["sources"],
               "replies": [], "revision": 1, "model": "gemini-3.1-flash-lite"}
    work = {k: copy.deepcopy(baseline[k]) for k in st.WORK_KEYS}
    st.validate_work(work, session, wf)
    before = errors(baseline, session)
    if not before:
        raise ValueError("Expected an invalid RACI baseline")
    session["generation_progress"] = {"status": "raci_failed", "revision_hash": wf.revision_hash(session),
        "configuration_hash": wf.digest({"stage_revision": st.REVISION, "prompt": wf.PLAN_INSTRUCTIONS,
                                          "schema": wf.PLAN_SCHEMA, "model": session["model"]}),
        "work_plan": work, "invalid_raci": {"raci": baseline["raci"]}, "errors": before, "raci_attempts": 1}
    save("baseline.raw.json", baseline)
    save("baseline-errors.json", before)
    save("original-input.json", original)
    for name in ("staged_plan.py", "plan_sources.py", "ba_workflow.py", "business_analysis.py", "run_raci_repair_eval.py"):
        shutil.copyfile(ROOT / name, DEST / name)
    run = {"origin": "live_api", "case_id": "PURE_002_without_team", "model": session["model"],
           "stage_revision": st.REVISION, "prompt_revision": wf.PLAN_PROMPT_REVISION,
           "checkpoint_origin": "reconstructed from preserved live output; not a new user approval",
           "started_at": wf.now(), "requests": 0, "retries": 0, "status": "running"}
    request = ba.request_json
    captured = {}
    def recorded(instructions, text, schema, model, limit=6000):
        run["requests"] += 1
        if run["requests"] != 1 or list(schema["properties"]) != ["raci"]:
            raise RuntimeError("Only one RACI-only request is authorized")
        save("request.input.json", json.loads(text))
        save("request.schema.json", schema)
        (DEST / "request.instructions.txt").write_text(instructions, encoding="utf-8")
        run["input_sha256"] = hashlib.sha256(text.encode()).hexdigest()
        response = request(instructions, text, schema, model, limit)
        captured["response"] = response
        save("response.raw.json", response)
        return response
    ba.load_env()
    ba.request_json = recorded
    try:
        plan, progress = st.generate(session, wf)
        if plan is not None:
            after = errors(plan, session)
            assert {k: plan[k] for k in st.WORK_KEYS} == work
            save("candidate.raw.json", plan)
            registry = ps.prepare_input(session["analysis"], session["sources"])["source_registry"]
            save("candidate.resolved.json", ps.hydrate(plan, registry))
            save("source-alignment-review.json", ps.alignment_review(plan, session["analysis"], session["sources"]))
            run["status"] = "passed_automated_checks_pending_semantic_review"
        else:
            after = progress["errors"]
            save("failed-progress.json", progress)
            run["status"] = "validation_or_execution_failed"
        save("comparison.json", {"baseline_errors": before, "candidate_errors": after,
             "work_unchanged": True, "work_note": "Frozen from the baseline, not regenerated or semantically repaired.",
             "baseline_activity_types": [r["activity_type"] for r in baseline["raci"]],
             "candidate_raci": captured.get("response"), "semantic_review": "pending"})
    except ValueError as exc:
        run.update(status="execution_failed", error=str(exc))
    finally:
        run["completed_at"] = wf.now()
        save("run.json", run)
    print(json.dumps(run))


if __name__ == "__main__":
    main()
