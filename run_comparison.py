import pandas as pd
import numpy as np
from nwe import nadaraya_watson_non_repainting, nadaraya_watson_repainting
from backtest import run_backtest

def compare_results(df, h_orig=8.0, mult_orig=3.0, h_opt=7.0, mult_opt=1.5):
    src = df['close'].values

    # Original Non-Repainting
    out_nr, upper_nr, lower_nr = nadaraya_watson_non_repainting(src, h_orig, mult_orig)
    df['upper_nr'] = upper_nr
    df['lower_nr'] = lower_nr
    wr_nr, pnl_nr, n_nr = run_backtest(df, 'upper_nr', 'lower_nr')

    # Optimized Non-Repainting
    out_opt, upper_opt, lower_opt = nadaraya_watson_non_repainting(src, h_opt, mult_opt)
    df['upper_opt'] = upper_opt
    df['lower_opt'] = lower_opt
    wr_opt, pnl_opt, n_opt = run_backtest(df, 'upper_opt', 'lower_opt')

    # Repainting (Final look on the last 1000 bars)
    sub_src = src[-1000:]
    nwe_r, upper_r, lower_r = nadaraya_watson_repainting(sub_src, h_orig, mult_orig)
    df_r = pd.DataFrame({'upper_r': upper_r, 'lower_r': lower_r, 'datetime': df['datetime'].iloc[-1000:], 'close': df['close'].iloc[-1000:]})
    wr_r, pnl_r, n_r = run_backtest(df_r, 'upper_r', 'lower_r')

    print(f"Results for R_100 (15m):")
    print(f"Original Non-Repainting (h=8.0, mult=3.0): Win Rate: {wr_nr:.2f}%, PnL: {pnl_nr:.2%}, Trades: {n_nr}")
    print(f"Optimized Non-Repainting (h=7.0, mult=1.5): Win Rate: {wr_opt:.2f}%, PnL: {pnl_opt:.2%}, Trades: {n_opt}")
    print(f"Repainting (h=8.0, mult=3.0) - Final State View: Win Rate: {wr_r:.2f}%, PnL: {pnl_r:.2%}, Trades: {n_r}")

if __name__ == "__main__":
    import asyncio
    from fetch_data import fetch_data
    df = asyncio.run(fetch_data())
    if df is not None:
        compare_results(df)
