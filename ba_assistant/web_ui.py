"""Local demonstration UI. Run: python app.py; open http://127.0.0.1:8000."""
import argparse
import json
import os
from pathlib import Path
import secrets
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Lock

from . import business_analysis as ba
from . import ba_workflow as wf
ROOT = Path(__file__).resolve().parents[1]


class DemoApp:
    def __init__(self):
        self.session = None
        self.lock = Lock()
        self.token = secrets.token_urlsafe(32)

    def state(self):
        return {"session": self.session,
                "blocking_reasons": wf.blocking_reasons(self.session) if self.session else []}

    def action(self, data):
        action = data.get("action")
        if action == "start":
            brief = data.get("brief", "")
            if not isinstance(brief, str):
                raise ValueError("Brief must be text")
            updated = wf.start_session(brief, ba.default_model())
        elif action == "load_demo":
            updated = json.loads((ROOT / "dev/demo/office-hours/verified.session.json").read_text(encoding="utf-8"))
            wf.validate_session(updated)
            wf.render_documents(updated)
            updated["demo_notice"] = "Saved live demo result. Approval was simulated for this demonstration, not supplied by you. No API call was made when loading."
        elif action == "reset":
            updated = None
        else:
            if self.session is None:
                raise ValueError("Analyze a brief first")
            if action == "reply":
                updated = wf.reply_to_session(self.session, data.get("question_id"), data.get("text"))
            elif action == "reply_many":
                updated = wf.reply_many_to_session(self.session, data.get("answers"))
            elif action == "request_changes":
                updated = wf.request_analysis_changes(self.session, data.get("text"))
            elif action == "approve":
                updated = wf.approve_session(self.session, data.get("message"))
            elif action in ("generate", "approve_generate"):
                if self.session.get("generation_progress", {}).get("raci_attempts", 0) >= 2:
                    raise ValueError("Both RACI attempts failed. Review the errors before starting a revised scenario.")
                if action == "approve_generate":
                    approved = wf.approve_session(self.session, "The reviewer clicked Approve & generate documents for this requirements revision.")
                    # Approval is a completed human action even if subsequent generation fails.
                    self.session = approved
                updated = wf.generate_documents(self.session)
            else:
                raise ValueError("Unknown action")
        self.session = updated
        return self.state()


def handler_for(app):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass  # Do not log briefs, answers or credentials.

        def send(self, status, value, content_type="application/json; charset=utf-8"):
            body = json.dumps(value, ensure_ascii=False).encode() if content_type.startswith("application/json") else value.encode()
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Content-Security-Policy", "default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self'; frame-ancestors 'none'; base-uri 'none'")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            if self.headers.get("Host") != f"127.0.0.1:{self.server.server_port}":
                return self.send(403, {"errors": ["Use the printed loopback address"]})
            if self.path == "/":
                return self.send(200, (ROOT / "web/index.html").read_text(encoding="utf-8"), "text/html; charset=utf-8")
            if self.path == "/app.js":
                return self.send(200, (ROOT / "web/app.js").read_text(encoding="utf-8"), "application/javascript; charset=utf-8")
            if self.path == "/generation.js":
                return self.send(200, (ROOT / "web/generation.js").read_text(encoding="utf-8"), "application/javascript; charset=utf-8")
            if self.path == "/print.js":
                return self.send(200, (ROOT / "web/print.js").read_text(encoding="utf-8"), "application/javascript; charset=utf-8")
            if self.path.startswith("/export/"):
                from . import document_export
                if not app.lock.acquire(blocking=False):
                    return self.send(409, {"errors": ["Generation is running; wait before exporting"]})
                try:
                    if not app.session:
                        raise ValueError("Generate documents first")
                    html = document_export.render(app.session, self.path.removeprefix("/export/"))
                    return self.send(200, html, "text/html; charset=utf-8")
                except ValueError as exc:
                    return self.send(422, {"errors": [str(exc)]})
                finally:
                    app.lock.release()
            if self.path == "/api/state":
                with app.lock:
                    return self.send(200, {**app.state(), "token": app.token, "example": ba.EXAMPLE,
                        "demo_brief": (ROOT / "dev/demo/office-hours/brief.txt").read_text(encoding="utf-8"),
                        "demo_available": (ROOT / "dev/demo/office-hours/verified.session.json").exists(),
                        "model": ba.default_model()})
            return self.send(404, {"errors": ["Not found"]})

        def do_POST(self):
            origin = f"http://127.0.0.1:{self.server.server_port}"
            if (self.headers.get("Host") != origin.removeprefix("http://")
                    or self.headers.get("Origin") not in (None, origin)
                    or self.headers.get("X-Demo-Token") != app.token):
                return self.send(403, {"errors": ["Invalid local request"]})
            if self.path != "/api/action":
                return self.send(404, {"errors": ["Not found"]})
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if length <= 0 or length > 200000:
                    raise ValueError("Invalid request size")
                data = json.loads(self.rfile.read(length))
                if not isinstance(data, dict):
                    raise ValueError("Request must be an object")
            except (ValueError, UnicodeError):
                return self.send(400, {"errors": ["Invalid JSON request"]})
            if not app.lock.acquire(blocking=False):
                return self.send(409, {"errors": ["Another action is running; please wait"]})
            try:
                self.send(200, app.action(data))
            except ba.AnalysisValidationError as exc:
                message = ("The generated documents failed validation. Your approved requirements are preserved; no new document package was accepted."
                           if data.get("action") in ("generate", "approve_generate") else
                           "The model response failed validation. Your answers have not been applied; the previous analysis is preserved. This does not mean you must answer every question.")
                self.send(422, {"errors": exc.errors, "previous_revision_preserved": True,
                    "message": message})
            except ValueError as exc:
                self.send(400, {"errors": [str(exc)]})
            except Exception:
                self.send(500, {"errors": ["Unexpected server error; the last accepted session is preserved"]})
            finally:
                app.lock.release()
    return Handler


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--session", type=Path, help="Resume an existing validated session JSON")
    args = parser.parse_args()
    ba.load_env()
    app = DemoApp()
    if args.session:
        app.session = json.loads(args.session.read_text(encoding="utf-8"))
        wf.validate_session(app.session)
    server = ThreadingHTTPServer(("127.0.0.1", args.port), handler_for(app))
    print(f"Business Analysis Assistant: http://127.0.0.1:{server.server_port}", flush=True)
    print("Sessions stay in memory until the server stops. Ctrl+C to stop.", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
