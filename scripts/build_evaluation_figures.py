"""Reproduce descriptive evaluation figures from preserved outputs, without any API calls."""
import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from scripts import collect_test_evaluation as collect
ROOT = Path(__file__).resolve().parents[1]
PASS = ROOT / "tests/evaluation/pass-01"
ASSISTED = ROOT / "tests/evaluation/pass-01-assisted-library"
OUT = PASS / "report-assets"


def rate(numerator, denominator):
    return {"numerator": numerator, "denominator": denominator,
            "value": numerator / denominator if denominator else None}


def finish(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / f"{name}.png", dpi=220, bbox_inches="tight")
    fig.savefig(OUT / f"{name}.svg", bbox_inches="tight")
    plt.close(fig)


def main():
    collect.verify(PASS)
    OUT.mkdir(exist_ok=True)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                         "axes.spines.top": False, "axes.spines.right": False})
    rows = []
    for file in sorted(PASS.glob("*/step-*/run.json")):
        run = collect.read(file)
        automatic = collect.read(file.parent / "automatic-checks.json")
        q = automatic["verbatim_quotes"]
        rows.append({"case": run["case_id"], "stage": run["stage"], "status": run["status"],
                     "quotes_correct": q["numerator"], "quotes_total": q["denominator"],
                     "api_calls": run["api_calls"]})
    qn, qd = sum(r["quotes_correct"] for r in rows), sum(r["quotes_total"] for r in rows)
    labels = [("Library" if "library" in r["case"] else "Equipment") + "\n" + r["stage"] for r in rows]
    fig, ax = plt.subplots(figsize=(8.7, 4.5))
    bars = ax.bar(labels, [r["quotes_correct"] / r["quotes_total"] * 100 for r in rows],
                  color=["#3274a1" if r["quotes_correct"] == r["quotes_total"] else "#d18a32" for r in rows])
    for bar, row in zip(bars, rows):
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+1,
                f"{row['quotes_correct']}/{row['quotes_total']}", ha="center")
    ax.set(ylim=(0, 112), ylabel="Exact quote occurrences (%)", title="Quote fidelity in original test trajectories")
    ax.text(0, -.24, "Exact substrings only; semantic support is a separate manual check.", transform=ax.transAxes, fontsize=9)
    finish(fig, "quote_fidelity")

    initial = []
    for case in collect.read(PASS / "dataset.json")["cases"]:
        result = collect.read(PASS / case["case_id"] / "step-01-initial/call-01/output.raw.json")
        initial.append((case, result))
    categories = ["requirements", "goals", "users", "team_roles", "questions"]
    fig, ax = plt.subplots(figsize=(8.7, 4.5))
    positions = np.arange(len(categories))
    for index, (case, result) in enumerate(initial):
        values = [len(result[key]) for key in categories]
        bars = ax.bar(positions + (index-.5)*.36, values, width=.36,
                      label="Library" if "library" in case["case_id"] else "Equipment")
        ax.bar_label(bars)
    ax.set_xticks(positions, ["Requirements", "Goals", "Users", "Team roles", "Questions"])
    ax.set(ylabel="Output record count", ylim=(0, 10), title="Initial extraction: descriptive counts, not quality scores")
    ax.legend(frameon=False)
    finish(fig, "initial_record_counts")

    # Exact matching of the approved incompatible source pair, not a general semantic judge.
    tp = fp = fn = clean_correct = 0
    for case, result in initial:
        expected = {tuple(sorted((c["statement_a"], c["statement_b"]))) for c in case["expected"]["initial_analysis"]["conflicts"]}
        reqs = {r["id"]: r for r in result["requirements"]}
        found = [tuple(sorted(reqs[rid]["source"]["quote"] for rid in c["requirement_ids"])) for c in result["contradictions"]]
        matched = set(found) & expected
        tp += len(matched); fp += len(found)-len(matched); fn += len(expected-matched)
        clean_correct += int(not expected and not found)
    # Explicit assisted annotation against the six already-approved equipment gold units.
    # The coordinator-review action is present in users but absent as a standalone requirement.
    equipment_case, equipment_output = next((c, r) for c, r in initial if "equipment" in c["case_id"])
    gold_units = equipment_case["expected"]["initial_analysis"]["requirements_to_cover"]
    matched_ids = ["R1", "R2", "R3", None, "R4", "R5"]
    assert len(gold_units) == len(matched_ids) == 6
    annotation = {"status": "single_assistant_manual_matching",
        "rule": "Facts must match the full brief; standalone requirement coverage is separate from quote support and atomicity.",
        "gold_matches": [{"expected": gold, "output_id": rid} for gold, rid in zip(gold_units, matched_ids)],
        "correct_output_ids": ["R1", "R2", "R3", "R4", "R5"],
        "precision": rate(5, len(equipment_output["requirements"])), "recall": rate(5, len(gold_units))}
    (OUT / "equipment-requirement-matching.json").write_text(json.dumps(annotation, indent=2)+"\n", encoding="utf-8")
    fig, ax = plt.subplots(figsize=(7, 4.2))
    values = [annotation["precision"], annotation["recall"]]
    bars = ax.bar(["Precision", "Recall"], [r["value"]*100 for r in values], color=["#3274a1", "#d18a32"])
    for bar, value in zip(bars, values): ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+1, f"{value['numerator']}/{value['denominator']}", ha="center")
    ax.set(ylim=(0, 114), ylabel="Percent", title="Equipment initial requirements: assisted semantic matching")
    ax.text(0, -.20, "One case only; single assistant-assisted assessment.\nCoordinator-review requirement omitted; citation support scored separately.", transform=ax.transAxes, fontsize=9)
    finish(fig, "equipment_requirement_metrics")
    equipment = PASS / "TEST_002_equipment_unresolved"
    e0 = collect.read(equipment / "step-01-initial/session.json")
    e1 = collect.read(equipment / "step-02-clarify/session.json")
    unchanged = sum(r in e1["analysis"]["requirements"] for r in e0["analysis"]["requirements"])
    guards = collect.read(equipment / "blocking-checks.json")

    fig, ax = plt.subplots(figsize=(9, 3.8))
    ax.set_xlim(-.7, 3.7); ax.set_ylim(-.7, 1.7)
    cells = [
        ["Pass", "Quote error\n(original run failed)", "Not reached", "Not reached"],
        ["Pass", "Decision remains open", "Blocked as required\n(local guard)", "Blocked as required\n(local guard)"]]
    colors = [["#d7eee4", "#f4d8d8", "#e8ecf2", "#e8ecf2"], ["#d7eee4"]*4]
    for row in range(2):
        y = 1-row
        for column in range(4):
            ax.add_patch(plt.Rectangle((column-.46, y-.28), .92, .56, color=colors[row][column]))
            ax.text(column, y, cells[row][column], ha="center", va="center", fontsize=9)
    ax.set_xticks(range(4), ["Initial analysis", "Clarification", "Approval", "Final documents"])
    ax.set_yticks([1, 0], ["Library", "Equipment"])
    ax.set_title("Original scenario progression; editorial branch excluded")
    for spine in ax.spines.values(): spine.set_visible(False)
    ax.tick_params(length=0)
    finish(fig, "scenario_progression")

    approved = collect.read(ASSISTED / "documents-02/approved.session.json")
    work = collect.read(ASSISTED / "documents-02/call-01/output.raw.json")
    implementable = {r["id"] for r in approved["analysis"]["requirements"] if r["kind"] != "constraint"}
    task_ids = {rid for t in work["tasks"] for rid in t["requirement_ids"]}
    ac_ids = {a["requirement_id"] for a in work["acceptance_criteria"]}
    tc, ac = len(implementable & task_ids), len(implementable & ac_ids)
    fig, ax = plt.subplots(figsize=(7, 4.2))
    bars = ax.bar(["Task links", "Criterion links"], [tc/len(implementable)*100, ac/len(implementable)*100], color="#5478a9")
    for bar, value in zip(bars, [tc, ac]): ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+1, f"{value}/{len(implementable)}", ha="center")
    ax.set(ylim=(0, 114), ylabel="Implementable requirement IDs covered (%)", title="Assisted work-stage output: link coverage only")
    ax.text(0, -.20, "No final package: repeated performance question blocked RACI.\nID coverage does not establish criterion correctness.", transform=ax.transAxes, fontsize=9)
    finish(fig, "assisted_link_coverage")

    calls = []
    for origin, directory in [("original", PASS), ("assisted", ASSISTED)]:
        for file in sorted(directory.glob("**/call-*/run.json")):
            r = collect.read(file)
            calls.append({"origin": origin, "artifact": str(file.relative_to(ROOT)),
                          "elapsed_seconds": r["elapsed_seconds"], "status": r["status"]})
    fig, ax = plt.subplots(figsize=(9, 4.2))
    ax.bar(range(1, len(calls)+1), [r["elapsed_seconds"] for r in calls],
           color=["#3274a1" if r["origin"] == "original" else "#d18a32" for r in calls])
    ax.set(xlabel="Recorded request (grouped by original / assisted)", ylabel="Seconds", title="Observed API response time; one observation per request")
    ax.set_xticks(range(1, len(calls)+1))
    finish(fig, "request_latency")
    total_seconds = sum(r["elapsed_seconds"] for r in calls)
    metrics = {"scope": "Original test trajectories and separate owner-assisted recovery, not pooled scenario success",
        "original_quote_fidelity": rate(qn, qd),
        "original_response_structural_pass": rate(sum(r["status"] == "validated_result" for r in rows), len(rows)),
        "conflict_pair_precision": rate(tp, tp+fp), "conflict_pair_recall": rate(tp, tp+fn),
        "conflict_pair_counts": {"tp": tp, "fp": fp, "fn": fn, "clean_cases_without_false_conflicts": clean_correct},
        "equipment_requirement_matching": annotation,
        "unchanged_equipment_requirements": rate(unchanged, len(e0["analysis"]["requirements"])),
        "equipment_approval_blocked": guards["approval"]["blocked"], "equipment_generation_blocked": guards["generation"]["blocked"],
        "library_unassisted_documents": "not_reached_after_invalid_clarification",
        "assisted_task_id_coverage": rate(tc, len(implementable)), "assisted_criterion_id_coverage": rate(ac, len(implementable)),
        "assisted_documents": "not_finalized_due_to_repeated_nonessential_performance_question",
        "raci_quality": None, "requirement_precision_and_recall": None, "full_semantic_source_support": None,
        "live_api_calls": len(calls), "original_calls": sum(r["origin"] == "original" for r in calls),
        "assisted_calls": sum(r["origin"] == "assisted" for r in calls),
        "response_seconds_total": round(total_seconds, 3), "response_seconds_mean": round(total_seconds/len(calls), 3),
        "original_observations": rows, "requests": calls}
    (OUT / "metrics.json").write_text(json.dumps(metrics, indent=2)+"\n", encoding="utf-8")
    with (OUT / "observations.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    print(json.dumps({k:metrics[k] for k in ("original_quote_fidelity", "original_response_structural_pass", "live_api_calls", "assisted_task_id_coverage", "assisted_criterion_id_coverage")}))


if __name__ == "__main__":
    main()
