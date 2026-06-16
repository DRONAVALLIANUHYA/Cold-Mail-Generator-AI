from playwright.sync_api import sync_playwright

def scrape_job(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        page.goto(url, wait_until="networkidle")

        text = page.locator("body").inner_text()

        browser.close()

        return text