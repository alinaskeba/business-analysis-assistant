# Project tools

Run from the repository root using Python module syntax:

| Command | Purpose | Model calls |
| --- | --- | --- |
| `python -m scripts.build_evaluation_figures` | Reproduce plots and metrics from saved evidence | None |
| `python -m scripts.build_submission` | Rebuild editable reports and architecture assets | None |
| `python -m scripts.prepare_github` | Build the ignore-aware archive and scan for credentials | None |
| `python -m scripts.verify_layout` | Compare prompts/schemas to the evaluated snapshot | None |
| `python -m scripts.evaluate_dev --help` | Offline saved-session evaluator for dev cases | None |
| `python -m scripts.collect_test_evaluation --help` | Prepare and explicitly collect test stages | Live actions only |

`run_component_eval.py` is the retained historical component runner used by regression tests.
The current workflow uses staged work/RACI generation in `ba_assistant/`. Older one-off launchers
are archived locally and excluded from the public repository. Reporting requires the optional
packages in `requirements-reporting.txt`; the application itself uses the standard library.
