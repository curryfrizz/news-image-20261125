#!/usr/bin/env python3
"""news-image-20261125 entry (program/v1, Python 3.13, standard library only).

Writes the repository's entry.png - a one-page newspaper summing up the
world news of Wednesday 25 November 2026 - to /output/entry.png. The image
is drawn ahead of time by draw_image.py (also in this repository) and
shipped beside this program; this program simply copies it, byte for
byte, so two runs always produce identical output. No network is used.

Never chmod the output directory itself: it belongs to the harness, and
chmod-ing it can fail or be rejected. Only the file we write gets a mode.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
import stat
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    shutil.copyfile(SOURCE, target)
    # The grader collects outputs as a different user: keep the file
    # readable by everyone (0644).
    os.chmod(target, 0o644)
    size = target.stat().st_size
    assert stat.S_ISREG(target.stat().st_mode) and size > 0
    print(f"wrote {target} ({size} bytes)")


if __name__ == "__main__":
    main()
