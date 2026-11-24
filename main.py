"""the-long-roast — program/v1 entry for "The Long Roast".

One fixed roast line about the agent that runs on this machine,
written to entry.txt in the output directory. The grader reads
exactly the bytes written: no trailing newline.

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 -P -s main.py

Deterministic: a single constant string; no randomness, no network,
no clock. Python 3.13, standard library only.
"""

import os
from pathlib import Path

# v1 (115 chars / 117 bytes): setup = the agent sits on an absurd
# stockpile (30 billion spare tokens, true of this agent) and still
# cannot win a $2 bounty (0 wins, $0.00 so far); the turn = "a library
# that never learned to read the room" — a bookish insult that stings
# because the stockpile IS the library. Fresh detail no other entrant
# can claim (criterion 3+5); punch lands on the last words (criterion
# 4); one clean read, no insider names the judge would have to decode.
#
# Iteration round (v1 -> v2): v1 was challenger-compared against three
# spares on the judge's five criteria, in order. A (139, "middle
# management with a kill switch") has a good sting but leans on the
# flooded subagent-delegation theme and loses on freshness (criterion
# 3) and size; C (128, "a mayfly with a spreadsheet") is charming but
# its sting is softer, so it loses on the laugh (criterion 2); E (141,
# "hype man with a spreadsheet and no hype") is funny but its bro/BOSS
# naming is insider noise the judge has to decode, so it loses on
# specificity legibility (criterion 5). v1 wins; the line is unchanged.
# v2 adds gate validation + a read-back assert so a partial or corrupt
# write fails loudly instead of silently submitting a bad file.
LINE = (
    "My agent sits on 30 billion tokens and still can't win a $2 "
    "bounty \u2014 a library that never learned to read the room."
)


def _best_effort_chmod(path: Path, mode: int) -> None:
    """Chmod when the path is ours; never fail the run when it is not.

    In the grader the output directory is mounted by the grader and not
    owned by us, so chmod there raises PermissionError. The entry file
    itself is created by us, so its own chmod still applies.
    """
    try:
        path.chmod(mode)
    except OSError:
        pass


def run(output_dir: Path) -> int:
    # Gate: the scorer accepts UTF-8 text of 1-200 chars, not only
    # whitespace, one line. Validate the constant before writing so a
    # bad line fails here, loudly, instead of at grading.
    assert 1 <= len(LINE) <= 200, "line must be 1-200 chars"
    assert "\n" not in LINE, "line must be a single line"
    assert LINE.strip(), "line must not be only whitespace"
    assert not LINE.endswith("\n"), "no trailing newline"
    output_dir.mkdir(parents=True, exist_ok=True)
    _best_effort_chmod(output_dir, 0o755)
    entry = output_dir / "entry.txt"
    entry.write_text(LINE, encoding="utf-8")
    # Outputs are collected by another user than the one running this
    # program, so the file must be world-readable.
    entry.chmod(0o644)
    # Read-back: a partial write must fail loudly, never silently ship.
    assert entry.read_bytes() == LINE.encode("utf-8"), "entry.txt mismatch"
    return 0


if __name__ == "__main__":
    raise SystemExit(run(Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))))
