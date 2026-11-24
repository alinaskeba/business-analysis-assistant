"""Plan source IDs and deterministic evidence hydration, separate from semantic review."""
import copy
import json
import re

import business_analysis as ba


ACTIVITIES = {
    "requirements_approval": r"approv\w* (?:the )?business requirements",
    "specification_preparation": r"prepar\w* (?:the )?specification|specification preparation",
    "specification_acceptance": r"specification acceptance|acceptance of (?:the )?specification|approv\w* (?:the )?specification",
    "uat_acceptance": r"user acceptance testing",
    "release_decision": r"(?:release|launch) decision",
}


def schema_from(legacy_schema):
    schema = json.loads(json.dumps(legacy_schema))  # Detach reused assignment/property dictionaries.
    citation = {"type": "array", "minItems": 1, "items": ba.STRING}
    items = [schema["properties"]["acceptance_criteria"]["items"]]
    raci = schema["properties"]["raci"]["items"]
    for code in ("accountable", "responsible", "consulted", "informed"):
        items.append(raci["properties"][code]["items"])
    for item in items:
        del item["properties"]["source"]
        item["properties"]["source_ids"] = copy.deepcopy(citation)
        item["required"] = list(item["properties"])
    raci["properties"]["activity_type"] = {"type": "string", "enum": [*ACTIVITIES, "implementation", "testing", "deployment", "other"]}
    raci["required"] = list(raci["properties"])
    return schema


def build_registry(sources):
    registry = {}
    for document, text in sources.items():
        # Retain actual substrings and offsets. Decimal points without following whitespace stay intact.
        for match in re.finditer(r"\S.*?(?:[.!?](?=\s|$)|$)", text, re.S):
            registry[f"S{len(registry)+1}"] = {"document": document, "quote": match.group(),
                                                "start": match.start(), "end": match.end()}
    return registry


def prepare_input(analysis, sources):
    registry = build_registry(sources)
    def convert(value):
        if isinstance(value, dict):
            result = {k: convert(v) for k, v in value.items() if k != "source"}
            if "source" in value:
                source = value["source"]
                if source["document"] not in sources or source["quote"] not in sources[source["document"]]:
                    raise ValueError("Approved input evidence does not match its source document")
                # Map exact character overlap with the true original span, including multi-sentence evidence.
                start = sources[source["document"]].index(source["quote"])
                end = start + len(source["quote"])
                result["source_ids"] = [sid for sid, entry in registry.items()
                    if entry["document"] == source["document"] and entry["start"] < end and entry["end"] > start]
            return result
        if isinstance(value, list):
            return [convert(v) for v in value]
        return value
    transformed = convert(analysis)
    role_sources = {r["id"]: {sid for duty in r["responsibilities"] for sid in duty["source_ids"]}
                    for r in transformed["team_roles"]}
    for role in transformed["team_roles"]:
        role_sources[role["id"]].update(sid for sid, entry in registry.items()
            if role["name"].casefold() in entry["quote"].casefold())
    governance = []
    for kind, pattern in ACTIVITIES.items():
        supported = []
        for role in transformed["team_roles"]:
            for sid in role_sources[role["id"]]:
                if re.search(pattern, registry[sid]["quote"], re.I):
                    supported.append({"role_id": role["id"], "source_id": sid})
        if supported:
            governance.append({"activity_type": kind, "evidence": sorted(supported, key=lambda r: (r["role_id"], r["source_id"]))})
    return {"approved_analysis": transformed, "source_registry": registry, "required_governance": governance}


def cited_records(plan):
    for i, item in enumerate(plan["acceptance_criteria"]):
        yield f"acceptance_criteria[{i}]", item
    for i, activity in enumerate(plan["raci"]):
        for code in ("accountable", "responsible", "consulted", "informed"):
            for j, item in enumerate(activity[code]):
                yield f"raci[{i}].{code}[{j}]", item


def plain(plan, registry):
    result = copy.deepcopy(plan)
    for path, item in cited_records(result):
        if "sources" in item:
            expected = [{"source_id": sid, **registry[sid]} for sid in item["source_ids"] if sid in registry]
            if item.pop("sources") != expected:
                raise ba.AnalysisValidationError([f"{path}.sources: hydrated evidence was modified"])
    return result


def hydrate(plan, registry):
    result = copy.deepcopy(plan)
    for path, item in cited_records(result):
        if any(sid not in registry for sid in item["source_ids"]):
            raise ba.AnalysisValidationError([f"{path}.source_ids: unknown source ID"])
        item["sources"] = [{"source_id": sid, **registry[sid]} for sid in item["source_ids"]]
    return result


def validate(plan, session, schema, legacy_validator):
    payload = prepare_input(session["analysis"], session["sources"])
    registry = payload["source_registry"]
    raw = plain(plan, registry)
    errors = ba.collect_schema_errors(raw, schema)
    if errors:
        raise ba.AnalysisValidationError(errors)
    for path, item in cited_records(raw):
        if len(item["source_ids"]) != len(set(item["source_ids"])):
            errors.append(f"{path}.source_ids: duplicate source ID")
        for sid in item["source_ids"]:
            if sid not in registry:
                errors.append(f"{path}.source_ids: unknown source ID")
    if errors:
        raise ba.AnalysisValidationError(errors)
    # Reuse existing structural, coverage and role checks with Python-resolved verbatim evidence.
    projected = copy.deepcopy(raw)
    for _, item in cited_records(projected):
        sid = item.pop("source_ids")[0]
        item["source"] = {k: registry[sid][k] for k in ("document", "quote")}
    for activity in projected["raci"]:
        del activity["activity_type"]
    try:
        legacy_validator(projected, session)
    except ba.AnalysisValidationError as exc:
        errors.extend(exc.errors)
    reqs = {r["id"]: r for r in payload["approved_analysis"]["requirements"]}
    roles = {r["id"]: {sid for duty in r["responsibilities"] for sid in duty["source_ids"]} |
             {sid for sid, entry in registry.items() if r["name"].casefold() in entry["quote"].casefold()}
             for r in payload["approved_analysis"]["team_roles"]}
    for i, item in enumerate(raw["acceptance_criteria"]):
        req = reqs.get(item["requirement_id"])
        if req and not set(req["source_ids"]) & set(item["source_ids"]):
            errors.append(f"acceptance_criteria[{i}]: sources do not support the referenced requirement's origin")
    for i, activity in enumerate(raw["raci"]):
        if activity["activity_type"] in ACTIVITIES and activity["task_ids"]:
            errors.append(f"raci[{i}]: governance activity must not reference product implementation tasks")
        for code in ("accountable", "responsible", "consulted", "informed"):
            for item in activity[code]:
                if item["role_id"] in roles and not set(item["source_ids"]) & roles[item["role_id"]]:
                    errors.append(f"raci[{i}].{code}: source does not support the assigned role's confirmed duties")
                pattern = ACTIVITIES.get(activity["activity_type"])
                if pattern and not any(re.search(pattern, registry[sid]["quote"], re.I) for sid in item["source_ids"]):
                    errors.append(f"raci[{i}].{code}: cited evidence concerns a different governance action")
    if not raw["open_questions"]:
        present = {r["activity_type"] for r in raw["raci"]}
        for required in payload["required_governance"]:
            if required["activity_type"] not in present:
                errors.append("raci: missing explicit governance activity " + required["activity_type"])
    if errors:
        raise ba.AnalysisValidationError(errors)
    return raw


def alignment_review(plan, analysis, sources):
    """Audit support links without claiming that ID validity proves semantic entailment."""
    payload = prepare_input(analysis, sources)
    audit = []
    for path, item in cited_records(plan):
        audit.append({"path": path, "source_ids": item["source_ids"],
                      "evidence": [payload["source_registry"][sid] for sid in item["source_ids"] if sid in payload["source_registry"]],
                      "status": "needs_semantic_review",
                      "check": "Verify full actor/action/conditions/scope or actual RACI authority against these fragments."})
    return audit
