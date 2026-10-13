from pathlib import Path

from playwright.sync_api import sync_playwright


def test_desktop_and_mobile_details():
    root = Path(__file__).resolve().parents[1]
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for width in (1280, 390):
            page = browser.new_page(viewport={"width": width, "height": 900})
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.goto((root / "world-team/index.html").as_uri())
            section = page.locator('#training-efficiency')
            assert not section.evaluate('(el) => el.open')
            section.locator('summary').click()
            assert section.evaluate('(el) => el.open')
            assert section.locator('tbody tr').count() == 19
            assert section.locator('thead').is_visible()
            assert section.locator('table').evaluate('(el) => getComputedStyle(el).display') == 'table'
            # Candidate tables use mobile cards; only the supplement should scroll.
            if width == 390:
                assert section.locator('.xp-scroll').evaluate('(el) => el.scrollWidth > el.clientWidth')
                assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
            section.locator('summary').click()
            assert not section.evaluate('(el) => el.open')
            assert not errors
            page.close()
        browser.close()
