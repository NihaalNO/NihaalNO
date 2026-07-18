from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def run(name: str) -> None:
    subprocess.run([sys.executable, str(HERE / name)], check=True)


if __name__ == "__main__":
    run("make_info_card.py")
    run("fetch_contributions.py")
    run("render_heatmap_svg.py")
