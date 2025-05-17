#!/usr/bin/env python3
"""
Async Playwright util for ProductHistory scraping:
- No nest_asyncio patching, designed to be used within existing async loops
- Launches headless Chromium
- Navigates to producthistory.in
- Submits a product URL
- Waits explicitly 10 seconds after submission and returns the page HTML
"""
import asyncio
from playwright.async_api import async_playwright, Browser, Page
from datetime import datetime

def log(msg: str):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

class ProductHistoryPlaywrightAsync:
    def __init__(self, headless: bool = True, timeout: int = 20):
        self.headless = headless
        # timeout in milliseconds for navigation and selectors
        self.timeout = timeout * 1000
        self.browser: Browser | None = None
        self.page: Page | None = None
        self._playwright = None

    async def start(self) -> None:
        """Launch the Playwright browser and open a new page."""
        self._playwright = await async_playwright().start()
        self.browser = await self._playwright.chromium.launch(
            headless=self.headless,
               args=[
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-dev-shm-usage"
    ]
        )
        self.page = await self.browser.new_page()
        # Set default timeouts
        self.page.set_default_navigation_timeout(self.timeout)
        self.page.set_default_timeout(self.timeout)

    async def get_page_html(self, product_url: str):
        await self.page.goto("https://producthistory.in/", timeout=self.timeout)
        await self.page.wait_for_load_state("networkidle", timeout=self.timeout)

        input_loc = self.page.locator("#productUrl")
        await input_loc.scroll_into_view_if_needed()
        await input_loc.wait_for(state="visible", timeout=self.timeout)
        await input_loc.wait_for(state="enabled", timeout=self.timeout)
        await self.page.screenshot(path="before_fill.png")

        # Try the normal fill
        await input_loc.click()
        await input_loc.fill(product_url)

        # Fallback: force the DOM value if fill didn’t stick
        await self.page.evaluate(
            """(selector, value) => {
                 const el = document.querySelector(selector);
                 if (el) {
                   el.value = value;
                   el.dispatchEvent(new Event('input', { bubbles: true }));
                 }
               }""",
            "#productUrl",
            product_url
        )

        await self.page.screenshot(path="after_fill.png")

        # Submit
        await self.page.keyboard.press("Enter")

        # Let the results render
        await self.page.wait_for_timeout(10_000)

        html = await self.page.content()
        await self.page.screenshot(path="final_page.png")
        return html


    async def close(self) -> None:
        """Close the browser and Playwright instance."""
        if self.browser:
            await self.browser.close()
        if self._playwright:
            await self._playwright.stop()
        log("Browser closed")


# Example usage
def run_example():
    async def _main():
        scraper = ProductHistoryPlaywrightAsync(headless=False, timeout=20)
        await scraper.start()
        html = await scraper.get_page_html("https://www.myntra.com/handbags/caprese/caprese-floral-loged-sling-bag-with-pouch/30777601/buy")
        log(html[:200], "...")
        await scraper.close()

    try:
        asyncio.run(_main())
    except RuntimeError:
        # In case event loop is already running (e.g., Colab/Jupyter)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(_main())

if __name__ == '__main__':
    run_example()
