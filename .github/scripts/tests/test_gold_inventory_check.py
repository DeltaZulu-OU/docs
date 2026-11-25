"""Source inventory drift checker regression fixtures."""
import importlib.util
from pathlib import Path
from unittest import TestCase

path = Path(__file__).resolve().parents[1] / "gold_inventory_check.py"
spec = importlib.util.spec_from_file_location("gold_inventory_check", path)
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)

def code_sample(name="Dns", field="Q"):
    return (f"public static readonly IReadOnlyList<ColumnDef> {name}Columns = "
            f"[new(\"{field}\", DuckDbType.Varchar, KustoType.String)];")

def doc_sample(name="Dns", field="Q", typed="String / Varchar"):
    return (f"## `golden.{name}` — 1 fields (ASIM 1.0.0)\n"
            "| Existing Gold field | Existing Kusto / DuckDB | Candidate | Disposition | Check |\n"
            "|---|---|---|---|---|\n"
            f"| `{field}` | `{typed}` | `Dummy` | review | fixture |\n\n")

class GoldInventoryCheckTests(TestCase):
    def test_extracts_names_and_types(self):
        self.assertEqual(check.extract_code(code_sample()),
                         {"Dns": [("Q", "String", "Varchar")]})
        self.assertEqual(check.extract_register(doc_sample()),
                         {"Dns": [("Q", "String", "Varchar")]})

    def test_reports_missing_family(self):
        self.assertTrue(any("missing families" in x for x in check.check(code_sample(), doc_sample())))

    def test_reports_field_or_type_drift(self):
        sources = "".join(code_sample(f) for f in check.EXPECTED)
        docs = "".join(doc_sample(f) for f in check.EXPECTED)
        self.assertEqual(check.check(sources, docs), [])
        self.assertTrue(any("source columns/types/order differ" in x for x
                            in check.check(sources, docs.replace("`String / Varchar`", "`Long / BigInt`"))))
        self.assertTrue(any("source columns/types/order differ" in x for x
                            in check.check(sources, docs.replace("`Q`", "`Missing`"))))

    def test_section_count_mismatch_is_error(self):
        with self.assertRaises(ValueError):
            check.extract_register(doc_sample().replace("— 1 fields", "— 2 fields"))

    def test_unexpected_source_family_is_error(self):
        sources = "".join(code_sample(f) for f in check.EXPECTED)
        docs = "".join(doc_sample(f) for f in check.EXPECTED)
        self.assertTrue(any("unexpected families" in x for x in
                            check.check(sources + code_sample("FileEvent"), docs)))

    def test_explicit_constructor_is_not_ignored(self):
        src = code_sample().replace("];", ', new ColumnDef("Extra", DuckDbType.Integer, KustoType.Int)];')
        self.assertEqual(len(check.extract_code(src)["Dns"]), 2)

    def test_unknown_column_syntax_fails(self):
        with self.assertRaises(ValueError):
            check.extract_code(code_sample().replace("];", ", MakeColumn()];"))

    def test_catalog_registration_must_match(self):
        catalog = "CanonicalViews { get; } = [GoldenEventContracts.Dns];"
        check.check_catalog(catalog, {"Dns"})
        with self.assertRaises(ValueError):
            check.check_catalog(catalog, {"Dns", "Authentication"})
