import os



def action():
    output = os.system("curl --location 'https://www.myntra.com/tshirts/aeropostale/aeropostale-brand-logo-printed-relaxed-fit-drop-shoulder-sleeves-pure-cotton-t-shirt/31101891/buy' \
    --header 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:138.0) Gecko/20100101 Firefox/138.0'")

    return output
