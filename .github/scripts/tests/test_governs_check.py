"""Governance checker regression tests. Run with python -m unittest discover."""
import importlib.util
from pathlib import Path
from unittest import TestCase
from tempfile import TemporaryDirectory
from contextlib import contextmanager
import os

script_path = Path(__file__).resolve().parents[1] / "governs_check.py"
spec = importlib.util.spec_from_file_location("governs_check", script_path)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)

@contextmanager
def fixture():
    old = os.getcwd()
    with TemporaryDirectory() as tmp:
        os.chdir(tmp)
        Path("decisions").mkdir()
        Path("constraints").mkdir()
        try:
            yield Path(tmp)
        finally:
            os.chdir(old)

def sample(status="Accepted"):
    return ("---\nid: DEC-0001\nstatus: " + status
            + "\nrepos: [DeltaZulu.Sample]\ngoverns:\n  types: [ExampleType]\n"
            + "  paths: [src/ExampleType.cs]\ncites: []\n---\n"
            + "\n# DEC-0001 — Example\n")

class GovernanceRegression(TestCase):
    def test_reject_missing_or_bad_frontmatter(self):
        for body in ("no frontmatter", "---\nid: [\n---\n", sample("Unknown")):
            with self.subTest(body=body), fixture():
                Path("decisions/DEC-0001-example.md").write_text(body)
                with self.assertRaises(ValueError):
                    checker.load_decisions()

    def test_reject_invalid_id_and_unresolved_reference(self):
        with fixture():
            p = Path("decisions/DEC-0001-example.md")
            p.write_text(sample().replace("DEC-0001", "DEC-0002"))
            with self.assertRaises(ValueError):
                checker.load_decisions()
            p.write_text(sample().replace("cites: []", "cites: [CON-9999]"))
            with self.assertRaises(ValueError):
                checker.load_decisions()

    def test_source_only_declaration(self):
        with fixture() as root:
            Path("decisions/DEC-0001-example.md").write_text(sample())
            checkout = root / "checkout" / "DeltaZulu.Sample"
            (checkout / "src").mkdir(parents=True)
            (checkout / "tests").mkdir()
            (checkout / "tests/ExampleType.cs").write_text("public class ExampleType {}")
            (checkout / "src/ExampleType.cs").write_text("// missing")
            self.assertEqual(checker.verify(root / "checkout"), 1)
            (checkout / "src/ExampleType.cs").write_text("namespace Sample;\npublic class ExampleType {}")
            self.assertEqual(checker.verify(root / "checkout"), 0)
            self.assertTrue(checker.type_is_declared(checkout, "Sample.ExampleType"))
            self.assertFalse(checker.type_is_declared(checkout, "Wrong.ExampleType"))

    def test_supersession_requires_target(self):
        with fixture():
            Path("decisions/DEC-0001-example.md").write_text(sample("Superseded"))
            with self.assertRaises(ValueError):
                checker.load_decisions()

    def test_empty_governs_does_not_hide_missing_repository(self):
        with fixture() as root:
            Path("decisions/DEC-0001-example.md").write_text(
                sample().replace("types: [ExampleType]", "types: []")
                        .replace("paths: [src/ExampleType.cs]", "paths: []")
            )
            self.assertEqual(checker.verify(root / "checkout"), 1)

    def test_commented_and_string_declarations_do_not_count(self):
        with fixture() as root:
            src = root / "src"
            src.mkdir()
            (src / "Example.cs").write_text('// class ExampleType {}\n/* class ExampleType {} */\n'
                                            'class Other { string text = "class ExampleType {}"; }')
            self.assertFalse(checker.type_is_declared(root, "ExampleType"))

    def test_status_relationship_and_reciprocity(self):
        with fixture():
            old = Path("decisions/DEC-0001-example.md")
            newer = Path("decisions/DEC-0002-example.md")
            old.write_text(sample("Superseded").replace("cites: []", "cites: []\nsuperseded_by: DEC-0002"))
            newer.write_text(sample().replace("DEC-0001", "DEC-0002"))
            with self.assertRaises(ValueError):
                checker.load_decisions()
            newer.write_text(sample().replace("DEC-0001", "DEC-0002").replace("cites: []", "cites: []\nsupersedes: [DEC-0001]"))
            self.assertEqual(len(checker.load_decisions()), 2)
