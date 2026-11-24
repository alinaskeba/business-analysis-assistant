"""Offline comparison of organized model contracts with the evaluated v1.2 snapshot."""
import importlib.util
import json
from pathlib import Path
import sys
import types

from ba_assistant import business_analysis as ba, ba_workflow as wf, plan_sources as ps

ROOT = Path(__file__).resolve().parents[1]


def main():
    snapshot = ROOT / 'dev/evaluation/final-system/v1.2-eval'
    old_ba = types.ModuleType('_evaluated_analysis')
    old_ba.__file__ = str(snapshot/'business_analysis.py')
    exec(compile((snapshot/'business_analysis.py').read_text(encoding='utf-8'), old_ba.__file__, 'exec'), old_ba.__dict__)
    old_wf = types.ModuleType('_evaluated_workflow')
    old_wf.__file__ = str(snapshot/'ba_workflow.py')
    prior = {name:sys.modules.get(name) for name in ('business_analysis','plan_sources')}
    try:
        sys.modules['business_analysis'] = old_ba
        sys.modules['plan_sources'] = ps
        exec(compile((snapshot/'ba_workflow.py').read_text(encoding='utf-8'), old_wf.__file__, 'exec'), old_wf.__dict__)
    finally:
        for name,value in prior.items():
            if value is None:sys.modules.pop(name,None)
            else:sys.modules[name]=value
    checks = {'analysis_prompt':ba.INSTRUCTIONS==old_ba.INSTRUCTIONS,
              'legacy_analysis_schema':ba.SCHEMA==old_ba.SCHEMA,
              'workflow_analysis_prompt':wf.ANALYSIS_INSTRUCTIONS==old_wf.ANALYSIS_INSTRUCTIONS,
              'workflow_analysis_schema':wf.ANALYSIS_SCHEMA==old_wf.ANALYSIS_SCHEMA,
              'plan_prompt':wf.PLAN_INSTRUCTIONS==old_wf.PLAN_INSTRUCTIONS,
              'plan_schema':wf.PLAN_SCHEMA==old_wf.PLAN_SCHEMA}
    if not all(checks.values()):raise ValueError('Model contracts changed: '+str(checks))
    print(json.dumps({'mode':'offline','new_api_calls':0,'evaluated_model_contracts_unchanged':checks}))


if __name__=='__main__':main()
