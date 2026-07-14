import requests
import time

cases = ["Kilowatt Case", "Fracture Case", "Recoil Case"]

def steam_scrapper(case):
    baseurl = "https://steamcommunity.com/market/priceoverview/" # for price overview
    appid = 730
    currency = 1 # usd

    params = {
        "appid": appid,
        "currency": currency,
        "market_hash_name": case
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5"
    }

    res = requests.get(baseurl, params=params, headers=headers)
    print(res.status_code)
    print(res.text)
    data = res.json()
    
    return data
    
data = steam_scrapper("Kilowatt Case")
print(data)