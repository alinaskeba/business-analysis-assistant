"""Source-ID provenance, deterministic hydration and retained semantic-review regressions."""
import copy
import unittest
from unittest.mock import patch

import ba_workflow as wf
import business_analysis as ba
import plan_sources as ps
import test_workflow as fixtures


class PlanSourceTests(unittest.TestCase):
    def setUp(self):
        self.session = fixtures.WorkflowTests().clarified()
        self.plan = fixtures.valid_plan()
        self.payload = ps.prepare_input(self.session["analysis"], self.session["sources"])
        self.registry = self.payload["source_registry"]

    def test_registry_is_deterministic_and_contains_original_substrings(self):
        self.assertEqual(self.payload, ps.prepare_input(self.session["analysis"], self.session["sources"]))
        for source in self.registry.values():
            self.assertEqual(self.session["sources"][source["document"]][source["start"]:source["end"]], source["quote"])

    def test_generator_schema_never_allows_model_written_quotes(self):
        for _, record in ps.cited_records(self.plan):
            self.assertIn("source_ids", record)
            self.assertNotIn("source", record)
        broken = copy.deepcopy(self.plan)
        broken["acceptance_criteria"][0]["source"] = {"document": "brief", "quote": "Invented ... quote"}
        with self.assertRaises(ba.AnalysisValidationError):
            wf.validate_plan(broken, self.session)

    def test_unknown_id_is_rejected(self):
        self.plan["acceptance_criteria"][0]["source_ids"] = ["S99999"]
        with self.assertRaises(ba.AnalysisValidationError) as caught:
            wf.validate_plan(self.plan, self.session)
        self.assertTrue(any("unknown source ID" in e for e in caught.exception.errors))

    def test_valid_but_unrelated_id_does_not_prove_support(self):
        sid = next(sid for sid, s in self.registry.items() if "QA Engineer is accountable for test execution" in s["quote"])
        self.plan["acceptance_criteria"][0]["source_ids"] = [sid]
        with self.assertRaises(ba.AnalysisValidationError) as caught:
            wf.validate_plan(self.plan, self.session)
        self.assertTrue(any("requirement's origin" in e for e in caught.exception.errors))

    def test_hydration_uses_registry_and_tampering_is_detected(self):
        resolved = ps.hydrate(self.plan, self.registry)
        wf.validate_plan(resolved, self.session)
        resolved["acceptance_criteria"][0]["sources"][0]["quote"] = "Modified text"
        with self.assertRaises(ba.AnalysisValidationError):
            wf.validate_plan(resolved, self.session)

    def test_governance_coverage_is_required_independently_of_raci_cardinality(self):
        self.plan["raci"] = [r for r in self.plan["raci"] if r["activity_type"] != "specification_acceptance"]
        with self.assertRaises(ba.AnalysisValidationError) as caught:
            wf.validate_plan(self.plan, self.session)
        self.assertTrue(any("missing explicit governance activity specification_acceptance" in e for e in caught.exception.errors))

    def test_generation_and_export_preserve_semantic_review_instead_of_claiming_entailment(self):
        approved = wf.approve_session(self.session, "Approve fixture")
        with patch.object(ba, "request_json", side_effect=fixtures.staged_response(self.plan)) as call:
            result = wf.generate_documents(approved)
        self.assertIn('"source_registry"', call.call_args.args[1])
        self.assertIn('"validated_work_plan"', call.call_args.args[1])
        self.assertTrue(all(row["status"] == "needs_semantic_review" for row in result["documents"]["source_alignment_review"]))
        self.assertIn('"quote"', wf.render_documents(result))

    def test_governance_only_plan_is_rejected_for_each_uncovered_task(self):
        self.plan["raci"] = [r for r in self.plan["raci"] if r["activity_type"] != "implementation"]
        with self.assertRaises(ba.AnalysisValidationError) as caught:
            wf.validate_plan(self.plan, self.session)
        for task in self.plan["tasks"]:
            self.assertIn(f"raci: task {task['id']} has no implementation activity", caught.exception.errors)

    def test_testing_or_deployment_does_not_replace_implementation(self):
        for kind in ("testing", "deployment", "other"):
            with self.subTest(kind=kind):
                plan = copy.deepcopy(self.plan)
                plan["raci"][0]["activity_type"] = kind
                with self.assertRaises(ba.AnalysisValidationError) as caught:
                    wf.validate_plan(plan, self.session)
                self.assertTrue(any("has no implementation activity" in e for e in caught.exception.errors))

    def test_partial_task_coverage_is_rejected(self):
        extra = copy.deepcopy(self.plan["tasks"][0])
        extra["id"] = "TASK999"
        self.plan["tasks"].append(extra)
        with self.assertRaises(ba.AnalysisValidationError) as caught:
            wf.validate_plan(self.plan, self.session)
        self.assertIn("raci: task TASK999 has no implementation activity", caught.exception.errors)

    def test_consulted_role_does_not_need_approval_authority(self):
        sid = next(sid for sid, entry in self.registry.items()
                   if "The Business Analyst gathers" in entry["quote"])
        row = next(r for r in self.plan["raci"] if r["activity_type"] == "requirements_approval")
        row["consulted"] = [{"role_id": "T2", "source_ids": [sid]}]
        wf.validate_plan(self.plan, self.session)
        # Structural acceptance still leaves full semantic support for manual review.
        audit = ps.alignment_review(self.plan, self.session["analysis"], self.session["sources"])
        self.assertTrue(all(r["status"] == "needs_semantic_review" for r in audit))
        row["accountable"] = [{"role_id": "T2", "source_ids": [sid]}]
        with self.assertRaises(ba.AnalysisValidationError) as caught:
            wf.validate_plan(self.plan, self.session)
        self.assertTrue(any("different governance action" in e for e in caught.exception.errors))

    def test_consulted_unknown_role_is_still_rejected(self):
        row = next(r for r in self.plan["raci"] if r["activity_type"] == "requirements_approval")
        row["consulted"] = [{"role_id": "T999", "source_ids": row["accountable"][0]["source_ids"]}]
        with self.assertRaises(ba.AnalysisValidationError) as caught:
            wf.validate_plan(self.plan, self.session)
        self.assertTrue(any("unknown project-team role" in e for e in caught.exception.errors))


if __name__ == "__main__":
    unittest.main()
