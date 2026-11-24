import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts import collect_test_evaluation as collect
from ba_assistant import business_analysis as ba
from ba_assistant import ba_workflow as wf
from tests import test_workflow as fixtures


class CollectionTests(unittest.TestCase):
    def test_nested_quote_checks_do_not_claim_semantic_correctness(self):
        analysis = fixtures.initial_analysis()
        report = collect.checks(analysis, {"brief": fixtures.BRIEF})
        self.assertEqual(report["semantic_support"], "requires_human_review")
        self.assertGreater(report["verbatim_quotes"]["denominator"], 0)
        bad = copy.deepcopy(analysis)
        bad["requirements"][0]["source"]["quote"] = "invented fragment"
        result = collect.checks(bad, {"brief": fixtures.BRIEF})
        self.assertLess(result["verbatim_quotes"]["numerator"], result["verbatim_quotes"]["denominator"])

    def test_manual_rows_include_each_team_duty_and_pending_labels(self):
        session = fixtures.WorkflowTests().clarified()
        review = collect.review_rows(session["analysis"], session["sources"])
        self.assertTrue(any(r["category"] == "team_roles_responsibility" for r in review["rows"]))
        self.assertTrue(all(r["judgment"] == "pending" for r in review["rows"]))

    def test_frozen_collection_initial_payload_has_no_expected_labels(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "collection"
            dataset = collect.prepare(Path('tests/ba_test_cases.json'), root)
            case = dataset["cases"][0]
            result = {key: [] for key in wf.ANALYSIS_SCHEMA["properties"]}
            with patch.object(ba, "request_json", return_value=result) as request:
                meta = collect.run(root, case["case_id"], "initial")
            payload = json.loads(request.call_args.args[1])
            self.assertEqual(payload["sources"], {"brief": case["input"]["initial_requirements"]})
            self.assertEqual(payload["replies"], [])
            self.assertNotIn("expected", payload)
            self.assertEqual(meta["api_calls"], 1)
            self.assertTrue((root / case["case_id"] / "step-01-initial/manual-review.json").exists())


if __name__ == "__main__":
    unittest.main()
