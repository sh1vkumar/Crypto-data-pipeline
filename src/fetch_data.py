import requests
# import pyspark.sql as ps
from dotenv import load_dotenv
import os
import psycopg
import logging
import json
import time

LOG_FILE = "crypto_data.log"
logging.basicConfig(
    # filename='crypto_data.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),  # Write logs to a file
        logging.StreamHandler()  # Also log to console
    ]
)

load_dotenv()

API_KEY = os.getenv("API_KEY")

DB_PARAMS = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}


def fetch_data(API_KEY, CURRENCY, PER_PAGE=250):
    headers = {
        "accept": "application/json",
        "x-cg-pro-api-key": API_KEY
    }

    all_data = []
    page = 1

    while page<=5:
        url = (
            f"https://api.coingecko.com/api/v3/coins/markets"
            f"?vs_currency={CURRENCY}&per_page={PER_PAGE}&page={page}"
        )

        response = requests.get(url, headers=headers)

        if response.status_code == 429:
            print("Rate limit hit. Sleeping for 60 seconds...")
            time.sleep(60)
            continue

        if response.status_code != 200:
            raise Exception(f"Failed to fetch data on page {page}: {response.status_code}")

        data = response.json()

        # if not data:
        #     break  # No more data

        all_data.extend(data)
        print(f"Fetched page {page} with {len(data)} records.")
        page += 1
        time.sleep(3)  # 1 request every 2 seconds to stay under 30 RPM

    return all_data

CURRENCY = "usd"
PER_PAGE = 250
crypto_data = fetch_data(API_KEY,CURRENCY,PER_PAGE)


# Insert Crypto data into PostgreSQL
def insert_crypto_data(crypto_data):
    """Insert holiday data into PostgreSQL with batch processing.
    
    - If a holiday has no subdivisions, insert it for all subdivisions in the country.
    - If a holiday has specific subdivisions, insert it only for those subdivisions.
    """
    if not crypto_data:
        logging.info(f"No data to insert for {CURRENCY}.")
        return

    try:
        with psycopg.connect(**DB_PARAMS) as conn:
            with conn.cursor() as cur:
                insert_query = """ 
                    INSERT INTO crypto_data (
                        id, symbol, name, image, current_price, market_cap, market_cap_rank, 
                        fully_diluted_valuation, total_volume, high_24h, low_24h, 
                        price_change_24h, price_change_percentage_24h, 
                        market_cap_change_24h, market_cap_change_percentage_24h, 
                        circulating_supply, total_supply, max_supply, 
                        ath, ath_change_percentage, ath_date, 
                        atl, atl_change_percentage, atl_date, 
                        roi, last_updated
                    ) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id,last_updated) DO UPDATE SET
                        symbol = EXCLUDED.symbol,
                        name = EXCLUDED.name,
                        image = EXCLUDED.image,
                        current_price = EXCLUDED.current_price,
                        market_cap = EXCLUDED.market_cap,
                        market_cap_rank = EXCLUDED.market_cap_rank,
                        fully_diluted_valuation = EXCLUDED.fully_diluted_valuation,
                        total_volume = EXCLUDED.total_volume,
                        high_24h = EXCLUDED.high_24h,
                        low_24h = EXCLUDED.low_24h,
                        price_change_24h = EXCLUDED.price_change_24h,
                        price_change_percentage_24h = EXCLUDED.price_change_percentage_24h,
                        market_cap_change_24h = EXCLUDED.market_cap_change_24h,
                        market_cap_change_percentage_24h = EXCLUDED.market_cap_change_percentage_24h,
                        circulating_supply = EXCLUDED.circulating_supply,
                        total_supply = EXCLUDED.total_supply,
                        max_supply = EXCLUDED.max_supply,
                        ath = EXCLUDED.ath,
                        ath_change_percentage = EXCLUDED.ath_change_percentage,
                        ath_date = EXCLUDED.ath_date,
                        atl = EXCLUDED.atl,
                        atl_change_percentage = EXCLUDED.atl_change_percentage,
                        atl_date = EXCLUDED.atl_date,
                        roi = EXCLUDED.roi,
                        last_updated = EXCLUDED.last_updated;
                    """
                values = []

                for crypto in crypto_data:
                    id_ = crypto.get("id")
                    symbol = crypto.get("symbol")
                    name = crypto.get("name")
                    image = crypto.get("image")
                    current_price = crypto.get("current_price")
                    market_cap = crypto.get("market_cap")
                    market_cap_rank = crypto.get("market_cap_rank")
                    fully_diluted_valuation = crypto.get("fully_diluted_valuation")
                    total_volume = crypto.get("total_volume")
                    high_24h = crypto.get("high_24h")
                    low_24h = crypto.get("low_24h")
                    price_change_24h = crypto.get("price_change_24h")
                    price_change_percentage_24h = crypto.get("price_change_percentage_24h")
                    market_cap_change_24h = crypto.get("market_cap_change_24h")
                    market_cap_change_percentage_24h = crypto.get("market_cap_change_percentage_24h")
                    circulating_supply = crypto.get("circulating_supply")
                    total_supply = crypto.get("total_supply")
                    max_supply = crypto.get("max_supply")
                    ath = crypto.get("ath")
                    ath_change_percentage = crypto.get("ath_change_percentage")
                    ath_date = crypto.get("ath_date")
                    atl = crypto.get("atl")
                    atl_change_percentage = crypto.get("atl_change_percentage")
                    atl_date = crypto.get("atl_date")
                    roi = crypto.get("roi")  # might be None or dict
                    roi_json = json.dumps(roi) if roi else None
                    last_updated = crypto.get("last_updated")

                    values.append((
                        id_, symbol, name, image, current_price, market_cap, market_cap_rank,
                        fully_diluted_valuation, total_volume, high_24h, low_24h,
                        price_change_24h, price_change_percentage_24h,
                        market_cap_change_24h, market_cap_change_percentage_24h,
                        circulating_supply, total_supply, max_supply,
                        ath, ath_change_percentage, ath_date,
                        atl, atl_change_percentage, atl_date,
                        roi_json, last_updated
                    ))

                # Ensure there is data to insert
                if values:
                    # print(f"Values to be inserted: {values[0]}")
                    # cur.execute(insert_query, values[0])
                    cur.executemany(insert_query, values)
                    conn.commit()
                    logging.info(f"Inserted {len(values)} crypto records.")
                else:
                    logging.info("No valid crypto data to insert.")

    except Exception as e:
        logging.error(f"Error inserting Crypto Data for {CURRENCY}: {e}")

insert_crypto_data(crypto_data)

