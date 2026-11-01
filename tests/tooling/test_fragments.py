"""Exercise extraction semantics and error handling with independent small sources."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import extract_code  # noqa: E402


class FragmentExtraction(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="adm-fragments-")
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)

    def source(self, name, text):
        path = self.directory / name
        path.write_text(text)
        return path

    def test_nested_regions_include_inner_code_without_markers(self):
        source = self.source(
            "nested.c",
            "outside\n/* [[[ outer */\nfirst\n/* [[[ inner */\nsecond\n"
            "/* ]]] */\nthird\n/* ]]] */\noutside\n",
        )
        self.assertEqual(
            extract_code.extract_fragments(source),
            {"inner": "second\n", "outer": "first\nsecond\nthird\n"},
        )

    def test_hyphenated_and_empty_regions(self):
        source = self.source("empty.h", "/* [[[ a-b */\n/* ]]] */\n")
        self.assertEqual(extract_code.extract_fragments(source), {"a-b": ""})

    def test_unbalanced_and_invalid_markers_have_line_diagnostics(self):
        for text, expected in [
            ("/* ]]] */\n", "closing marker"),
            ("/* [[[ unfinished */\nbody\n", "unclosed fragment"),
            ("/* [[[ ../escape */\n", "malformed fragment"),
            ("/* [[[ x */\n/* ]]] */\n/* [[[ x */\n/* ]]] */\n", "duplicate fragment"),
        ]:
            with self.subTest(expected=expected):
                source = self.source("invalid.c", text)
                with self.assertRaisesRegex(extract_code.FragmentError, expected) as raised:
                    extract_code.extract_fragments(source)
                self.assertIn("invalid.c:", str(raised.exception))

    def test_directory_selection_ignores_binaries_and_subdirectories(self):
        self.source("z.h", "/* [[[ z */\nlast\n/* ]]] */\n")
        self.source("a.c", "/* [[[ a */\nfirst\n/* ]]] */\n")
        (self.directory / "program").write_bytes(b"\xff\x00")
        (self.directory / "directory.c").mkdir()
        fragments = extract_code.collect_fragments([self.directory])
        self.assertEqual(list(fragments), ["a", "z"])

    def test_duplicate_names_across_sources_are_rejected(self):
        first = self.source("first.c", "/* [[[ same */\none\n/* ]]] */\n")
        second = self.source("second.h", "/* [[[ same */\ntwo\n/* ]]] */\n")
        with self.assertRaisesRegex(extract_code.FragmentError, "occurs in both"):
            extract_code.collect_fragments([first, second])

    def test_legacy_comment_encoding(self):
        source = self.directory / "latin1.c"
        source.write_bytes(b"/* [[[ comment */\n/* caf\xe9 */\n/* ]]] */\n")
        self.assertEqual(extract_code.extract_fragments(source), {"comment": "/* café */\n"})

    def test_cli_extension_and_complete_parse_before_writing(self):
        source = self.source("source.c", "/* [[[ example */\nint value;\n/* ]]] */\n")
        output = self.directory / "saved"
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "extract_code.py"),
                str(source),
                "-d",
                str(output),
                "-e",
                "c",
            ],
            capture_output=True,
            text=True,
            timeout=5,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((output / "example.c").read_text(), "int value;\n")
        broken = self.source("broken.c", "/* [[[ unfinished */\n")
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "extract_code.py"),
                str(source),
                str(broken),
                "-d",
                str(output),
                "-e",
                "c",
            ],
            capture_output=True,
            text=True,
            timeout=5,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("unclosed fragment", result.stderr)
        self.assertEqual((output / "example.c").read_text(), "int value;\n")


if __name__ == "__main__":
    unittest.main()
