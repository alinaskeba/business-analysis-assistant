"""Regression tests for criterion coverage, explicit questions and governance RACI."""
import copy
import unittest
from unittest.mock import patch

from ba_assistant import ba_workflow as wf
from ba_assistant import business_analysis as ba
from tests import test_workflow as fixtures
from tests.test_workflow import valid_plan


class PlanCoverageTests(unittest.TestCase):
    def setUp(self):
        self.session = fixtures.WorkflowTests().clarified()

    def test_each_implementable_requirement_needs_a_criterion(self):
        plan = valid_plan()
        plan["acceptance_criteria"] = plan["acceptance_criteria"][:1]
        with self.assertRaises(ba.AnalysisValidationError) as caught:
            wf.validate_plan(plan, self.session)
        self.assertIn("R2: missing acceptance criteria", caught.exception.errors)

    def test_concrete_question_is_not_criterion_coverage_and_blocks_documents(self):
        plan = valid_plan()
        plan["acceptance_criteria"] = plan["acceptance_criteria"][:1]
        plan["open_questions"] = [{"id": "OQ1", "requirement_id": "R2",
                                    "missing_information": "The exact customer-visible response is not specified.",
                                    "question": "What should customers see when empty-cart submission is rejected?"}]
        wf.validate_plan(plan, self.session)
        approved = wf.approve_session(self.session, "Approve reviewed requirements")
        with patch.object(ba, "request_json", side_effect=fixtures.staged_response(plan)):
            result = wf.generate_documents(approved)
        self.assertIsNone(result["documents"])
        self.assertIsNone(result["approval"])
        self.assertTrue(result["analysis"]["questions"][0]["blocks_final_specification"])
        self.assertEqual(result["planning_attempt"]["status"], "blocked_on_plan_questions")
        self.assertTrue(wf.blocking_reasons(result))
        self.assertTrue(any(q["text"] == plan["open_questions"][0]["question"] for q in result["question_history"].values()))

    def test_empty_or_unknown_question_does_not_excuse_missing_criteria(self):
        for rid, text in (("R99", "What is missing?"), ("R2", "")):
            plan = valid_plan()
            plan["acceptance_criteria"] = plan["acceptance_criteria"][:1]
            plan["open_questions"] = [{"id": "OQ1", "requirement_id": rid,
                                        "missing_information": "Unknown decision", "question": text}]
            with self.assertRaises(ba.AnalysisValidationError):
                wf.validate_plan(plan, self.session)

    def test_generic_success_statement_is_not_a_test(self):
        plan = valid_plan()
        plan["acceptance_criteria"][0]["then"] = "The requirement is satisfied."
        with self.assertRaises(ba.AnalysisValidationError) as caught:
            wf.validate_plan(plan, self.session)
        self.assertTrue(any("not an observable" in e for e in caught.exception.errors))

    def test_governance_activity_needs_no_implementation_task(self):
        plan = valid_plan()
        governance = [r for r in plan["raci"] if r["activity_type"] in wf.plan_sources.ACTIVITIES]
        self.assertEqual(len(governance), 5)
        self.assertTrue(all(r["task_ids"] == [] for r in governance))
        wf.validate_plan(plan, self.session)

    def test_all_undefined_requirements_can_return_only_questions(self):
        plan = {"tasks": [], "raci": [], "acceptance_criteria": [], "open_questions": [
            {"id": f"OQ{i}", "requirement_id": rid, "missing_information": "Required business decision is absent",
             "question": "Which observable business outcome should apply?"} for i, rid in enumerate(("R1", "R2"), 1)]}
        wf.validate_plan(plan, self.session)


if __name__ == "__main__":
    unittest.main()
