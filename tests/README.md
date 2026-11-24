# Tests and evaluation data

```powershell
python -m unittest discover -s tests -t . -q
node tests/test_generation_ui.cjs
```

There are 89 Python checks and four JavaScript UI-flow scenarios. They are offline software tests,
not independent model-quality observations. Imports use the `ba_assistant` and `scripts` packages.

- `ba_test_cases.json`: final test expectations.
- `EVALUATION.md`: collection and semantic scoring protocol.
- `evaluation/`: recorded requests, outputs, failures and derived statistics.
- `test_*.py`, `test_generation_ui.cjs`: software regression tests.

Historical evidence used as fixtures remains in `dev/` and `history/` at its original paths so
snapshot hashes and provenance references remain valid. Those files are not alternate application
implementations. Current runnable code is exclusively in `ba_assistant/`.
