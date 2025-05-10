from playwright.async_api import async_playwright

from Receiver.getUrlHtmlDataReceiver import *
from Controller.pojo.LinkDataRequest import *
from Controller.pojo.LinkDataResponse import *

from playwright.sync_api import sync_playwright


async def action(getLinkDataRequest: getLinkDataRequest):
    desc, price = await fetch_description(getLinkDataRequest.link)
    print(desc, price)
    return getLinkDataResponse(description=desc, price=convert_price_to_decimal(price))


async def fetch_description(URL):
    print("given link ",URL)
    browser = get_browser()
    print("step1")
    context = await browser.new_context()
    print("step2")
    page = await context.new_page()
    print("step3")

    try:
        await page.goto(URL, wait_until="domcontentloaded")
        print("step4")
        await page.wait_for_selector(".pdp-name", timeout=20_000)
        print("step5")
        desc = await page.locator(".pdp-name").inner_text()
        price = await page.locator(".pdp-price").inner_text()
        return desc, price
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None, None
    finally:
        await page.close()
        await context.close()


# global_browser.py
from playwright.sync_api import sync_playwright

#
# playwright = None
# browser = None

playwright_context = {
    "playwright": None,
    "browser": None
}


async def init_browser():
    pw = await async_playwright().start()
    # Launch Chromium headless with sandbox disabled
    browser = await pw.chromium.launch(
        headless=True,
        args=[
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-dev-shm-usage",       # avoids /dev/shm issues
            "--disable-gpu",                 # GPU off since headless
        ]
    )
    playwright_context["playwright"] = pw
    playwright_context["browser"] = browser

async def close_browser():
    await playwright_context["browser"].close()
    await playwright_context["playwright"].stop()


def get_browser():
    browser = playwright_context.get("browser")
    if browser is None:
        raise RuntimeError("Browser not initialized. Make sure init_browser() has been called.")
    return browser

def convert_price_to_decimal(price_string):
    """
    Convert a price string (like '$19.99') to a decimal number.

    Args:
        price_string (str): The price string to convert

    Returns:
        float: The price as a decimal number
    """
    # Remove currency symbols, spaces, and any other non-numeric characters except for the decimal point
    cleaned_string = ''.join(char for char in price_string if char.isdigit() or char == '.')

    # Convert to float
    try:
        return float(cleaned_string)
    except ValueError:
        # Handle cases where there might be multiple decimal points after cleaning
        print(f"Error converting '{price_string}' to decimal")
        return None
