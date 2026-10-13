#!/usr/bin/env python3
"""Import the generated world-team report and add the shared site navigation."""

from __future__ import annotations

import argparse
from pathlib import Path


STYLESHEET = '<link rel="stylesheet" href="../assets/site-nav.css">'
TRAINING_STYLESHEET = '<link rel="stylesheet" href="../assets/training-efficiency.css">'
TRAINING_TEMPLATE = Path(__file__).resolve().parent / "templates" / "training-efficiency.html"
NAVIGATION = """<nav class="site-nav" aria-label="資料ナビゲーション">
  <a class="site-brand" href="../">EIKAN HUB</a>
  <div class="site-links"><a href="../calendar/">カレンダー</a><a class="is-current" href="./">日本代表投手</a></div>
</nav>"""


def prepare_html(html: str) -> str:
    for stylesheet in (STYLESHEET, TRAINING_STYLESHEET):
        if stylesheet not in html:
            html = html.replace("</title>", f"</title>\n{stylesheet}", 1)
    if NAVIGATION not in html:
        html = html.replace("<body>", f"<body>\n{NAVIGATION}", 1)
    # Keep the reference outside the candidate table and its filtering logic.
    # The guard also allows an already imported page to be imported again.
    if 'id="training-efficiency"' not in html:
        if "<footer>" not in html:
            raise ValueError("world-team report has no footer insertion point")
        html = html.replace("<footer>", TRAINING_TEMPLATE.read_text(encoding="utf-8") + "\n<footer>", 1)
    return html


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

    html = prepare_html(args.source.read_text(encoding="utf-8"))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(html, encoding="utf-8")
    print(f"imported={args.source} output={args.output}")


if __name__ == "__main__":
    main()
