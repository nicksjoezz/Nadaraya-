import pandas as pd
import numpy as np
from nwe import nadaraya_watson_non_repainting, nadaraya_watson_repainting
from backtest_fixed_tpsl import run_backtest_fixed_tpsl

def compare_results_fixed(df, h_opt=8.0, mult_opt=1.8):
    src = df['close'].values

    # Optimized Non-Repainting
    out_opt, upper_opt, lower_opt = nadaraya_watson_non_repainting(src, h_opt, mult_opt)
    df['upper_opt'] = upper_opt
    df['lower_opt'] = lower_opt
    wr_opt, pnl_opt, n_opt, dd_opt = run_backtest_fixed_tpsl(df, 'upper_opt', 'lower_opt')

    # Repainting (Final look on the last 1000 bars)
    sub_src = src[-1000:]
    nwe_r, upper_r, lower_r = nadaraya_watson_repainting(sub_src, h_opt, mult_opt)
    df_r = pd.DataFrame({
        'upper_r': upper_r,
        'lower_r': lower_r,
        'datetime': df['datetime'].iloc[-1000:],
        'close': df['close'].iloc[-1000:],
        'open': df['open'].iloc[-1000:],
        'high': df['high'].iloc[-1000:],
        'low': df['low'].iloc[-1000:]
    })
    wr_r, pnl_r, n_r, dd_r = run_backtest_fixed_tpsl(df_r, 'upper_r', 'lower_r')

    print(f"Fixed TP (3%) / SL (1%) Results (Dataset: {len(df)} candles):")
    print(f"Optimized Non-Repainting (h={h_opt}, mult={mult_opt}): WR: {wr_opt:.2f}%, PnL: {pnl_opt:.2%}, Trades: {n_opt}, Max DD: {dd_opt:.2%}")
    print(f"\nRepainting (Final View - Last 1000 candles):")
    print(f"Repainting Results: WR: {wr_r:.2f}%, PnL: {pnl_r:.2%}, Trades: {n_r}")

if __name__ == "__main__":
    import os
    if os.path.exists("r_100_15m_large.csv"):
        df = pd.read_csv("r_100_15m_large.csv")
        compare_results_fixed(df)
    else:
        print("Data file not found. Run fetch_large_data.py first.")
