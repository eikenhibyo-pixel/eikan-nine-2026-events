import importlib.util
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("import_world_team", ROOT / "scripts/import_world_team.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_collapsed_supplement_preserves_original_content():
    original = '<html><head><title>test</title></head><body><table id="candidate-table"><tbody><tr><td>候補</td></tr></tbody></table><footer>foot</footer><script>filter()</script></body></html>'
    result = MODULE.prepare_html(original)
    supplement = MODULE.TRAINING_TEMPLATE.read_text(encoding="utf-8")
    assert '<details id="training-efficiency" class="method-details">' in result
    # Removal of only the intended additions must recover the original byte for byte.
    recovered = result.replace(supplement + "\n", "", 1)
    recovered = recovered.replace("\n" + MODULE.NAVIGATION, "", 1)
    for css in (MODULE.STYLESHEET, MODULE.TRAINING_STYLESHEET):
        recovered = recovered.replace("\n" + css, "", 1)
    assert recovered == original
    assert result.index('id="training-efficiency"') > result.index('</table>')
    assert MODULE.prepare_html(result) == result


def test_reference_table_order_and_conditions():
    html = MODULE.TRAINING_TEMPLATE.read_text(encoding="utf-8")
    rows = re.findall(r'<tr><th scope="row">(.*?)</tr>', html)
    assert len(rows) == 19
    efficiency = [float(re.search(r'／([\d.]+)</td>', row)[1]) for row in rows]
    assert efficiency == sorted(efficiency, reverse=True)
    assert all(row.count('<td>') == 4 for row in rows)
    assert '甲子園１勝・２回戦敗退の２試合' in html
    assert '３か月連続の成長を示すものではない' in html
    assert '暫定推計' in html


def test_missing_insertion_point_fails():
    with pytest.raises(ValueError, match="footer"):
        MODULE.prepare_html('<html><head><title>test</title></head><body></body></html>')


def test_generated_page_matches_template():
    html = (ROOT / 'world-team/index.html').read_text(encoding="utf-8")
    assert html.count(MODULE.TRAINING_TEMPLATE.read_text(encoding="utf-8")) == 1
    assert html.count(MODULE.TRAINING_STYLESHEET) == 1
