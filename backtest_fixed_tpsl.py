import pandas as pd
import numpy as np

def run_backtest_fixed_tpsl(df, upper_col, lower_col, tp_pct=0.03, sl_pct=0.01):
    """
    Mean Reversion Strategy with Fixed TP (3%) and SL (1%).
    - Long entry: close < lower band
    - Short entry: close > upper band
    - Exit: Fixed TP or SL based on entry price.
    """
    df_bt = df.dropna(subset=[upper_col, lower_col]).copy()

    trades = []
    position = 0 # 0: None, 1: Long, -1: Short
    entry_price = 0
    sl_price = 0
    tp_price = 0
    entry_time = None

    for i in range(len(df_bt) - 1):
        row = df_bt.iloc[i]
        next_row = df_bt.iloc[i+1] # This is the bar where we enter at 'open'

        if position == 0:
            if row['close'] < row[lower_col]:
                position = 1
                entry_price = next_row['open']
                sl_price = entry_price * (1 - sl_pct)
                tp_price = entry_price * (1 + tp_pct)
                entry_time = next_row['datetime']

                # Check for exit on the SAME bar as entry (Bar B)
                if next_row['low'] <= sl_price:
                    trades.append({'entry_time': entry_time, 'exit_time': next_row['datetime'], 'type': 'Long', 'pnl': -sl_pct, 'result': 'SL'})
                    position = 0
                elif next_row['high'] >= tp_price:
                    trades.append({'entry_time': entry_time, 'exit_time': next_row['datetime'], 'type': 'Long', 'pnl': tp_pct, 'result': 'TP'})
                    position = 0

            elif row['close'] > row[upper_col]:
                position = -1
                entry_price = next_row['open']
                sl_price = entry_price * (1 + sl_pct)
                tp_price = entry_price * (1 - tp_pct)
                entry_time = next_row['datetime']

                # Check for exit on the SAME bar as entry (Bar B)
                if next_row['high'] >= sl_price:
                    trades.append({'entry_time': entry_time, 'exit_time': next_row['datetime'], 'type': 'Short', 'pnl': -sl_pct, 'result': 'SL'})
                    position = 0
                elif next_row['low'] <= tp_price:
                    trades.append({'entry_time': entry_time, 'exit_time': next_row['datetime'], 'type': 'Short', 'pnl': tp_pct, 'result': 'TP'})
                    position = 0

        elif position == 1:
            # Check for SL
            if next_row['low'] <= sl_price:
                trades.append({'entry_time': entry_time, 'exit_time': next_row['datetime'], 'type': 'Long', 'pnl': -sl_pct, 'result': 'SL'})
                position = 0
            # Check for TP
            elif next_row['high'] >= tp_price:
                trades.append({'entry_time': entry_time, 'exit_time': next_row['datetime'], 'type': 'Long', 'pnl': tp_pct, 'result': 'TP'})
                position = 0

        elif position == -1:
            # Check for SL
            if next_row['high'] >= sl_price:
                trades.append({'entry_time': entry_time, 'exit_time': next_row['datetime'], 'type': 'Short', 'pnl': -sl_pct, 'result': 'SL'})
                position = 0
            # Check for TP
            elif next_row['low'] <= tp_price:
                trades.append({'entry_time': entry_time, 'exit_time': next_row['datetime'], 'type': 'Short', 'pnl': tp_pct, 'result': 'TP'})
                position = 0

    if not trades:
        return 0, 0, 0, 0

    trades_df = pd.DataFrame(trades)
    win_rate = (trades_df['pnl'] > 0).mean() * 100
    total_pnl = trades_df['pnl'].sum()
    num_trades = len(trades_df)

    cum_pnl = (1 + trades_df['pnl']).cumprod()
    max_dd = (cum_pnl.cummax() - cum_pnl).max() / cum_pnl.cummax().max() if not cum_pnl.empty else 0

    return win_rate, total_pnl, num_trades, max_dd

if __name__ == "__main__":
    from nwe import nadaraya_watson_non_repainting
    import os
    if os.path.exists("r_100_15m_large.csv"):
        df = pd.read_csv("r_100_15m_large.csv")
        out, upper, lower = nadaraya_watson_non_repainting(df['close'].values, 8.0, 1.8)
        df['upper'] = upper
        df['lower'] = lower
        wr, pnl, n, dd = run_backtest_fixed_tpsl(df, 'upper', 'lower')
        print(f"Fixed TP (3%) / SL (1%) Results: WR: {wr:.2f}%, PnL: {pnl:.2%}, Trades: {n}, Max DD: {dd:.2%}")
    else:
        print("Data file not found.")
