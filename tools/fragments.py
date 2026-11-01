"""Regenerate or check saved root-source fragments; retain three historical orphans."""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from extract_code import FragmentError, collect_fragments, write_fragments  # noqa: E402

# These older Sudoku declarations/wrappers have no current root-source markers.
HISTORICAL_FRAGMENTS = {"cell_instance_cut", "make_move_sudoku_cut", "unmake_move_sudoku_cut"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Report drift without writing files")
    args = parser.parse_args(argv)
    try:
        expected = collect_fragments([ROOT])
        destination = ROOT / "code-fragments"
        saved = {path.name: path for path in destination.iterdir() if path.is_file()}
        unexpected = saved.keys() - expected.keys() - HISTORICAL_FRAGMENTS
        if unexpected:
            parser.error("Unrecognized saved fragments: " + ", ".join(sorted(unexpected)))
        if not args.check:
            write_fragments(expected, destination)
            print(
                f"Updated {len(expected)} fragments; retained {len(HISTORICAL_FRAGMENTS)} historical copies"
            )
            return 0
        drift = [
            name
            for name, text in expected.items()
            if name not in saved or saved[name].read_text() != text
        ]
        if drift:
            print(
                "Saved fragments differ from source: " + ", ".join(sorted(drift)), file=sys.stderr
            )
            return 1
        print(f"All {len(expected)} generated fragments match their source")
        return 0
    except (OSError, FragmentError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    raise SystemExit(main())
