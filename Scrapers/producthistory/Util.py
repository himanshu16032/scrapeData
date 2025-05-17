
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# ✅ Configure logging to print timestamps
# logging.basicConfig(
#     level=print,
#     format="%(asctime)s [%(levelname)s]: %(message)s",
#     datefmt="%Y-%m-%d %H:%M:%S"
# )
CHROME_PATH = "/usr/bin/google-chrome-stable"
class Producthistory:
    def __init__(self, headless: bool = True, timeout: int = 20):
        chrome_opts = Options()
        if headless:
            chrome_opts.add_argument("--headless=new")
        chrome_opts.add_argument("--disable-blink-features=AutomationControlled")
        chrome_opts.add_argument("--no-sandbox")
        chrome_opts.add_argument("--disable-dev-shm-usage")
        chrome_opts.binary_location = CHROME_PATH

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_opts)
        self.wait = WebDriverWait(self.driver, timeout)
        print("Chrome launched (headless=%s), timeout=%ds", headless, timeout)

    def get_page_html(self, product_url: str):
        try:
            print("→ Navigating to producthistory.com")
            self.driver.get("https://producthistory.in/")

            print("→ Waiting for search bar")
            search = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='productUrl']"))
            )
            search.click()

            # 1) Clear existing input
            search.send_keys(product_url)

            # 4) Submit
            search.send_keys(Keys.ENTER)
            print("→ URL submitted; waiting for JSON-LD…")

            self.driver.implicitly_wait(10)
            time.sleep(1)

            # 5) Wait up to 20s for the JSON-LD <script> to appear in the DOM
            # print("Pausing for 10 seconds…")
            # time.sleep(10)  # ❌ Not ideal, but guarantees the delay
            # print("→ Resuming execution.")

            html = self.driver.page_source
            print("Captured HTML (%d chars)", len(html))
            return html

        except Exception as e:
            print("Error fetching page HTML: %s", e)
            return None

    def close(self):
        print("Closing Chrome")
        self.driver.quit()
        print("Browser closed")


#
# def extract_price_and_description(html: str):
#     soup = BeautifulSoup(html, 'html.parser')
#
# # 1. Product name
#     product_name = soup.find('h2', id='productName').get_text(strip=True)
#
#     # 2. Current price (top-level)
#     current_price_tag = soup.find('span', class_='product-current-price')
#     current_price = current_price_tag.get_text(strip=True) if current_price_tag else None
#
#     # 3. “Last updated” text
#     #    it’s the first <span> inside the div#lastUpdated
#     last_updated_div = soup.find('div', id='lastUpdated')
#     last_updated = last_updated_div.find('span').get_text(strip=True) if last_updated_div else None
#
#     # 4. Highest MRP
#     highest_mrp = (soup
#         .find('p', class_='product-mrp')
#         .find('span', class_='mrp')
#         .get_text(strip=True)
#     )
#
#     # 5. Price stats (current, lowest, average, highest)
#     stats = {}
#     for stat_id in ('currentPrice', 'lowestPrice', 'averagePrice', 'highestPrice'):
#         el = soup.find('div', id=stat_id)
#         stats[stat_id] = el.get_text(strip=True) if el else None
#
#     # Print everything out
#     print("Product Name:   ", product_name)
#     print("Current Price:  ", current_price)
#     print("Last Updated:   ", last_updated)
#     print("Highest MRP:    ", highest_mrp)
#     print("Stats:")
#     for k, v in stats.items():
#         print(f"  {k}: {v}")

# ——— Usage ———
# if __name__ == "__main__":
#     scraper = BuyhatkeScraper(headless=True, timeout=20)
#     try:
#         link = "https://www.myntra.com/co-ords/aeropostale/aeropostale-hooded-sweatshirt--shorts/30702310/buy"
#         html = scraper.get_page_html(link)
#         if html:
#             extract_price_and_description(html)
#         else:
#             print("❌ Failed to fetch HTML")
#     finally:
#         scraper.close()
