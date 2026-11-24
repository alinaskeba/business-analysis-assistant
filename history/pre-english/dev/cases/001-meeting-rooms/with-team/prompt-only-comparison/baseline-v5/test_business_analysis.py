"""Offline checks for analysis provenance and reference integrity."""
import copy
import json
from pathlib import Path
import unittest
import io
from unittest.mock import patch

import business_analysis as ba


class AnalysisValidationTests(unittest.TestCase):
    def setUp(self):
        self.result = {key: [] for key in ba.SCHEMA["properties"]}
        self.result["goals"] = [{"id": "G1", "description": "Goal", "source": {
            "document": "brief", "quote": ba.EXAMPLE.splitlines()[1]}}]
        self.result["team_roles"] = [{"id": "T1", "name": "Example role", "responsibilities": [
            {"description": "First responsibility", "source": {
                "document": "brief", "quote": ba.EXAMPLE.splitlines()[5]}},
            {"description": "Second responsibility", "source": {
                "document": "brief", "quote": ba.EXAMPLE.splitlines()[6]}}]}]
        self.result["users"] = [{"id": "U1", "name": "Example user", "responsibilities": [
            {"description": "Participation", "source": {
                "document": "brief", "quote": ba.EXAMPLE.splitlines()[2]}}]}]
        self.result["requirements"] = [
            {"id": f"R{i}", "kind": "functional", "description": "Rule",
             "source": {"document": "brief", "quote": ba.EXAMPLE.splitlines()[i + 4]}}
            for i in (1, 2)]
        self.result["contradictions"] = [{"id": "C1", "description": "Approval conflict",
                                           "requirement_ids": ["R1", "R2"]}]
        self.result["missing_information"] = [{"id": "M1", "topic": "Team", "why_needed": "Ownership"}]
        self.result["questions"] = [
            {"id": "Q1", "text": "Which rule?", "target_type": "conflict", "target_id": "C1",
             "blocks_final_specification": True},
            {"id": "Q2", "text": "Who owns delivery?", "target_type": "gap", "target_id": "M1",
             "blocks_final_specification": False}]

    def test_valid_graph(self):
        self.assertIs(ba.validate_analysis(self.result, ba.EXAMPLE), self.result)

    def test_saved_dev_result(self):
        case = Path(__file__).parent / "dev/cases/001-meeting-rooms"
        brief = (case / "brief.txt").read_text(encoding="utf-8").strip()
        result = json.loads((case / "analysis.model-result.json").read_text(encoding="utf-8"))
        self.assertEqual(brief, ba.EXAMPLE)
        archived_schema = json.loads((case / "analysis.schema.json").read_text(encoding="utf-8"))
        ba.validate_analysis(result, brief, schema=archived_schema)
        requirements = {item["id"]: item for item in result["requirements"]}
        positions = {brief.splitlines()[5], brief.splitlines()[6]}
        self.assertTrue(any(
            positions <= {requirements[identifier]["source"]["quote"]
                          for identifier in conflict["requirement_ids"]}
            for conflict in result["contradictions"]))
        self.assertEqual(result["team_roles"], [])

    def test_glued_nested_quote_and_uncovered_gap_reported_together(self):
        self.result["team_roles"][0]["responsibilities"][1]["source"]["quote"] = (
            ba.EXAMPLE.splitlines()[5] + " [...] " + ba.EXAMPLE.splitlines()[6])
        self.result["questions"].pop()
        with self.assertRaises(ba.AnalysisValidationError) as caught:
            ba.validate_analysis(self.result, ba.EXAMPLE)
        self.assertEqual(len(caught.exception.errors), 2)
        self.assertTrue(any("responsibilities[1].source.quote" in e for e in caught.exception.errors))
        self.assertTrue(any("missing_information[0]: no clarification question" in e
                            for e in caught.exception.errors))

    def test_all_user_and_team_responsibility_quotes_checked(self):
        self.result["users"][0]["responsibilities"][0]["source"]["quote"] = "invented user quote"
        self.result["team_roles"][0]["responsibilities"][0]["source"]["quote"] = "invented first quote"
        self.result["team_roles"][0]["responsibilities"][1]["source"]["quote"] = "invented second quote"
        self.assertEqual(len(ba.collect_analysis_errors(self.result, ba.EXAMPLE)), 3)

    def test_malformed_fields_do_not_hide_other_errors(self):
        self.result["team_roles"][0]["responsibilities"][0]["source"] = None
        self.result["requirements"][0]["source"]["quote"] = "invented"
        self.result["questions"][0]["blocks_final_specification"] = "true"
        self.result["questions"][1]["target_id"] = "M99"
        errors = ba.collect_analysis_errors(self.result, ba.EXAMPLE)
        self.assertEqual(len(errors), 5)
        for fragment in ("expected object", "quote not found", "expected boolean",
                         "missing target", "no clarification question"):
            self.assertTrue(any(fragment in error for error in errors), fragment)

    def test_duplicate_role_and_empty_responsibilities_rejected(self):
        self.result["team_roles"].append({"id": "T2", "name": "example ROLE", "responsibilities": []})
        errors = ba.collect_analysis_errors(self.result, ba.EXAMPLE)
        self.assertTrue(any("duplicate role" in e for e in errors))
        self.assertTrue(any("too few items" in e for e in errors))

    def test_baseline_reports_both_known_errors_with_archived_schema(self):
        case = Path(__file__).parent / "dev/cases/001-meeting-rooms/with-team/roles-v3/baseline-v4"
        result = json.loads((case / "model-result.json").read_text(encoding="utf-8"))
        schema = json.loads((case / "schema.json").read_text(encoding="utf-8"))
        errors = ba.collect_analysis_errors(result, (case / "brief.txt").read_text(encoding="utf-8"), schema)
        self.assertEqual(len(errors), 2)
        self.assertTrue(any("quote not found" in e for e in errors))
        self.assertTrue(any("no clarification question" in e for e in errors))

    def test_cli_rejects_invalid_analysis_without_success_output(self):
        self.result["questions"].pop()
        def invalid_analysis(*args):
            return ba.validate_analysis(self.result, ba.EXAMPLE)
        out, err = io.StringIO(), io.StringIO()
        with patch("sys.argv", ["business_analysis.py", "--example"]), patch.object(ba, "load_env"), \
                patch.object(ba, "analyze", side_effect=invalid_analysis), \
                patch("sys.stdout", out), patch("sys.stderr", err):
            self.assertEqual(ba.main(), 1)
        self.assertEqual(out.getvalue(), "")
        self.assertIn("no clarification question", err.getvalue())

    def test_saved_schema_v3_candidate_and_nested_sources(self):
        case = Path(__file__).parent / "dev/cases/001-meeting-rooms/with-team/roles-v3/candidate-v5"
        result = json.loads((case / "model-result.json").read_text(encoding="utf-8"))
        brief = (case.parent / "baseline-v4/brief.txt").read_text(encoding="utf-8")
        ba.validate_analysis(result, brief)
        po = [role for role in result["team_roles"] if role["name"] == "Product Owner"]
        self.assertEqual(len(po), 1)
        self.assertEqual(len(po[0]["responsibilities"]), 2)
        self.assertTrue(any(role["name"] == "Офіс-менеджер" for role in result["users"]))

    def test_reject_invalid_graphs_and_sources(self):
        mutations = [
            lambda r: r["goals"][0]["source"].update(quote="invented quote"),
            lambda r: r["requirements"][0]["source"].update(quote="invented quote"),
            lambda r: r["requirements"][1].update(id="R1"),
            lambda r: r["requirements"][0]["source"].update(document="unknown"),
            lambda r: r["contradictions"][0].update(requirement_ids=["R1", "R99"]),
            lambda r: r["contradictions"][0].update(requirement_ids=["R1", "R1"]),
            lambda r: r["contradictions"][0].update(requirement_ids=["R1"]),
            lambda r: r["questions"][0].update(target_id="C99"),
            lambda r: r["questions"][0].update(target_id="M1"),
            lambda r: r["questions"][1].update(target_id="M99"),
            lambda r: r["questions"][0].update(blocks_final_specification="true"),
            lambda r: r["questions"].pop(),
            lambda r: r.update(extra="unexpected"),
        ]
        for index, mutate in enumerate(mutations):
            with self.subTest(index=index):
                result = copy.deepcopy(self.result)
                mutate(result)
                with self.assertRaises(ValueError):
                    ba.validate_analysis(result, ba.EXAMPLE)


if __name__ == "__main__":
    unittest.main()
