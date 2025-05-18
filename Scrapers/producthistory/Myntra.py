from Scrapers.producthistory.Util import Producthistory
from bs4 import BeautifulSoup
from Receiver.getUrlHtmlDataReceiver import *
from Controller.pojo.LinkDataResponse import getLinkDataResponse
from Scrapers.producthistory.utilPlayWright import ProductHistoryPlaywrightAsync

# productHistoryScraper = Producthistory(headless=True, timeout=40)



async def action(link: str):
    print("got link to scrape", link)
    scraperPlayWright = ProductHistoryPlaywrightAsync(headless=True, timeout=40)
    await scraperPlayWright.start()
    html = await scraperPlayWright.get_page_html(link)
    await scraperPlayWright.close()
    return extract_price_and_description(html)


def extract_price_and_description(html: str):
    soup = BeautifulSoup(html, 'html.parser')

    # 1. Product name
    product_name = soup.find('h2', id='productName').get_text(strip=True)

    # 2. Current price (top-level)
    current_price_tag = soup.find('span', class_='product-current-price')
    current_price = current_price_tag.get_text(strip=True) if current_price_tag else None

    # 3. “Last updated” text
    #    it’s the first <span> inside the div#lastUpdated
    last_updated_div = soup.find('div', id='lastUpdated')
    last_updated = last_updated_div.find('span').get_text(strip=True) if last_updated_div else None

    # 4. Highest MRP
    highest_mrp = (soup
                   .find('p', class_='product-mrp')
                   .find('span', class_='mrp')
                   .get_text(strip=True)
                   )

    # 5. Price stats (current, lowest, average, highest)
    stats = {}
    for stat_id in ('currentPrice', 'lowestPrice', 'averagePrice', 'highestPrice'):
        el = soup.find('div', id=stat_id)
        stats[stat_id] = el.get_text(strip=True) if el else None

    # Print everything out
    print("Product Name:   ", product_name)
    print("Current Price:  ", current_price)
    print("Last Updated:   ", last_updated)
    print("Highest MRP:    ", highest_mrp)
    return getLinkDataResponse(description=product_name, price=str(convert_price_to_decimal(current_price)))
    # print("Stats:")
    # for k, v in stats.items():
    #     print(f"  {k}: {v}")
