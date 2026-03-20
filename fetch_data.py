import asyncio
import os
import pandas as pd
from deriv_api import DerivAPI

async def fetch_data(symbol="R_100", granularity=900, count=5000):
    app_id = 1089  # Default app_id for testing
    api = DerivAPI(app_id=app_id)

    print(f"Fetching historical data for {symbol}...")

    try:
        response = await api.ticks_history({
            'ticks_history': symbol,
            'adjust_start_time': 1,
            'count': count,
            'end': 'latest',
            'style': 'candles',
            'granularity': granularity
        })

        if 'candles' in response:
            candles = response['candles']
            df = pd.DataFrame(candles)
            df['datetime'] = pd.to_datetime(df['epoch'], unit='s')
            df = df[['datetime', 'open', 'high', 'low', 'close']]
            return df
        else:
            print("Failed to fetch candles.")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        await api.clear()

if __name__ == "__main__":
    df = asyncio.run(fetch_data())
    if df is not None:
        df.to_csv("r_100_15m.csv", index=False)
        print(f"Saved {len(df)} candles to r_100_15m.csv")
