import os
import subprocess
import  requests

url = "https://www.myntra.com/kurtis/anouk/anouk-v-neck-regular-sleeves-short-kurti/28886594/buy"
def action():
    cmd = [
        "curl",
        "--silent",                 # don’t print progress
        "--location",
        "--insecure",               # disable SSL verification
        url,
        "--header", "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:138.0) Gecko/20100101 Firefox/138.0"
    ]
    html = subprocess.check_output(cmd, text=True)  # captures stdout as string
    print(html)
    return html


def action2():
    cmd = [
        "curl",
        "--silent",
        "--location",
        "--insecure",
        url,
        "--header", "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:138.0) Gecko/20100101 Firefox/138.0"
    ]
    html = subprocess.check_output(cmd, text=True)
    print(html)
    return {"raw_html": html}

def action3():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:138.0) "
                      "Gecko/20100101 Firefox/138.0"
    }
    # disable SSL verification to bypass any cert issues
    resp = requests.get(url, headers=headers, verify=False, timeout=30)
    resp.raise_for_status()
    print(resp.text)
    return {"raw_html": resp.text}



import requests, re
from bs4 import BeautifulSoup
import requests
import json
from bs4 import BeautifulSoup
from typing import List, Optional, Dict

def getProxyList():
    regex = r"[0-9]+(?:\.[0-9]+){3}:[0-9]+"
    c = requests.get("https://spys.me/proxy.txt")
    test_str = c.text
    a = re.finditer(regex, test_str, re.MULTILINE)
    with open("proxies_list.txt", 'w') as file:
        for i in a:
           print(i.group(),file=file)

    d = requests.get("https://free-proxy-list.net/")
    soup = BeautifulSoup(d.content, 'html.parser')
    td_elements = soup.select('.fpl-list .table tbody tr td')
    ips = []
    ports = []
    proxyList = []
    for j in range(0, len(td_elements), 8):
        ips.append(td_elements[j].text.strip())
        ports.append(td_elements[j + 1].text.strip())
    with open("proxies_list.txt", "a") as myfile:
        for ip, port in zip(ips, ports):
            proxy = f"{ip}:{port}"
            proxyList.append(proxy)
    return proxyList



def fetch_product_with_proxies(
    url: str,
    proxy_list: List[str],
    timeout: int = 15
) -> Dict:
    """
    Attempts to fetch the Product JSON-LD block from `url` using each proxy in `proxy_list`.
    Returns the parsed product dict on success, or raises RuntimeError if all proxies fail.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;"
                  "q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-IN,en;q=0.9",
        "Referer": "https://www.myntra.com/",
        "Upgrade-Insecure-Requests": "1",
    }

    for proxy in proxy_list:
        session = requests.Session()
        session.headers.update(headers)
        # configure this proxy for both http and https
        session.proxies.update({
            "http": proxy,
            "https": proxy
        })
        try:
            # Seed cookies by hitting the homepage
            session.get("https://www.myntra.com/", timeout=timeout).raise_for_status()
            # Fetch the target page
            resp = session.get(url, timeout=timeout)
            resp.raise_for_status()
        except Exception as e:
            print(f"[!] Proxy {proxy} failed: {e}")
            continue

        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup.find_all("script", {"type": "application/ld+json"}):
            try:
                data = json.loads(tag.string)
            except (json.JSONDecodeError, TypeError):
                continue
            items = data if isinstance(data, list) else [data]
            for item in items:
                if item.get("@type") == "Product":
                    return item

        print(f"[!] Proxy {proxy} did not yield Product JSON-LD")
    raise RuntimeError("All proxies failed to fetch the product data")

def action4():
    product_url = (
        "https://www.myntra.com/kurtis/anouk/"
        "anouk-v-neck-regular-sleeves-short-kurti/28886594/buy"
    )
    # Replace these with your real proxy addresses
    proxies = getProxyList()
    print(proxies)
    try:
        product = fetch_product_with_proxies(product_url, proxies)
        print("Name:",        product["name"])
        print("Description:", product["description"])
        offers = product.get("offers", {})
        print("Price:",       offers.get("price"))
        print("Currency:",    offers.get("priceCurrency"))
        print("Availability:",offers.get("availability"))
    except RuntimeError as err:
        print("Failed:", err)
    return "ok"
