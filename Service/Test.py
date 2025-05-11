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
