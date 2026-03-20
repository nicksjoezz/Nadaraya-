import pandas as pd
import numpy as np

def run_backtest_v3(df, upper_col, lower_col, midpoint_col, sl_mult=2.0, use_trend_filter=False, trend_period=200):
    """
    Mean Reversion Strategy with Trend Filter (EMA 200).
    - Long entry: close < lower band AND close > EMA 200 (optional filter)
    - Short entry: close > upper band AND close < EMA 200 (optional filter)
    """
    df_bt = df.dropna(subset=[upper_col, lower_col, midpoint_col]).copy()

    if use_trend_filter:
        df_bt['ema'] = df_bt['close'].ewm(span=trend_period, adjust=False).mean()
        df_bt = df_bt.dropna(subset=['ema'])

    df_bt['band_width'] = df_bt[upper_col] - df_bt[lower_col]

    trades = []
    position = 0 # 0: None, 1: Long, -1: Short
    entry_price = 0
    sl_price = 0
    tp_price = 0
    entry_time = None

    for i in range(len(df_bt) - 1):
        row = df_bt.iloc[i]
        next_row = df_bt.iloc[i+1]

        if position == 0:
            can_long = row['close'] < row[lower_col]
            can_short = row['close'] > row[upper_col]

            if use_trend_filter:
                # Basic trend filter: only long if above EMA (bullish) or during range
                # Or even better: only long if close is within a certain distance from EMA
                # Let's try: only long if close < lower band and we're not in a strong downtrend
                can_long = can_long and row['close'] > row['ema']
                can_short = can_short and row['close'] < row['ema']

            if can_long:
                position = 1
                entry_price = next_row['open']
                sl_price = entry_price - (row['band_width'] / 2) * sl_mult
                tp_price = row[midpoint_col]
                entry_time = next_row['datetime']
            elif can_short:
                position = -1
                entry_price = next_row['open']
                sl_price = entry_price + (row['band_width'] / 2) * sl_mult
                tp_price = row[midpoint_col]
                entry_time = next_row['datetime']

        elif position == 1:
            if next_row['low'] <= sl_price:
                pnl = (sl_price - entry_price) / entry_price
                trades.append({'entry_time': entry_time, 'exit_time': next_row['datetime'], 'type': 'Long', 'pnl': pnl, 'result': 'SL'})
                position = 0
            elif next_row['high'] >= tp_price:
                pnl = (tp_price - entry_price) / entry_price
                trades.append({'entry_time': entry_time, 'exit_time': next_row['datetime'], 'type': 'Long', 'pnl': pnl, 'result': 'TP'})
                position = 0

        elif position == -1:
            if next_row['high'] >= sl_price:
                pnl = (entry_price - sl_price) / entry_price
                trades.append({'entry_time': entry_time, 'exit_time': next_row['datetime'], 'type': 'Short', 'pnl': pnl, 'result': 'SL'})
                position = 0
            elif next_row['low'] <= tp_price:
                pnl = (entry_price - tp_price) / entry_price
                trades.append({'entry_time': entry_time, 'exit_time': next_row['datetime'], 'type': 'Short', 'pnl': pnl, 'result': 'TP'})
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
    df = pd.read_csv("r_100_15m.csv")
    out, upper, lower = nadaraya_watson_non_repainting(df['close'].values, 7.0, 1.5)
    df['midpoint'] = out
    df['upper'] = upper
    df['lower'] = lower

    print("Backtest WITHOUT Trend Filter:")
    wr, pnl, n, dd = run_backtest_v3(df, 'upper', 'lower', 'midpoint', use_trend_filter=False)
    print(f"WR: {wr:.2f}%, PnL: {pnl:.2%}, Trades: {n}, Max DD: {dd:.2%}")

    print("\nBacktest WITH Trend Filter (EMA 200):")
    wr, pnl, n, dd = run_backtest_v3(df, 'upper', 'lower', 'midpoint', use_trend_filter=True, trend_period=200)
    print(f"WR: {wr:.2f}%, PnL: {pnl:.2%}, Trades: {n}, Max DD: {dd:.2%}")
