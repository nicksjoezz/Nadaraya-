import pandas as pd
import numpy as np

def run_backtest(df, upper_col, lower_col):
    """
    Mean Reversion Strategy:
    - Long entry: close < lower band
    - Long exit: close >= midpoint
    - Short entry: close > upper band
    - Short exit: close <= midpoint
    """
    df_bt = df.dropna(subset=[upper_col, lower_col]).copy()

    trades = []
    position = 0 # 0: None, 1: Long, -1: Short
    entry_price = 0
    entry_time = None

    for i in range(len(df_bt) - 1):
        row = df_bt.iloc[i]
        next_row = df_bt.iloc[i+1]

        if position == 0:
            if row['close'] < row[lower_col]:
                position = 1
                entry_price = next_row['open']
                entry_time = next_row['datetime']
            elif row['close'] > row[upper_col]:
                position = -1
                entry_price = next_row['open']
                entry_time = next_row['datetime']

        elif position == 1:
            midpoint = (row[upper_col] + row[lower_col]) / 2
            if row['close'] >= midpoint:
                pnl = (next_row['open'] - entry_price) / entry_price
                trades.append({'entry_time': entry_time, 'exit_time': next_row['datetime'], 'type': 'Long', 'pnl': pnl})
                position = 0

        elif position == -1:
            midpoint = (row[upper_col] + row[lower_col]) / 2
            if row['close'] <= midpoint:
                pnl = (entry_price - next_row['open']) / entry_price
                trades.append({'entry_time': entry_time, 'exit_time': next_row['datetime'], 'type': 'Short', 'pnl': pnl})
                position = 0

    if not trades:
        return 0, 0, 0

    trades_df = pd.DataFrame(trades)
    win_rate = (trades_df['pnl'] > 0).mean() * 100
    total_pnl = trades_df['pnl'].sum()
    num_trades = len(trades_df)

    return win_rate, total_pnl, num_trades
