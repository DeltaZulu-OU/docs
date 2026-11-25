import csv
import io
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from extract import (MAPPING_HEADER, TESTER_HEADER, check_mapping, compare_native, parse_native,
                     parse_tester, parse_yaml)
from reference import FAMILIES, git_blob, read_manifest, verify_bytes


def tester(extra=()):
    output = io.StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow(TESTER_HEADER)
    writer.writerow(["EventType", "string", "Mandatory", "Common", "Enumerated", "a|b", "", "", ""])
    for family in FAMILIES:
        writer.writerow(["EventType", "string", "Mandatory", family, "Enumerated", "c|d", "", "", ""])
        writer.writerow(["EventCount", "int", "Optional", family, "", "", "", "", ""])
    writer.writerows(extra)
    return output.getvalue()


class ReferenceTests(unittest.TestCase):
    def test_manifest(self):
        m = read_manifest()
        self.assertEqual(set(m["families"]), set(FAMILIES))

    def test_git_blob(self):
        self.assertEqual(git_blob(b""), "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391")
        verify_bytes({"source": "sentinel", "path": "file", "blob": git_blob(b"abc")}, b"abc")
        with self.assertRaises(ValueError):
            verify_bytes({"source": "sentinel", "path": "file", "blob": git_blob(b"abc")}, b"xyz")

    def test_tester_overrides_preserve_enums(self):
        fields, overrides = parse_tester(tester())
        self.assertEqual(len(overrides), len(FAMILIES))
        self.assertEqual(fields["Dns"]["EventType"]["ListOfValues"], "c|d")
        self.assertEqual(overrides[0]["common"]["ListOfValues"], "a|b")

    def test_unknown_type_and_duplicate_rejected(self):
        for row in (["X", "unknown", "Optional", "Dns", "", "", "", "", ""],
                    ["EventType", "string", "Mandatory", "Dns", "", "", "", "", ""]):
            with self.subTest(row=row), self.assertRaises(ValueError):
                parse_tester(tester([row]))

    def test_native_columns_and_diff(self):
        markdown = "# Test\n\n## Columns\n\n| Column | Type | Description |\n|---|---|---|\n| EventCount | long | Count |\n| NativeOnly | string | Extra |\n"
        native = parse_native(markdown, "Test")
        fields, _ = parse_tester(tester())
        diff = compare_native(fields["Dns"], native)
        self.assertEqual(diff["native_only"], ["NativeOnly"])
        self.assertEqual(diff["tester_only"], ["EventType"])
        self.assertEqual(diff["type_conflicts"], [{"field": "EventCount", "tester": "int", "native": "long"}])
        with self.assertRaises(ValueError):
            parse_native(markdown.replace("long", "unknown"), "Test")
        with self.assertRaises(ValueError):
            parse_native(markdown + "| EventCount | long | duplicate |\n", "Test")

    def test_yaml_preserves_spellings_and_rejects_duplicates(self):
        self.assertEqual(parse_yaml("Version: 0.1.0\nName: yes\n"), {"Version": "0.1.0", "Name": "yes"})
        with self.assertRaises(ValueError):
            parse_yaml("Name: a\nName: b\n")

    def test_mapping_checks_metadata_and_coverage(self):
        fields, _ = parse_tester(tester())
        output = io.StringIO(newline="")
        writer = csv.writer(output)
        writer.writerow(MAPPING_HEADER)
        for family, entries in fields.items():
            for name, r in entries.items():
                writer.writerow([family, name, r["ColumnType"], r["Class"], r["LogicalType"],
                                 r["Aliased"], r["Schema"], "review", ""])
        valid = output.getvalue()
        check_mapping(valid, fields)
        with self.assertRaises(ValueError):
            check_mapping(valid.replace("EventCount,int", "EventCount,string", 1), fields)
        with self.assertRaises(ValueError):
            check_mapping("\n".join(valid.splitlines()[:-1]), fields)


if __name__ == "__main__":
    unittest.main()
