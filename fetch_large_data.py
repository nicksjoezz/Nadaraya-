import asyncio
import os
import pandas as pd
from deriv_api import DerivAPI

async def fetch_large_data(symbol="R_100", granularity=900, total_count=100000):
    app_id = 1089
    api = DerivAPI(app_id=app_id)

    print(f"Fetching up to {total_count} historical candles for {symbol}...")

    all_candles = []
    end_time = 'latest'
    remaining = total_count

    while remaining > 0:
        count = min(remaining, 5000)
        try:
            response = await api.ticks_history({
                'ticks_history': symbol,
                'adjust_start_time': 1,
                'count': count,
                'end': end_time,
                'style': 'candles',
                'granularity': granularity
            })

            if 'candles' in response and response['candles']:
                candles = response['candles']
                all_candles.extend(candles)
                remaining -= len(candles)
                end_time = candles[0]['epoch'] - 1

                if len(candles) < count:
                    break
            else:
                break

        except Exception as e:
            print(f"An error occurred: {e}")
            break

    await api.clear()

    if all_candles:
        df = pd.DataFrame(all_candles)
        df = df.drop_duplicates(subset=['epoch']).sort_values('epoch')
        df['datetime'] = pd.to_datetime(df['epoch'], unit='s')
        df = df[['datetime', 'open', 'high', 'low', 'close']]
        return df
    return None

if __name__ == "__main__":
    df = asyncio.run(fetch_large_data())
    if df is not None:
        df.to_csv("r_100_15m_large.csv", index=False)
        print(f"Successfully saved {len(df)} candles to r_100_15m_large.csv")
