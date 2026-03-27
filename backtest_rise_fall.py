import pandas as pd
import numpy as np

def run_backtest_rise_fall(df, upper_col, lower_col, expiry=5):
    """
    Rise/Fall (Binary Options style) Mean Reversion Strategy:
    - Long (Rise) entry: close < lower band (at Bar A close, entry at Bar B open)
    - Short (Fall) entry: close > upper band (at Bar A close, entry at Bar B open)
    - Expiry: Result is checked at the close of the 5th candle (Bar B + 4 more).
    """
    df_bt = df.dropna(subset=[upper_col, lower_col]).reset_index(drop=True)

    trades = []
    n = len(df_bt)

    # We iterate until n - expiry because we need future candles for results
    for i in range(n - expiry):
        row = df_bt.iloc[i] # Signal candle (Bar A)
        entry_bar = df_bt.iloc[i + 1] # Entry bar (Bar B)
        exit_bar = df_bt.iloc[i + expiry] # 5th candle (Bar B + 4 more)

        entry_price = entry_bar['open']
        exit_price = exit_bar['close']

        # We can only have one trade at a time to keep it simple,
        # but let's allow overlapping trades if the signal persists.
        # This gives a better "winrate per signal" view.

        if row['close'] < row[lower_col]:
            # Rise (Call)
            win = 1 if exit_price > entry_price else 0
            trades.append({'entry_time': entry_bar['datetime'], 'type': 'Rise', 'win': win})
        elif row['close'] > row[upper_col]:
            # Fall (Put)
            win = 1 if exit_price < entry_price else 0
            trades.append({'entry_time': entry_bar['datetime'], 'type': 'Fall', 'win': win})

    if not trades:
        return 0, 0

    trades_df = pd.DataFrame(trades)
    win_rate = trades_df['win'].mean() * 100
    num_trades = len(trades_df)

    return win_rate, num_trades

if __name__ == "__main__":
    from nwe import nadaraya_watson_non_repainting
    import os
    if os.path.exists("r_100_15m_large.csv"):
        df = pd.read_csv("r_100_15m_large.csv")
        out, upper, lower = nadaraya_watson_non_repainting(df['close'].values, 8.0, 1.8)
        df['upper'] = upper
        df['lower'] = lower

        wr, n = run_backtest_rise_fall(df, 'upper', 'lower')
        print(f"Rise/Fall (5-Candle Expiry) Results: WR: {wr:.2f}%, Trades: {n}")
    else:
        print("Data file not found.")
