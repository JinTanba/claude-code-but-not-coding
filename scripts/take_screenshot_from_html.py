from playwright.sync_api import sync_playwright
import argparse

def takescreenshot(html_path: str, content_selector: str, out: str, width: int=1280, height: int=800):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width":width, "height":height})
        page.goto(html_path, wait_until="networkidle")
        el = page.wait_for_selector(content_selector, state="visible")
        # 要素を自動でスクロール → その要素だけをスクショ
        el.screenshot(path=out)
        browser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Take a screenshot from an HTML file")
    parser.add_argument("--html_path", type=str, required=True)
    parser.add_argument("--content_selector", type=str, required=True)
    parser.add_argument("--out", type=str, required=True)
    parser.add_argument("--width", type=int, default=1280)
    parser.add_argument("--height", type=int, default=800)
    args = parser.parse_args()
    takescreenshot("file://" + args.html_path, args.content_selector, args.out, args.width, args.height)
