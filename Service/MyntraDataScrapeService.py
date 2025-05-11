# from playwright.async_api import async_playwright

from Receiver.getUrlHtmlDataReceiver import *
from Controller.pojo.LinkDataRequest import *
from Controller.pojo.LinkDataResponse import *
import requests
import json
from bs4 import BeautifulSoup


# from playwright.sync_api import sync_playwright


async def action(getLinkDataRequest: getLinkDataRequest):
    name, description, price, priceCurrency, availability = fetchData(getLinkDataRequest.link)
    return getLinkDataResponse(description=description, price=convert_price_to_decimal(price), name=name,
                               priceCurrency=priceCurrency, availability=availability)


def fetchData(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:138.0) Gecko/20100101 Firefox/138.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd"
    }
    session = requests.get(url=url,headers=headers)

    # 1. Pretend to be a real browser

    # 2. Hit the homepage to pick up cookies

    session.raise_for_status()

    # 3. Now fetch the actual product page
    html = session.text
    print(html)

    soup = BeautifulSoup(html, "html.parser")

    # Find all JSON-LD scripts and pick the one where "@type": "Product"
    product_data = None
    for tag in soup.find_all("script", {"type": "application/ld+json"}):
        try:
            data = json.loads(tag.string)
        except (json.JSONDecodeError, TypeError):
            continue

        # It may be a list or a dict
        items = data if isinstance(data, list) else [data]
        for item in items:
            if item.get("@type") == "Product":
                product_data = item
                break
        if product_data:
            break

    if not product_data:
        raise ValueError("No Product JSON-LD block found")

    # Extract fields
    name = product_data.get("name")
    description = product_data.get("description")
    offers = product_data.get("offers", {})
    price = offers.get("price")
    priceCurrency = offers.get("priceCurrency")
    availability = offers.get("availability")

    print(f"Name:        {name}")
    print(f"Description: {description}")
    print(f"Price:       {price}")
    print(f"Price Currency: {priceCurrency}")
    print(f"Availability: {availability}")

    return name, description, price, priceCurrency, availability


# async def fetch_description(URL):
#     print("given link ", URL)
#     browser = get_browser()
#     print("step1")
#     context = await browser.new_context()
#     print("step2")
#     page = await context.new_page()
#     print("step3")
#
#     try:
#         await page.goto(URL, wait_until="domcontentloaded")
#         print("step4")
#         await page.wait_for_selector(".pdp-name", timeout=20_000)
#         print("step5")
#         desc = await page.locator(".pdp-name").inner_text()
#         price = await page.locator(".pdp-price").inner_text()
#         return desc, price
#     except Exception as e:
#         print(f"Error fetching data: {e}")
#         return None, None
#     finally:
#         await page.close()
#         await context.close()


# global_browser.py
from playwright.sync_api import sync_playwright


#
# playwright = None
# browser = None

# playwright_context = {
#     "playwright": None,
#     "browser": None
# }


# async def init_browser():
#     pw = await async_playwright().start()
#     # Launch Chromium headless with sandbox disabled
#     browser = await pw.firefox.launch(
#         headless=True,
#         args=[
#             "--no-sandbox",
#             "--disable-setuid-sandbox",
#             "--disable-dev-shm-usage",  # avoids /dev/shm issues
#             "--disable-gpu",  # GPU off since headless
#         ]
#     )
#     playwright_context["playwright"] = pw
#     playwright_context["browser"] = browser


# async def close_browser():
#     await playwright_context["browser"].close()
#     await playwright_context["playwright"].stop()


# def get_browser():
#     browser = playwright_context.get("browser")
#     if browser is None:
#         raise RuntimeError("Browser not initialized. Make sure init_browser() has been called.")
#     return browser


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
