"""Local Markdown link validation regression tests."""
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
import importlib.util

path = Path(__file__).resolve().parents[1] / "current_links_check.py"
spec = importlib.util.spec_from_file_location("current_links_check", path)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class LocalLinksTests(TestCase):
    def test_local_existing_missing_external_and_anchor(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "decisions").mkdir()
            (root / "decisions/a.md").write_text(
                "[exists](../README.md) [same](#heading) "
                "[remote](https://example.org/test) [missing](../gone.md)"
            )
            (root / "README.md").write_text("# heading")
            errors = checker.links_for(root, ["decisions/a.md"])
            self.assertEqual(len(errors), 1)
            self.assertIn("gone.md", errors[0])

    def test_missing_source_fails(self):
        with TemporaryDirectory() as tmp:
            self.assertIn("missing", checker.links_for(Path(tmp), ["absent.md"])[0])

    def test_relative_traversal_fails(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "doc.md").write_text("[escape](../../outside.md)")
            self.assertEqual(len(checker.links_for(root, ["doc.md"])), 1)

    def test_valid_local_link(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "doc.md").write_text("[self](doc.md) [fragment](#top)")
            self.assertEqual(checker.links_for(root, ["doc.md"]), [])

    def test_code_fences_and_indentation(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "doc.md").write_text(
                "````text\n[code](missing.md)\n```\n[still code](missing.md)\n````\n"
                "~~~\n[code](missing.md)\n~~~\n    [indent](missing.md)\n[real](gone.md)"
            )
            errors = checker.links_for(root, ["doc.md"])
            self.assertEqual(len(errors), 1)
            self.assertIn("gone.md", errors[0])
