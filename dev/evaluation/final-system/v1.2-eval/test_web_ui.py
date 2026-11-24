"""Web adapter checks; no live Gemini calls."""
import json
import copy
import threading
import unittest
from http.server import ThreadingHTTPServer
from unittest.mock import patch
from urllib.request import Request, urlopen
from urllib.error import HTTPError

import business_analysis as ba
import web_ui
import test_workflow as fixtures


class WebTests(unittest.TestCase):
    def test_approval_button_records_approval_without_typed_message(self):
        app = web_ui.DemoApp()
        app.session = fixtures.WorkflowTests().clarified()
        with patch.object(web_ui.wf, "generate_documents", side_effect=lambda session: session) as generate:
            result = app.action({"action": "approve_generate"})
        generate.assert_called_once()
        self.assertIn("clicked Approve", result["session"]["approval"]["message"])

    def test_ui_blocks_third_raci_attempt(self):
        app = web_ui.DemoApp()
        app.session = fixtures.WorkflowTests().clarified()
        app.session["generation_progress"] = {"status": "raci_failed", "raci_attempts": 2}
        with patch.object(web_ui.wf, "generate_documents") as generate:
            with self.assertRaisesRegex(ValueError, "Both RACI attempts"):
                app.action({"action": "generate"})
            generate.assert_not_called()

    def test_review_corrections_are_reply_evidence_and_clear_approval(self):
        app = web_ui.DemoApp()
        app.session = web_ui.wf.approve_session(fixtures.WorkflowTests().clarified(), "Approve fixture")
        original = copy.deepcopy(app.session)
        text = "Keep the currently stated product rules."
        analysis = copy.deepcopy(app.session["analysis"])
        qid = f"Q{max(int(q[1:]) for q in app.session['question_history']) + 1}"
        aid = f"A{len(app.session['replies']) + 1}"
        analysis["resolutions"].append({"question_id": qid, "answer_id": aid, "outcome": "resolved",
            "description": "The reviewer confirms the existing rules.", "source": {"document": aid, "quote": text}})
        with patch.object(ba, "request_json", return_value=analysis):
            result = app.action({"action": "request_changes", "text": text})
        self.assertEqual(result["session"]["sources"][aid], text)
        self.assertIsNone(result["session"]["approval"])
        self.assertIsNone(result["session"]["documents"])
        self.assertEqual(original["sources"], {k:v for k,v in result["session"]["sources"].items() if k!=aid})

    def test_saved_live_demo_passes_validation_without_api_call(self):
        app = web_ui.DemoApp()
        with patch.object(ba, "request_json") as request:
            result = app.action({"action": "load_demo"})
            web_ui.wf.render_documents(result["session"])
            request.assert_not_called()
        self.assertIn("simulated", result["session"]["demo_notice"])
        self.assertEqual(len(result["session"]["documents"]["tasks"]), 2)

    def test_batch_answers_are_separate_sources_with_one_reanalysis(self):
        session = fixtures.WorkflowTests().clarified()
        original = copy.deepcopy(session)
        ids = list(session["question_history"])[:2]
        self.assertEqual(len(ids), 2)
        answers = [{"question_id": qid, "text": f"Answer {index}"} for index, qid in enumerate(ids)]
        with patch.object(web_ui.wf, "analyze_session", side_effect=lambda s: s) as analyze:
            result = web_ui.wf.reply_many_to_session(session, answers)
        analyze.assert_called_once()
        self.assertEqual(session, original)
        self.assertEqual(len(result["replies"]), len(session["replies"]) + 2)
        for reply in result["replies"][-2:]:
            self.assertEqual(result["sources"][reply["id"]], reply["text"])

    def test_failed_batch_preserves_accepted_session_and_validation(self):
        app = web_ui.DemoApp()
        app.session = fixtures.WorkflowTests().clarified()
        original = copy.deepcopy(app.session)
        qid = next(iter(app.session["question_history"]))
        answers = [{"question_id": qid, "text": "Explicit clarification"}]
        with patch.object(web_ui.wf, "analyze_session", side_effect=ba.AnalysisValidationError(["no clarification question"])):
            with self.assertRaises(ba.AnalysisValidationError):
                app.action({"action": "reply_many", "answers": answers})
        self.assertEqual(app.session, original)
        with patch.object(web_ui.wf, "analyze_session") as analyze:
            for invalid in ([], answers * 2, [{"question_id": qid, "text": " "}]):
                with self.assertRaises(ValueError):
                    web_ui.wf.reply_many_to_session(app.session, invalid)
            analyze.assert_not_called()

    def test_workflow_actions_and_failed_generation_preserve_session(self):
        app = web_ui.DemoApp()
        session = fixtures.WorkflowTests().clarified()
        with patch.object(web_ui.wf, "start_session", return_value=session):
            app.action({"action": "start", "brief": "Example"})
        app.action({"action": "approve", "message": "Reviewed and approved"})
        approved = app.session
        with patch.object(web_ui.wf, "generate_documents", side_effect=ba.AnalysisValidationError(["Invalid RACI"])):
            with self.assertRaises(ba.AnalysisValidationError):
                app.action({"action": "generate"})
        self.assertEqual(approved, app.session)
        with patch.object(web_ui.wf, "generate_documents", return_value={**approved, "documents": {"status": "draft"}}):
            self.assertEqual(app.action({"action": "generate"})["session"]["documents"]["status"], "draft")
        app.action({"action": "reset"})
        self.assertIsNone(app.session)

    def test_reply_uses_existing_workflow(self):
        app = web_ui.DemoApp()
        app.session = fixtures.WorkflowTests().clarified()
        with patch.object(web_ui.wf, "reply_to_session", return_value=app.session) as reply:
            app.action({"action": "reply", "question_id": "Q1", "text": "Clarification"})
        self.assertEqual(reply.call_args.args[1:], ("Q1", "Clarification"))

    def test_local_http_static_state_and_token_protection(self):
        app = web_ui.DemoApp()
        server = ThreadingHTTPServer(("127.0.0.1", 0), web_ui.handler_for(app))
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        base = f"http://127.0.0.1:{server.server_port}"
        try:
            with urlopen(base) as response:
                self.assertIn(b"Business Analysis Assistant", response.read())
            with urlopen(base + "/app.js") as response:
                self.assertIn(b"textContent", response.read())
            with urlopen(base + "/api/state") as response:
                self.assertEqual(json.load(response)["token"], app.token)
            for headers in ({}, {"X-Demo-Token": app.token, "Origin": "https://example.org"}):
                with self.assertRaises(HTTPError) as caught:
                    urlopen(Request(base + "/api/action", data=b'{"action":"reset"}', headers=headers))
                self.assertEqual(caught.exception.code, 403)
                caught.exception.close()
            request = Request(base + "/api/action", data=b'{"action":"reset"}', headers={"X-Demo-Token": app.token})
            with urlopen(request) as response:
                self.assertIsNone(json.load(response)["session"])
        finally:
            server.shutdown()
            server.server_close()
            worker.join()


if __name__ == "__main__":
    unittest.main()
