"""Checks for the source-reviewed baseline; no model/API invocation."""
import hashlib
import json
from pathlib import Path
import unittest

import ba_workflow as wf
import business_analysis as ba


class ReviewedBaselineTests(unittest.TestCase):
    root = Path(__file__).parent / "dev/evaluation/plan-pass-03-reviewed-baseline"

    def setUp(self):
        self.plan = json.loads((self.root / "plan.reviewed.json").read_text(encoding="utf-8"))
        self.data = json.loads((self.root / "input.json").read_text(encoding="utf-8"))
        self.criteria = {x["id"]: x for x in self.plan["acceptance_criteria"]}

    def test_all_sources_match_the_named_document(self):
        def walk(value):
            if isinstance(value, dict):
                if "document" in value and "quote" in value:
                    self.assertTrue(value["quote"].strip())
                    self.assertIn(value["quote"], self.data["sources"][value["document"]])
                for child in value.values():
                    walk(child)
            elif isinstance(value, list):
                for child in value:
                    walk(child)
        walk(self.plan)
        walk(json.loads((self.root / "governance-questions.json").read_text()))

    def test_complete_requirement_coverage_and_parameters(self):
        required = {r["id"] for r in self.data["approved_analysis"]["requirements"] if r["kind"] != "constraint"}
        self.assertEqual(len(required), 13)
        self.assertEqual({c["requirement_id"] for c in self.criteria.values()}, required)
        self.assertEqual(len(self.criteria), 15)
        parameters = json.loads((self.root / "scenario-parameters.json").read_text())
        actor = parameters[0]
        self.assertEqual(actor["values"], ["Store owner", "Sales personnel"])
        self.assertEqual(set(actor["criterion_ids"]), {"AC1", "AC2", "AC10", "AC11"})
        self.assertEqual(parameters[2]["values"], [0, -1, 1.5])

    def test_access_and_scope_conditions_are_not_weakened(self):
        self.assertIn("available", self.criteria["AC4"]["given"])
        self.assertIn("add-to-cart", self.criteria["AC4"]["when"])
        self.assertIn("signed-in", self.criteria["AC5"]["given"])
        self.assertIn("no order is placed before successful sign-in", self.criteria["AC7"]["then"])
        for identifier in ("AC10", "AC11"):
            self.assertIn("Store owner, Sales personnel", self.criteria[identifier]["given"])
        self.assertNotIn("unique", self.criteria["AC12"]["then"])
        self.assertIn("successfully submits", self.criteria["AC12"]["when"])

    def test_separate_governance_and_explicit_unresolved_authority(self):
        rows = {r["id"]: r for r in self.plan["raci"]}
        self.assertEqual(rows["RA5"]["activity"], "Approve Business Requirements")
        self.assertEqual(rows["RA6"]["activity"], "Accept the Specification")
        self.assertEqual(rows["RA5"]["task_ids"], [])
        self.assertEqual(rows["RA6"]["task_ids"], [])
        self.assertEqual(rows["RA1"]["accountable"], [])
        self.assertEqual(rows["RA6"]["accountable"][0]["role_id"], "T1")
        self.assertEqual(rows["RA6"]["responsible"], [])
        questions = json.loads((self.root / "governance-questions.json").read_text())
        self.assertEqual({q["activity_id"] for q in questions}, {"RA1", "RA6"})
        self.assertTrue(all(q["blocks_finalization"] for q in questions))
        with self.assertRaises(ba.AnalysisValidationError) as caught:
            wf.validate_plan_legacy_v2(self.plan, {"analysis": self.data["approved_analysis"], "sources": self.data["sources"]})
        self.assertEqual(len(caught.exception.errors), 2)

    def test_history_and_baseline_hashes_are_preserved(self):
        manifest = json.loads((self.root / "manifest.json").read_text())
        original = Path(__file__).parent / manifest["original_output"]
        self.assertEqual(original.read_bytes(), (self.root / "model-original.json").read_bytes())
        self.assertEqual(hashlib.sha256(original.read_bytes()).hexdigest(), manifest["original_output_sha256"])
        self.assertFalse(manifest["ready_for_finalization"])
        self.assertTrue(manifest["not_a_model_run"])
        for filename, expected in manifest["files_sha256"].items():
            self.assertEqual(hashlib.sha256((self.root / filename).read_bytes()).hexdigest(), expected)


if __name__ == "__main__":
    unittest.main()
