"""Offline workflow/component tests. Model responses below are hand-authored fixtures."""
import copy
import json
from pathlib import Path
import tempfile
import subprocess
import sys
import os
import unittest
from unittest.mock import patch

from ba_assistant import business_analysis as ba
from ba_assistant import ba_workflow as wf
from scripts import evaluate_dev

DATASET_PATH = Path(__file__).resolve().parents[1] / "dev/cases/ba_dev_cases.json"
DATASET = json.loads(DATASET_PATH.read_text(encoding="utf-8"))
CASE = DATASET["cases"][0]
BRIEF = CASE["input"]["initial_requirements"]
TEAM_REPLY = CASE["conversation"]["prepared_answers"][0]["text"]
RULE_REPLY = CASE["conversation"]["prepared_answers"][1]["text"]
RACI_REPLY = CASE["conversation"]["prepared_answers"][2]["text"]
# Explicitly extended mechanical-test fixture using the later user-confirmed governance authority.
# The dataset itself is unchanged; this fixture is not claimed as a literal dataset conversation.
RACI_REPLY += (" The Product Owner is Accountable for specification preparation. "
               "The Product Owner reviews and approves the specification and is both Responsible and Accountable for its acceptance.")


def source(document, quote):
    return {"document": document, "quote": quote}


def requirement(identifier, description, document, quote):
    return {"id": identifier, "description": description, "source": source(document, quote),
            "kind": "functional", "status": "confirmed"}


def initial_analysis():
    result = {key: [] for key in wf.ANALYSIS_SCHEMA["properties"]}
    result["goals"] = [{"id": "G1", "description": "Enable new online retailers to run a store",
                        "source": source("brief", BRIEF.split(". ")[0] + ".")}]
    result["requirements"] = [requirement("R1", "Store staff manage products", "brief", BRIEF.split(". ")[1])]
    for i, (topic, question) in enumerate([
        ("Team", "Who is on the project team and who makes decisions?"),
        ("Business rules", "What is the first-release scope and ordering behavior?"),
        ("RACI authority", "Who is accountable for each project activity?")], 1):
        result["missing_information"].append({"id": f"M{i}", "topic": topic, "why_needed": "Define scope and responsibilities"})
        result["questions"].append({"id": f"Q{i}", "text": question, "target_type": "gap", "target_id": f"M{i}",
                                    "blocks_final_specification": True})
    result["assumptions"] = [{"id": "P1", "description": "A shared staging environment may help delivery",
                              "rationale": "Proposal only; not supplied by the customer", "status": "proposed"}]
    return result


def after_replies(count):
    result = initial_analysis()
    result["missing_information"] = result["missing_information"][count:]
    result["questions"] = result["questions"][count:]
    replies = [TEAM_REPLY, RULE_REPLY, RACI_REPLY]
    result["resolutions"] = [{"question_id": f"Q{i}", "answer_id": f"A{i}", "outcome": "resolved",
                              "description": "The user supplied this decision", "source": source(f"A{i}", replies[i-1])}
                             for i in range(1, count+1)]
    if count:
        for i, name in enumerate(["Product Owner", "Business Analyst", "Full-stack Developer", "QA Engineer"], 1):
            # Cite a complete sentence naming the role and an actual duty.
            sentence = next(s.strip() + "." for s in TEAM_REPLY.split(".") if name in s and "The " + name in s)
            result["team_roles"].append({"id": f"T{i}", "name": name, "responsibilities": [
                {"description": sentence, "source": source("A1", sentence)}]})
    if count >= 2:
        quote = "An empty cart cannot be submitted."
        result["requirements"].append(requirement("R2", "Reject empty-cart submission", "A2", quote))
        result["requirements"].append({"id": "R3", "kind": "constraint", "status": "confirmed",
                                      "description": "No online payment or shipping integrations in release one",
                                      "source": source("A2", "Orders are submitted for staff processing; online payments and shipping integrations are outside the first release.")})
    return result


def staged_response(plan):
    """Mock a response to the requested stage schema without returning extra fields."""
    return lambda instructions, text, schema, model, limit=6000: {k: copy.deepcopy(plan[k]) for k in schema["properties"]}


def valid_plan():
    legacy = {
        "open_questions": [],
        "tasks": [{"id": "TASK1", "title": "Implement product management", "description": "Implement supported staff operations",
                   "requirement_ids": ["R1"]},
                  {"id": "TASK2", "title": "Reject empty checkout", "description": "Enforce empty-cart rule", "requirement_ids": ["R2", "R3"]}],
        "acceptance_criteria": [{"id": "AC1", "requirement_id": "R1", "given": "A store staff member",
                                 "when": "They manage a product", "then": "The supported product operation succeeds",
                                 "source": source("brief", BRIEF.split(". ")[1])},
                                {"id": "AC2", "requirement_id": "R2", "given": "An empty cart",
                                 "when": "The customer attempts order submission", "then": "No order is submitted",
                                 "source": source("A2", "An empty cart cannot be submitted.")}],
        "raci": [{"id": "RA1", "activity": "Implement and deploy", "task_ids": ["TASK1", "TASK2"],
                  "accountable": [{"role_id": "T3", "source": source("A3", "The Full-stack Developer is accountable for implementation and deployment.")}],
                  "responsible": [{"role_id": "T3", "source": source("A1", "The Full-stack Developer makes technical implementation decisions, develops the application, and deploys releases.")}],
                  "consulted": [], "informed": []}]}
    sources = {"brief": BRIEF, "A1": TEAM_REPLY, "A2": RULE_REPLY, "A3": RACI_REPLY}
    registry = wf.plan_sources.build_registry(sources)
    for _, item in wf.plan_sources.cited_records(legacy):
        old = item.pop("source")
        item["source_ids"] = [next(sid for sid, entry in registry.items()
                                  if entry["document"] == old["document"] and old["quote"] in entry["quote"])]
    legacy["raci"][0]["activity_type"] = "implementation"
    for index, (kind, title, document, text, responsible) in enumerate([
        ("requirements_approval", "Approve business requirements", "A1", "The Product Owner defines priorities", "T1"),
        ("specification_preparation", "Prepare the specification", "A3", "The Product Owner is Accountable for specification preparation.", "T2"),
        ("specification_acceptance", "Accept the specification", "A3", "The Product Owner reviews and approves the specification", "T1"),
        ("uat_acceptance", "Accept UAT results", "A1", "The Product Owner approves the user acceptance testing results.", "T1"),
        ("release_decision", "Make the release decision", "A3", "The Product Owner is accountable for the final release decision.", "T1")], 2):
        sid = next(sid for sid, entry in registry.items() if entry["document"] == document and text in entry["quote"])
        rsid = next(sid for sid, entry in registry.items() if "The Business Analyst is responsible for preparing the specification." in entry["quote"]) if responsible == "T2" else sid
        legacy["raci"].append({"id": f"RA{index}", "activity": title, "activity_type": kind, "task_ids": [],
                              "accountable": [{"role_id": "T1", "source_ids": [sid]}],
                              "responsible": [{"role_id": responsible, "source_ids": [rsid]}], "consulted": [], "informed": []})
    return legacy


class WorkflowTests(unittest.TestCase):
    def start(self):
        with patch.object(ba, "request_json", return_value=initial_analysis()):
            session = wf.start_session(BRIEF, "gemini-3.1-flash-lite")
        session["execution_mode"] = "offline_mock_fixture"
        return session

    def clarified(self):
        session = self.start()
        for i, answer in enumerate([TEAM_REPLY, RULE_REPLY, RACI_REPLY], 1):
            with patch.object(ba, "request_json", return_value=after_replies(i)):
                session = wf.reply_to_session(session, f"Q{i}", answer)
        return session

    def test_complete_offline_journey_with_actual_scenario_sources(self):
        session = self.clarified()
        self.assertEqual(wf.blocking_reasons(session), [])
        session = wf.approve_session(session, "I approve these reviewed requirements")
        with patch.object(ba, "request_json", side_effect=staged_response(valid_plan())):
            session = wf.generate_documents(session)
        spec = session["documents"]["specification"]
        self.assertEqual(spec["functional_requirements"][0]["source"]["document"], "brief")
        self.assertEqual(spec["functional_requirements"][1]["source"]["document"], "A2")
        self.assertEqual(spec["proposed_assumptions"][0]["status"], "proposed")
        self.assertNotIn("P1", json.dumps(session["documents"]["tasks"]))
        self.assertIn("# Business analysis document package", wf.render_documents(session))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "session.json"
            wf.save_session(path, session, create=True)
            self.assertEqual(wf.validate_session(json.loads(path.read_text(encoding="utf-8")))["documents"], session["documents"])

    def test_expected_labels_and_unasked_prepared_answers_never_reach_model(self):
        with patch.object(ba, "request_json", return_value=initial_analysis()) as call:
            wf.start_session(BRIEF, "gemini-3.1-flash-lite")
        payload = json.loads(call.call_args.args[1])
        self.assertEqual(payload["sources"], {"brief": BRIEF})
        self.assertEqual(payload["replies"], [])
        self.assertNotIn("expected", call.call_args.args[1])
        self.assertNotIn(TEAM_REPLY, call.call_args.args[1])

    def test_unknown_or_cross_document_evidence_is_rejected(self):
        result = initial_analysis()
        result["requirements"][0]["source"] = source("brief", "An empty cart cannot be submitted.")
        with self.assertRaises(ba.AnalysisValidationError):
            wf.validate_updated_analysis(result, {"brief": BRIEF, "A2": RULE_REPLY}, [], {})
        result["requirements"][0]["source"]["document"] = "A99"
        with self.assertRaises(ba.AnalysisValidationError):
            wf.validate_updated_analysis(result, {"brief": BRIEF}, [], {})

    def test_generation_before_approval_or_with_blockers_never_calls_api(self):
        for session in (self.start(), self.clarified()):
            with patch.object(ba, "request_json") as call:
                with self.assertRaises(ValueError):
                    wf.generate_documents(session)
                call.assert_not_called()

    def test_unresolved_conflict_and_undecided_reply_block_finalization(self):
        session = self.start()
        result = initial_analysis()
        result["requirements"].append(requirement("R2", "Another incompatible rule", "brief", BRIEF))
        result["contradictions"] = [{"id": "C1", "description": "Two incompatible rules", "requirement_ids": ["R1", "R2"]}]
        result["missing_information"] = result["missing_information"][1:]
        result["questions"][0].update(target_type="conflict", target_id="C1")
        session["analysis"] = copy.deepcopy(result)
        undecided = DATASET["cases"][-1]["conversation"]["prepared_answers"][0]["text"]
        result["resolutions"] = [{"question_id": "Q1", "answer_id": "A1", "outcome": "still_open",
                                  "description": "The user has not decided", "source": source("A1", undecided)}]
        with patch.object(ba, "request_json", return_value=result):
            updated = wf.reply_to_session(session, "Q1", undecided)
        with self.assertRaises(ba.AnalysisValidationError):
            wf.approve_session(updated, "Approve")

    def test_model_cannot_silently_drop_earlier_blocker(self):
        session = self.start()
        analysis = after_replies(1)
        analysis["questions"] = []
        analysis["missing_information"] = []
        with patch.object(ba, "request_json", return_value=analysis):
            updated = wf.reply_to_session(session, "Q1", TEAM_REPLY)
        self.assertTrue(any("Q2" in reason for reason in wf.blocking_reasons(updated)))

    def test_reply_invalidates_approval_and_documents(self):
        session = wf.approve_session(self.clarified(), "Approve current revision")
        with patch.object(ba, "request_json", side_effect=staged_response(valid_plan())):
            session = wf.generate_documents(session)
        next_result = after_replies(3)
        next_result["resolutions"].append({"question_id": "Q2", "answer_id": "A4", "outcome": "resolved",
                                            "description": "Rule reaffirmed", "source": source("A4", "Keep the same scope.")})
        with patch.object(ba, "request_json", return_value=next_result):
            updated = wf.reply_to_session(session, "Q2", "Keep the same scope.")
        self.assertIsNone(updated["approval"])
        self.assertIsNone(updated["documents"])

    def test_failed_reply_is_transactional_and_unasked_reply_rejected(self):
        session = self.start()
        original = copy.deepcopy(session)
        with patch.object(ba, "request_json", side_effect=ValueError("API failure")):
            with self.assertRaises(ValueError):
                wf.reply_to_session(session, "Q1", TEAM_REPLY)
        self.assertEqual(session, original)
        with patch.object(ba, "request_json") as call:
            with self.assertRaises(ValueError):
                wf.reply_to_session(session, "Q99", TEAM_REPLY)
            call.assert_not_called()

    def test_stale_approval_is_rejected(self):
        session = wf.approve_session(self.clarified(), "Approve")
        session["analysis"]["requirements"][0]["description"] += " changed"
        with patch.object(ba, "request_json") as call:
            with self.assertRaisesRegex(ValueError, "approval"):
                wf.generate_documents(session)
            call.assert_not_called()

    def test_raci_single_accountable_role_references_and_coverage(self):
        session = self.clarified()
        plan = valid_plan()
        plan["raci"][0]["accountable"].append(copy.deepcopy(plan["raci"][0]["accountable"][0]))
        plan["tasks"][0]["requirement_ids"] = ["P1"]
        plan["acceptance_criteria"][0]["requirement_id"] = "R99"
        with self.assertRaises(ba.AnalysisValidationError) as caught:
            wf.validate_plan(plan, session)
        for fragment in ("exactly one Accountable", "unknown confirmed requirement", "missing implementation task", "missing acceptance criteria"):
            self.assertTrue(any(fragment in e for e in caught.exception.errors), fragment)
        plan = valid_plan()
        plan["raci"][0]["accountable"][0]["role_id"] = "U1"
        with self.assertRaises(ba.AnalysisValidationError):
            wf.validate_plan(plan, session)
        plan["raci"][0]["responsible"] = []
        with self.assertRaises(ba.AnalysisValidationError):
            wf.validate_plan(plan, session)

    def test_specification_export_cannot_be_changed_away_from_approved_facts(self):
        session = wf.approve_session(self.clarified(), "Approve")
        with patch.object(ba, "request_json", side_effect=staged_response(valid_plan())):
            session = wf.generate_documents(session)
        session["documents"]["specification"]["functional_requirements"] = []
        with self.assertRaisesRegex(ValueError, "no longer matches"):
            wf.render_documents(session)

    def test_dev_dataset_is_final_grouped_and_covers_components(self):
        self.assertEqual(DATASET["expectations_status"], "final")
        self.assertEqual(len(DATASET["cases"]), DATASET["coverage_summary"]["total_scenarios"])
        self.assertEqual(len({c["case_id"] for c in DATASET["cases"]}), len(DATASET["cases"]))
        self.assertEqual(set(DATASET["coverage_summary"]["variants"]), {c["case_id"] for c in DATASET["cases"]})
        groups = {}
        for case in DATASET["cases"]:
            self.assertEqual(case["expected_initial_analysis"]["status"], "final")
            self.assertEqual(case["expected_journey"]["status"], "final")
            groups.setdefault(case["group_id"], set()).add(case["split"])
            self.assertTrue(case["input"]["initial_requirements"])
            for component in ("clarification", "updated_requirements", "specification", "tasks", "acceptance_criteria", "raci", "end_to_end"):
                self.assertIn(component, case["expected_journey"])
        self.assertTrue(all(splits == {"dev"} for splits in groups.values()))
        self.assertEqual(len(groups), DATASET["coverage_summary"]["projects"])

    def test_dev_case_loader_never_exposes_expectations(self):
        for case in DATASET["cases"]:
            brief, metadata = wf.dev_case_input(DATASET_PATH, case["case_id"])
            self.assertEqual(brief, case["input"]["initial_requirements"])
            self.assertEqual(set(metadata), {"case_id", "group_id", "split"})
        with self.assertRaises(ValueError):
            wf.dev_case_input(DATASET_PATH, "missing-case")

    def test_offline_component_report_distinguishes_not_run_and_validated_artifacts(self):
        with tempfile.TemporaryDirectory() as directory:
            empty = evaluate_dev.evaluate(DATASET, directory)
            self.assertEqual(len(empty["cases"]), len(DATASET["cases"]))
            self.assertEqual(empty["expectations_status"], "final")
            self.assertTrue(all(value == "not_run" for row in empty["cases"] for value in row["components"].values()))
            session = wf.approve_session(self.clarified(), "Approve")
            with patch.object(ba, "request_json", side_effect=staged_response(valid_plan())):
                session = wf.generate_documents(session)
            wf.save_session(Path(directory) / (CASE["case_id"] + ".session.json"), session)
            report = evaluate_dev.evaluate(DATASET, directory)
            self.assertEqual(report["cases"][0]["errors"], [])
            self.assertEqual(report["cases"][0]["components"]["raci"], "structural_pass; semantic_review_needed")
            self.assertEqual(report["semantic_quality"], "not_measured; human review required")

    def test_unresolved_dev_trajectories_do_not_authorize_approval(self):
        trajectories = [case for case in DATASET["cases"] if case["case_id"].endswith("conflict_unresolved")]
        self.assertTrue(trajectories)
        for case in trajectories:
            with self.subTest(case=case["case_id"]):
                self.assertNotIn("approval_text", case["conversation"]["final_review"])
                self.assertTrue(case["conversation"]["prepared_answers"])

    def test_final_expectation_evidence_and_team_duties_match_actual_sources(self):
        for case in DATASET["cases"]:
            with self.subTest(case=case["case_id"]):
                initial = case["input"]["initial_requirements"]
                replies = {reply["reply_id"]: reply["text"] for reply in case["conversation"]["prepared_answers"]}
                initial_roles = case["expected_initial_analysis"]["team_expectation"]["responsibilities_to_cover"]
                updated_roles = case["expected_journey"]["updated_requirements"]["team_responsibilities_to_cover"]
                for role in initial_roles + updated_roles:
                    self.assertTrue(role["responsibilities"])
                    for duty in role["responsibilities"]:
                        evidence = duty["evidence"]
                        text = initial if evidence["stage"] == "initial" else replies[evidence["prepared_reply_id"]]
                        self.assertIn(evidence["quote"], text)
                for conflict in case["expected_initial_analysis"]["expected_conflicts"]:
                    for statement in conflict["statements"]:
                        self.assertIn(statement, initial)
                        self.assertIn(statement, case["expected_initial_analysis"]["requirement_meanings_to_cover"])

    def test_conflict_resolution_preserves_only_unchanged_active_rules(self):
        cases = [case for case in DATASET["cases"] if case["case_id"].endswith("conflict_resolved")]
        self.assertTrue(cases)
        for case in cases:
            updated = case["expected_journey"]["updated_requirements"]
            self.assertNotIn("preserve_initial_requirements", updated)
            self.assertTrue(updated["preserve_unchanged_initial_requirements"])
            replies = {reply["reply_id"]: reply["text"] for reply in case["conversation"]["prepared_answers"]}
            for retired in updated["superseded_requirements"]:
                self.assertIn(retired["statement"], case["input"]["initial_requirements"])
                self.assertIn(retired["evidence_quote"], replies[retired["evidence_prepared_reply_id"]])
            approval = next(check for check in case["expected_journey"]["acceptance_criteria"]["semantic_checks"]
                            if check["topic"] == "Approval")
            self.assertNotIn("remains pending", approval["then"])

    def test_user_and_actor_coverage_is_explicit(self):
        for case in DATASET["cases"]:
            expected = case["expected_initial_analysis"]
            if case["group_id"] == "PURE_002":
                for requirement in expected["requirement_meanings_to_cover"][:2]:
                    self.assertIn("Store owners and sales personnel", requirement)
            else:
                self.assertTrue(any("faculty administrator" in user for user in expected["users_to_cover"]))

    def test_reply_source_registry_must_match_actual_answers(self):
        session = self.clarified()
        session["sources"]["A1"] = "Forged source"
        with self.assertRaisesRegex(ValueError, "provenance"):
            wf.validate_session(session)

    def test_requirements_are_never_sourced_from_a_proposed_assumption(self):
        session = self.start()
        session["analysis"]["requirements"][0]["source"]["document"] = "P1"
        with self.assertRaises(ba.AnalysisValidationError):
            wf.validate_session(session)

    def test_real_cli_review_and_export_are_offline(self):
        session = wf.approve_session(self.clarified(), "Approve")
        with patch.object(ba, "request_json", side_effect=staged_response(valid_plan())):
            session = wf.generate_documents(session)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "session.json"
            output = Path(directory) / "package.md"
            wf.save_session(path, session, create=True)
            environment = dict(os.environ, GEMINI_API_KEY="")
            cli = ["-m", "ba_assistant.business_analysis"]
            review = subprocess.run([sys.executable, *cli, "--workflow", "review", "--session", str(path)],
                                    env=environment, capture_output=True, text=True)
            self.assertEqual(review.returncode, 0, review.stderr)
            self.assertEqual(json.loads(review.stdout)["source_ids"], ["brief", "A1", "A2", "A3"])
            export = subprocess.run([sys.executable, *cli, "--workflow", "export", "--session", str(path),
                                     "--output", str(output)], env=environment, capture_output=True, text=True)
            self.assertEqual(export.returncode, 0, export.stderr)
            self.assertTrue(output.exists())
            self.assertEqual(json.loads(export.stdout)["status"], "draft_for_document_review")

    def test_history_conflict_is_blocking_even_if_model_marked_question_nonblocking(self):
        session = self.clarified()
        session["question_history"]["Q99"] = {"id": "Q99", "text": "Which rule?", "target_type": "conflict",
                                               "target_id": "C99", "blocks_final_specification": False}
        self.assertTrue(any("Q99" in reason for reason in wf.blocking_reasons(session)))


if __name__ == "__main__":
    unittest.main()
