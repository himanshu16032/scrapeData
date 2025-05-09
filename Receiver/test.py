from playwright.sync_api import sync_playwright

URL =







def fetch_description():
    with sync_playwright() as pw:

        print("step1")
        browser = pw.firefox.launch(headless=True)
        print("step2")
        page = browser.new_page()
        print("step3")
        print("step4")

        # 1) Navigate and wait until the initial HTML and JS framework load:
        page.goto(URL, wait_until="domcontentloaded")
        print("step5")
        #    - “domcontentloaded” waits for the document to be parsed,
        #      but doesn’t stall forever on long‐lived XHRs.

        # 2) Then explicitly wait for your target element:
        page.wait_for_selector(".pdp-name", timeout=20_000)
        print("step6")

        # 3) Finally grab the text
        desc = page.locator(".pdp-name").inner_text()
        price = page.locator(".pdp-price").inner_text()
        print("step7")
        print("Description:", desc)
        print("price:", price)

        # 4) Tidy up
        page.close()
        # context.close()
        browser.close()

if __name__ == "__main__":
    fetch_description()
