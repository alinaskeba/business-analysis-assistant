"""Offline regressions for the live experiment runner; no API calls."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import business_analysis as ba
import run_component_eval as runner


class ComponentRunnerTests(unittest.TestCase):
    def dataset(self, root, case_id="example"):
        (root / "dataset.json").write_text(json.dumps({"expectations_status": "final", "cases": [{
            "case_id": case_id, "input": {"initial_requirements": "A user creates a request."},
            "expected_initial_analysis": {"secret_label": "must_not_reach_model"}}]}), encoding="utf-8")

    def test_initial_payload_has_no_expected_fields_and_never_overwrites(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.dataset(root)
            result = {key: [] for key in runner.wf.ANALYSIS_SCHEMA["properties"]}
            with patch.object(ba, "load_env"), patch.object(ba, "request_json", return_value=result) as call:
                runner.run(root, "initial")
                payload = json.loads(call.call_args.args[1])
                self.assertEqual(payload["sources"], {"brief": "A user creates a request."})
                self.assertNotIn("must_not_reach_model", call.call_args.args[1])
                self.assertEqual(payload["replies"], [])
                with self.assertRaises(ValueError):
                    runner.run(root, "initial")
                self.assertEqual(call.call_count, 1)

    def test_invalid_output_is_preserved_and_not_retried(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.dataset(root)
            with patch.object(ba, "load_env"), patch.object(ba, "request_json", return_value={}) as call:
                runner.run(root, "initial")
                self.assertEqual(call.call_count, 1)
            meta = json.loads((root / "example/initial/run.json").read_text())
            self.assertEqual(meta["status"], "validation_failed")
            self.assertTrue((root / "example/initial/output.json").exists())

    def test_transient_execution_failure_is_recorded_before_one_retry(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.dataset(root)
            result = {key: [] for key in runner.wf.ANALYSIS_SCHEMA["properties"]}
            with patch.object(ba, "load_env"), patch.object(ba, "request_json", side_effect=[ValueError("API returned HTTP 503"), result]):
                runner.run(root, "initial")
            meta = json.loads((root / "example/initial/run.json").read_text())
            self.assertEqual(len(meta["attempts"]), 2)
            self.assertEqual(meta["attempts"][0]["status"], "execution_failure")
            self.assertEqual(meta["status"], "validation_passed")

    def test_unresolved_plan_has_no_api_call(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.dataset(root, "example_unresolved")
            case = root / "example_unresolved"
            case.mkdir()
            (case / "reference.json").write_text(json.dumps({"sources": {"brief": "An unresolved conflict."}}))
            with patch.object(ba, "load_env"), patch.object(ba, "request_json") as call:
                runner.run(root, "plan")
                call.assert_not_called()
            self.assertEqual(json.loads((case / "plan/run.json").read_text())["status"], "not_applicable")


if __name__ == "__main__":
    unittest.main()
