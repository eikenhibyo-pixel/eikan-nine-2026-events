# EIKAN HUB

GitHub Pagesで個人用資料をまとめる静的サイト。

## ページ構造

- `/` — 資料一覧
- `/calendar/` — 育成イベントカレンダー
- `/world-team/` — 1年目夏・高校日本代表投手候補
- `/assets/` — 共通ナビゲーション等

新しい資料は用途名のディレクトリを作り、その中へ `index.html` を置く。ルートの資料カードと `assets/site-nav.css` を使った共通ナビへリンクを追加する。

`world-team/index.html` の生成元は別リポジトリの `eikan-nine-2026/outputs/world_team_prefecture_summary_2026.html`。

生成元を更新した後は、Pages側で次を実行して共通ナビ付きのページを取り込む。

```bash
python3 scripts/import_world_team.py
```
