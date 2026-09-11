#!/usr/bin/env python3
"""Import the generated world-team report and add the shared site navigation."""

from __future__ import annotations

import argparse
from pathlib import Path


STYLESHEET = '<link rel="stylesheet" href="../assets/site-nav.css">'
NAVIGATION = """<nav class="site-nav" aria-label="資料ナビゲーション">
  <a class="site-brand" href="../">EIKAN HUB</a>
  <div class="site-links"><a href="../calendar/">カレンダー</a><a class="is-current" href="./">日本代表投手</a></div>
</nav>"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "source",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[2]
        / "eikan-nine-2026"
        / "outputs"
        / "world_team_prefecture_summary_2026.html",
    )
    parser.add_argument(
        "output",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "world-team" / "index.html",
    )
    args = parser.parse_args()

    html = args.source.read_text(encoding="utf-8")
    if STYLESHEET not in html:
        html = html.replace("</title>", f"</title>\n{STYLESHEET}", 1)
    if NAVIGATION not in html:
        html = html.replace("<body>", f"<body>\n{NAVIGATION}", 1)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(html, encoding="utf-8")
    print(f"imported={args.source} output={args.output}")


if __name__ == "__main__":
    main()
