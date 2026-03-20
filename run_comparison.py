import pandas as pd
import numpy as np
from nwe import nadaraya_watson_non_repainting, nadaraya_watson_repainting
from backtest_v3 import run_backtest_v3

def compare_results(df, h_orig=8.0, mult_orig=3.0, h_opt=8.0, mult_opt=1.8, sl_opt=3.0):
    src = df['close'].values

    # Original Non-Repainting
    out_nr, upper_nr, lower_nr = nadaraya_watson_non_repainting(src, h_orig, mult_orig)
    df['midpoint_nr'] = out_nr
    df['upper_nr'] = upper_nr
    df['lower_nr'] = lower_nr
    wr_nr, pnl_nr, n_nr, dd_nr = run_backtest_v3(df, 'upper_nr', 'lower_nr', 'midpoint_nr', sl_mult=2.0)

    # Optimized Non-Repainting
    out_opt, upper_opt, lower_opt = nadaraya_watson_non_repainting(src, h_opt, mult_opt)
    df['midpoint_opt'] = out_opt
    df['upper_opt'] = upper_opt
    df['lower_opt'] = lower_opt
    wr_opt, pnl_opt, n_opt, dd_opt = run_backtest_v3(df, 'upper_opt', 'lower_opt', 'midpoint_opt', sl_mult=sl_opt)

    # Repainting (Final look on the last 1000 bars)
    sub_src = src[-1000:]
    nwe_r, upper_r, lower_r = nadaraya_watson_repainting(sub_src, h_orig, mult_orig)
    df_r = pd.DataFrame({
        'upper_r': upper_r,
        'lower_r': lower_r,
        'midpoint_r': nwe_r,
        'datetime': df['datetime'].iloc[-1000:],
        'close': df['close'].iloc[-1000:],
        'open': df['open'].iloc[-1000:],
        'high': df['high'].iloc[-1000:],
        'low': df['low'].iloc[-1000:]
    })
    wr_r, pnl_r, n_r, dd_r = run_backtest_v3(df_r, 'upper_r', 'lower_r', 'midpoint_r', sl_mult=2.0)

    print(f"Results for R_100 (15m) - Full Dataset ({len(df)} candles):")
    print(f"Original Non-Repainting: WR: {wr_nr:.2f}%, PnL: {pnl_nr:.2%}, Trades: {n_nr}, Max DD: {dd_nr:.2%}")
    print(f"Optimized Non-Repainting: WR: {wr_opt:.2f}%, PnL: {pnl_opt:.2%}, Trades: {n_opt}, Max DD: {dd_opt:.2%}")
    print(f"\nRepainting (Final View - Last 1000 candles):")
    print(f"Repainting Results: WR: {wr_r:.2f}%, PnL: {pnl_r:.2%}, Trades: {n_r}")

if __name__ == "__main__":
    import os
    if os.path.exists("r_100_15m_large.csv"):
        df = pd.read_csv("r_100_15m_large.csv")
        compare_results(df)
    else:
        print("Data file not found. Run fetch_large_data.py first.")
