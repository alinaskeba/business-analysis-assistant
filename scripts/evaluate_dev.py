"""Offline structural evaluation and human-review checklist; never calls an LLM."""
import argparse
import json
from pathlib import Path

from ba_assistant import ba_workflow as wf
COMPONENTS = ("initial_analysis", "clarification", "updated_requirements", "specification",
              "tasks", "acceptance_criteria", "raci", "end_to_end")


def evaluate(dataset, sessions_dir):
    report = {"mode": "offline_artifact_review", "expectations_status": dataset["expectations_status"],
              "semantic_quality": "not_measured; human review required", "api_calls": 0, "cases": []}
    for case in dataset["cases"]:
        row = {"case_id": case["case_id"], "group_id": case["group_id"], "split": case["split"],
               "components": {key: "not_run" for key in COMPONENTS}, "errors": [],
               "human_checks": {"initial_analysis": case.get("expected_initial_analysis", {}),
                                "journey": case["expected_journey"]},
               "findings": {"correct": [], "omissions": [], "unsupported_facts": [],
                            "status": "awaiting_human_review"}}
        path = Path(sessions_dir) / (case["case_id"] + ".session.json")
        failure = Path(sessions_dir) / (case["case_id"] + ".failure.json")
        if failure.exists():
            row["execution_failure"] = json.loads(failure.read_text(encoding="utf-8"))
            row["errors"].append("Recorded execution failure; not a semantic model-quality judgment")
        if path.exists():
            try:
                session = wf.validate_session(json.loads(path.read_text(encoding="utf-8")))
                if session["sources"]["brief"] != case["input"]["initial_requirements"].strip():
                    raise ValueError("Session brief does not match this dataset case")
                row["model"] = session["model"]
                row["execution_mode"] = session.get("execution_mode", "unknown")
                row["events"] = session["events"]
                # Check every recorded analysis, including intermediate revisions.
                for snapshot in session["history"]:
                    available = {key: session["sources"][key] for key in snapshot["source_ids"]}
                    replies = [reply for reply in session["replies"] if reply["id"] in available]
                    wf.validate_updated_analysis(snapshot["analysis"], available, replies, session["question_history"])
                row["components"]["initial_analysis"] = "structural_pass; semantic_review_needed"
                row["components"]["clarification"] = "structural_pass; semantic_review_needed"
                if session["replies"]:
                    row["components"]["updated_requirements"] = "structural_pass; semantic_review_needed"
                row["blocking_reasons"] = wf.blocking_reasons(session)
                if session["documents"]:
                    wf.render_documents(session)
                    for component in ("specification", "tasks", "acceptance_criteria", "raci", "end_to_end"):
                        row["components"][component] = "structural_pass; semantic_review_needed"
                elif row["blocking_reasons"]:
                    for component in ("specification", "tasks", "acceptance_criteria", "raci", "end_to_end"):
                        row["components"][component] = "blocked; documents_not_generated"
            except (ValueError, KeyError, TypeError) as exc:
                row["errors"].append(str(exc))
                row["artifact_validation"] = "failed"
        report["cases"].append(row)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=Path(__file__).resolve().parents[1] / "dev/cases/ba_dev_cases.json")
    parser.add_argument("--sessions", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    dataset = json.loads(args.dataset.read_text(encoding="utf-8-sig"))
    report = evaluate(dataset, args.sessions)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    # Do not overwrite an earlier evaluation artifact.
    with args.report.open("x", encoding="utf-8") as handle:
        handle.write(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(f"Offline report saved: {args.report}; {len(report['cases'])} cases; no API calls")


if __name__ == "__main__":
    main()
