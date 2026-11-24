"""Escaped, print-ready individual documents; browser Save as PDF needs no new dependency."""
from html import escape
import copy
import ba_workflow as wf

TITLES = {"specification": "Specification", "tasks": "Implementation tasks",
          "acceptance_criteria": "Acceptance criteria", "raci": "RACI"}


def render_value(value):
    if isinstance(value, dict):
        if "quote" in value and "document" in value:
            return f'<blockquote><b>{escape(str(value["document"]))}</b>: {escape(str(value["quote"]))}</blockquote>'
        return '<dl>' + ''.join(f'<dt>{escape(k.replace("_", " ").title())}</dt><dd>{render_value(v)}</dd>' for k, v in value.items()) + '</dl>'
    if isinstance(value, list):
        return ''.join(f'<article>{render_value(v)}</article>' for v in value) or '<p>None</p>'
    if isinstance(value, bool):
        return 'Yes' if value else 'No'
    return escape(str(value))


def render(session, kind):
    if kind not in TITLES:
        raise ValueError("Unknown document type")
    wf.render_documents(session)  # Reject stale approval, modified evidence and invalid packages.
    value = copy.deepcopy(session["documents"][kind])
    if kind == "raci":
        names = {role["id"]: role["name"] for role in session["analysis"]["team_roles"]}
        for row in value:
            for code in ("accountable", "responsible", "consulted", "informed"):
                for assignment in row[code]:
                    assignment["role_name"] = names[assignment["role_id"]]
    title = TITLES[kind]
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>{title} - Business Analysis Assistant</title><style>
body{{font:14px/1.5 system-ui,sans-serif;color:#17273f;max-width:900px;margin:32px auto;padding:0 24px}}
h1{{font-size:28px}}article{{border-top:1px solid #ddd;padding:12px 0;margin:8px 0}}
dt{{font-weight:650;margin-top:8px}}dd{{margin-left:16px;white-space:pre-wrap;overflow-wrap:anywhere}}
blockquote{{border-left:3px solid #b8c9e8;padding-left:12px;margin:8px 0;color:#526078}}
button{{background:#315bda;color:white;border:0;border-radius:6px;padding:12px;font:inherit;cursor:pointer}}
.note{{background:#fff4e6;padding:12px}}@page{{size:A4;margin:18mm}}
@media print{{body{{margin:0;padding:0;max-width:none;font-size:10pt}}.toolbar{{display:none}}h1,dt{{break-after:avoid}}blockquote{{break-inside:avoid}}}}
</style><script src="/print.js" defer></script></head><body>
<div class="toolbar"><button id="print">Print / Save as PDF</button><p>Select Save as PDF in the destination list. Each export contains only this document.</p></div>
<h1>{title}</h1><p>Business Analysis Assistant · Requirements revision {session['revision']}</p>
<p class="note">Draft for document review. Requirements approval and automated validation do not replace human review of document content.</p>
{render_value(value)}</body></html>'''
