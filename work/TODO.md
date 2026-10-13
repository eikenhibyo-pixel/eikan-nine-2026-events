# 2026-10-13 比較表公開

最悪: グローバルな表CSSによって既存候補一覧または比較表が崩れる。
反証: 表の転記だけでは再取り込み時に消えるため、テンプレートを取り込み処理に組み込む。

- [x] `scripts/templates/training-efficiency.html` に表・条件・出典を配置。
- [x] `scripts/import_world_team.py` に追記処理、`assets/training-efficiency.css` に専用表示を追加。
- [x] `python3 -m pytest -q tests/` で取り込み・冪等性・生成物一致・PC/スマホ表示を検証。5 passed in 2.45s。
- [ ] 通常のghラッパーで公開し、Pages反映を確認。
