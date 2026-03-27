import pandas as pd
import numpy as np
from nwe import nadaraya_watson_non_repainting
from backtest_fixed_tpsl import run_backtest_fixed_tpsl

def optimize_fixed_tpsl():
    if not os.path.exists("r_100_15m_large.csv"):
        print("Run fetch_large_data.py first.")
        return
    df = pd.read_csv("r_100_15m_large.csv")
    src = df['close'].values

    h_values = [7, 8, 9, 10, 11]
    mult_values = [1.5, 1.8, 2.0, 2.2, 2.5]

    best_pnl = -np.inf
    best_params = {}

    print("Starting optimization with Fixed TP (3%) / SL (1%)...")

    for h in h_values:
        out_nr, _, _ = nadaraya_watson_non_repainting(src, h, 1.0)
        abs_diff = np.abs(src - out_nr)
        sma_abs_diff = pd.Series(abs_diff).rolling(window=499, min_periods=1).mean().values

        for mult in mult_values:
            df['upper'] = out_nr + sma_abs_diff * mult
            df['lower'] = out_nr - sma_abs_diff * mult

            wr, pnl, n, dd = run_backtest_fixed_tpsl(df, 'upper', 'lower')

            if pnl > best_pnl:
                best_pnl = pnl
                best_params = {'h': h, 'mult': mult, 'wr': wr, 'pnl': pnl, 'dd': dd, 'n': n}
                print(f"New Best: {best_params}")

    print(f"\nOptimization Complete. Best: {best_params}")

if __name__ == "__main__":
    import os
    optimize_fixed_tpsl()
