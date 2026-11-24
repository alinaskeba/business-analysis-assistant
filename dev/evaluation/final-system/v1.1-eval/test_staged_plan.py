"""Offline stage isolation, retry, invalidation and final-validator regressions."""
import copy
import json
import unittest
from unittest.mock import patch

import business_analysis as ba
import ba_workflow as wf
import staged_plan as stages
import test_workflow as fixtures


class StagedPlanTests(unittest.TestCase):
    def setUp(self):
        self.session = wf.approve_session(fixtures.WorkflowTests().clarified(), "Approve test fixture")
        self.plan = fixtures.valid_plan()
        self.work = {k: self.plan[k] for k in stages.WORK_KEYS}
        self.bad_raci = {"raci": [r for r in self.plan["raci"] if r["activity_type"] != "implementation"]}

    def pending(self):
        with patch.object(ba, "request_json", side_effect=[self.work, self.bad_raci]) as request:
            result = wf.generate_documents(self.session)
        self.assertEqual(request.call_count, 2)
        return result

    def test_success_requires_two_stages_and_final_validation(self):
        with patch.object(ba, "request_json", side_effect=fixtures.staged_response(self.plan)) as request:
            result = wf.generate_documents(self.session)
        self.assertEqual(request.call_count, 2)
        self.assertNotIn("raci", request.call_args_list[0].args[2]["properties"])
        self.assertEqual(list(request.call_args_list[1].args[2]["properties"]), ["raci"])
        wf.render_documents(result)

    def test_failed_raci_keeps_work_but_is_not_exportable(self):
        original = copy.deepcopy(self.session)
        result = self.pending()
        self.assertEqual(original, self.session)
        self.assertIsNone(result["documents"])
        self.assertEqual(result["generation_progress"]["work_plan"], self.work)
        self.assertTrue(result["generation_progress"]["errors"])
        with self.assertRaises(ValueError):
            wf.render_documents(result)

    def test_retry_calls_only_raci_with_errors_and_exact_same_work(self):
        pending = self.pending()
        with patch.object(ba, "request_json", return_value={"raci": self.plan["raci"]}) as request:
            result = wf.generate_documents(pending)
        request.assert_called_once()
        payload = json.loads(request.call_args.args[1])
        self.assertEqual(payload["validated_work_plan"], self.work)
        self.assertEqual(payload["validation_errors_to_correct"], pending["generation_progress"]["errors"])
        self.assertEqual(result["documents"]["tasks"], self.work["tasks"])
        self.assertNotIn("generation_progress", result)

    def test_invalid_work_never_reaches_raci(self):
        work = copy.deepcopy(self.work)
        work["acceptance_criteria"] = []
        with patch.object(ba, "request_json", return_value=work) as request:
            with self.assertRaises(ba.AnalysisValidationError):
                wf.generate_documents(self.session)
        request.assert_called_once()

    def test_changed_revision_discards_checkpoint(self):
        pending = self.pending()
        pending["revision"] += 1
        pending = wf.approve_session(pending, "Approve revised test fixture")
        with patch.object(ba, "request_json", side_effect=fixtures.staged_response(self.plan)) as request:
            wf.generate_documents(pending)
        self.assertEqual(request.call_count, 2)

    def test_raci_network_failure_keeps_work_for_manual_retry(self):
        with patch.object(ba, "request_json", side_effect=[self.work, ValueError("network timeout")]):
            result = wf.generate_documents(self.session)
        self.assertEqual(result["generation_progress"]["errors"], ["network timeout"])
        self.assertEqual(result["generation_progress"]["work_plan"], self.work)


if __name__ == "__main__":
    unittest.main()
