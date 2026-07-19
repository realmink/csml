from datetime import datetime
import requests
import sqlite3
import time

cases = ["Kilowatt Case", "Fracture Case", "Recoil Case", "Revolution Case", "Dreams & Nightmares Case", "Snakebite Case", "Operation Riptide Case", "Operation Broken Fang Case", "Prisma 2 Case", "Danger Zone Case", "Horizon Case", "Clutch Case", "Spectrum 2 Case", "Gamma 2 Case", "Chroma 3 Case", "Shadow Case", "Falchion Case", "Operation Breakout Weapon Case", "Shattered Web Case", "Huntsman Weapon Case"]

def steam_scraper(case):
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

def get_current_price(cases):
    results = {}

    for case in cases:
        data = steam_scraper(case)

        if data:
            results[case] = data

        time.sleep(1.5)
    return results

def data_collection():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    res = get_current_price(cases)
    connection = sqlite3.connect('data/raw/cases.db')
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cases(
            id integer primary key,
            case_name text,
            time_stamp text,
            lowest_price real,
            median_price real,
            volume integer 
        )
    """)
    
    for case, data in res.items():
    # cleaning up data before we send
        raw_lowest_price = data.get('lowest_price')
        if raw_lowest_price is not None:
            raw_lowest_price = raw_lowest_price.replace("$", "")
            clean_lowest_price = float(raw_lowest_price)
        else:
            clean_lowest_price = None

        raw_median_price = data.get('median_price')
        if raw_median_price is not None:
            raw_median_price = raw_median_price.replace("$", "")
            clean_median_price = float(raw_median_price)
        else:
            clean_median_price = None

        raw_volume = data.get('volume')
        if raw_volume is not None:
            raw_volume = raw_volume.replace(",", "")
            clean_volume = int(raw_volume)
        else:
            clean_volume = None
        
        cursor.execute("INSERT INTO cases (case_name, time_stamp, lowest_price, median_price, volume) VALUES (?, ?, ?, ?, ?)",
        (case, current_time, clean_lowest_price, clean_median_price, clean_volume))
        
    connection.commit()
    connection.close()
    
data_collection()