"""Keep the source-to-port inventory complete as current C examples are added."""

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class PortInventory(unittest.TestCase):
    def test_each_current_c_source_has_one_documented_port_family(self):
        manifest = json.loads((ROOT / "docs" / "PORT_COVERAGE.json").read_text())
        expected = {p.name for p in ROOT.iterdir() if p.suffix in (".c", ".h")}
        entries = [source for family in manifest["families"] for source in family["c_sources"]]
        self.assertEqual(set(entries), expected)
        self.assertEqual(len(entries), len(set(entries)))
        for family in manifest["families"]:
            for language in ("cpp", "java", "python"):
                with self.subTest(family=family["family"], language=language):
                    self.assertTrue((ROOT / family[language]).is_file())


if __name__ == "__main__":
    unittest.main()
