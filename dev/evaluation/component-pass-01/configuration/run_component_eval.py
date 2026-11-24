"""Explicit live component experiment. Inputs must be prepared separately from labels."""
import argparse
import hashlib
import json
from pathlib import Path
import time

import business_analysis as ba
import ba_workflow as wf


def write(path, value):
    with Path(path).open("x", encoding="utf-8") as handle:
        handle.write(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def run(directory, stage):
    root = Path(directory)
    ba.load_env()
    import os
    model = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")
    dataset = json.loads((root / "dataset.json").read_text(encoding="utf-8"))
    if dataset["expectations_status"] != "final":
        raise ValueError("This experiment requires reviewed final expectations")
    for case in dataset["cases"]:
        target = root / case["case_id"] / stage
        target.mkdir(parents=True, exist_ok=True)
        if (target / "run.json").exists():
            raise ValueError("Run already exists; do not overwrite experiment artifacts")
        if stage == "initial":
            sources = {"brief": case["input"]["initial_requirements"].strip()}
            data = {"sources": sources, "replies": [], "previous_analysis": None, "previously_asked_questions": {}}
            schema, prompt = wf.ANALYSIS_SCHEMA, wf.ANALYSIS_INSTRUCTIONS
            validator = lambda result: wf.validate_updated_analysis(result, sources, [], {})
        else:
            reference = json.loads((root / case["case_id"] / "reference.json").read_text(encoding="utf-8"))
            sources = reference["sources"]
            if stage == "clarification":
                data = {"sources": sources, "replies": reference["replies"],
                        "previous_analysis": reference["initial_analysis"],
                        "previously_asked_questions": reference["question_history"]}
                schema, prompt = wf.ANALYSIS_SCHEMA, wf.ANALYSIS_INSTRUCTIONS
                validator = lambda result: wf.validate_updated_analysis(result, sources, reference["replies"], reference["question_history"])
            else:
                if case["case_id"].endswith("unresolved"):
                    write(target / "run.json", {"stage": stage, "status": "not_applicable",
                                               "reason": "Unresolved conflict: final document generation must not run", "api_calls": 0})
                    continue
                data = {"approved_analysis": reference["clarified_analysis"], "sources": sources}
                schema, prompt = wf.PLAN_SCHEMA, wf.PLAN_INSTRUCTIONS
                validator = lambda result: wf.validate_plan(result, {"analysis": reference["clarified_analysis"], "sources": sources})
        write(target / "input.json", data)
        meta = {"case_id": case["case_id"], "stage": stage, "model": model, "origin": "live_api",
                "started_at_utc": wf.now(), "input_sha256": wf.digest(data),
                "prompt_sha256": wf.digest(prompt), "schema_sha256": wf.digest(schema),
                "prompt_revision": wf.PROMPT_REVISION, "attempts": []}
        result = None
        for attempt in range(1, 3):
            started = time.monotonic()
            try:
                result = ba.request_json(prompt, json.dumps(data, ensure_ascii=False), schema, model, 16000)
            except ValueError as exc:
                meta["attempts"].append({"attempt": attempt, "status": "execution_failure", "error": str(exc),
                                         "elapsed_seconds": round(time.monotonic() - started, 3)})
                if attempt == 1 and ("HTTP 503" in str(exc) or "timeout" in str(exc)):
                    continue
                meta["status"] = "execution_failure"
                break
            else:
                meta["attempts"].append({"attempt": attempt, "status": "response_received",
                                         "elapsed_seconds": round(time.monotonic() - started, 3)})
                write(target / "output.json", result)
                try:
                    validator(result)
                except ba.AnalysisValidationError as exc:
                    meta.update(status="validation_failed", validation_errors=exc.errors)
                else:
                    meta.update(status="validation_passed", validation_errors=[])
                break
        meta["completed_at_utc"] = wf.now()
        write(target / "run.json", meta)
        print(case["case_id"], stage, meta["status"], flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, required=True)
    parser.add_argument("--stage", choices=["initial", "clarification", "plan"], required=True)
    args = parser.parse_args()
    run(args.directory, args.stage)
