import copy
import json
from pathlib import Path
import unittest

import document_export as export
import business_analysis as ba


class ExportTests(unittest.TestCase):
    def setUp(self):
        self.session = json.loads((Path(__file__).parent / 'dev/demo/office-hours/verified.session.json').read_text(encoding='utf-8'))

    def test_each_export_contains_only_the_selected_document(self):
        for kind, title in export.TITLES.items():
            with self.subTest(kind=kind):
                html = export.render(self.session, kind)
                self.assertIn(f'<h1>{title}</h1>', html)
                self.assertIn('Print / Save as PDF', html)
                self.assertNotIn('<h1>' + ('RACI' if kind != 'raci' else 'Specification') + '</h1>', html)

    def test_untrusted_content_is_escaped(self):
        self.assertNotIn('<script>', export.render_value({'description': '<script>alert(1)</script>'}))
        self.assertIn('&lt;script&gt;', export.render_value('<script>'))

    def test_stale_approval_and_invalid_sources_cannot_be_exported(self):
        stale = copy.deepcopy(self.session)
        stale['revision'] += 1
        with self.assertRaises(ValueError):
            export.render(stale, 'tasks')
        invalid = copy.deepcopy(self.session)
        invalid['documents']['acceptance_criteria'][0]['sources'][0]['quote'] = 'Invented'
        with self.assertRaises(ba.AnalysisValidationError):
            export.render(invalid, 'acceptance_criteria')

    def test_unknown_document_is_rejected(self):
        with self.assertRaises(ValueError):
            export.render(self.session, '../.env')
