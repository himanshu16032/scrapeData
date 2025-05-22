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
from Service.LoggerService import log_info,log_error

def log(msg: str):
    log_info(msg)


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
        self.browser = await self._playwright.firefox.launch(
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
        """Navigate to producthistory, submit URL, wait, and return HTML."""
        if not self.page:
            raise RuntimeError("start() must be called before get_page_html()")
        try:
            log("→ Navigating to producthistory.in")
            await self.page.goto("https://producthistory.in/", timeout=self.timeout)

            log("→ Waiting for search input selector")

            await self.page.wait_for_selector("#productUrl", timeout=self.timeout)
            await self.page.wait_for_timeout(3_000)
            log("----------------------------------------")
            log("     ")
            log(await self.page.content())
            log("----------------------------------------")
            log("     ")
            log(f"→ Filling product URL: {product_url}")
            await self.page.type("#productUrl", product_url)
            await self.page.click("#searchButton", timeout=self.timeout)

            log("→ URL submitted; sleeping for 10 seconds…")
            # Explicit 10-second delay
            await self.page.wait_for_timeout(10_000)

            html = await self.page.content()
            log(html)
            log(f"Captured HTML length: {len(html)} chars")
            return html
        except Exception as e:
            log(f"Error fetching page HTML: {e}")
            return None

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
        html = await scraper.get_page_html(
            "https://www.myntra.com/handbags/caprese/caprese-floral-loged-sling-bag-with-pouch/30777601/buy")
        # log(html[:200], "...")
        await scraper.close()

    try:
        asyncio.run(_main())
    except RuntimeError:
        # In case event loop is already running (e.g., Colab/Jupyter)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(_main())


if __name__ == '__main__':
    run_example()
