# Nadaraya-Watson Envelope Optimization (Deriv R_100) - Fixed TP/SL

## Overview
This project optimizes the LuxAlgo Nadaraya-Watson Envelope (NWE) indicator for the Deriv Volatility 100 Index (R_100) on the 15-minute timeframe, specifically targeting a mean reversion strategy with fixed Take Profit (TP) and Stop Loss (SL).

## Repainting vs. Non-Repainting
The original PineScript NWE repaints, meaning it uses future data points to calculate the "best-fit" line for historical bars. This creates a high win rate in backtests that cannot be replicated in live trading.

### The Solution: End-Point Method
We implemented the **End-Point method** in Python, which ensures that for each bar, the indicator is calculated using *only* historical and current data. This makes the performance results realistic and tradable.

## Strategy Rules (Fixed TP/SL)
- **Entry Long**: Price closes below the lower band.
- **Entry Short**: Price closes above the upper band.
- **Take Profit (TP)**: Fixed at **3.0%** from the entry price.
- **Stop Loss (SL)**: Fixed at **1.0%** from the entry price.

## Optimization Results
Using approximately **20,000 historical 15-minute candles**, we found the following optimal indicator parameters for the fixed 3% TP and 1% SL rules:

| Parameter | Value |
|-----------|-------|
| **Bandwidth (h)** | 8.0 |
| **Multiplier (mult)** | 1.8 |

### Performance Metrics (Non-Repainting)
- **Win Rate**: 26.36% (This is consistent for a 3:1 Reward-to-Risk ratio)
- **Total PnL**: +65.0%
- **Total Trades**: 1,199
- **Max Drawdown**: 46.85%

*Note: While the win rate may seem low, the 3:1 Reward-to-Risk ratio (3% TP / 1% SL) makes the strategy highly profitable overall.*

## Comparison with Repainting
The repainting version (on the last 1,000 bars) shows a win rate of **65.96%**, which is more than double the realistic win rate of **26.36%**. This illustrates why the original indicator seems "too good to be true" and why this non-repainting optimization is essential.

## Using the Python Scripts
1. **`fetch_large_data.py`**: Downloads historical data from Deriv API.
2. **`nwe.py`**: Core Nadaraya-Watson Envelope logic (Repainting and Non-Repainting).
3. **`backtest_fixed_tpsl.py`**: Strategy engine with fixed 3% TP and 1% SL.
4. **`run_comparison_fixed.py`**: Final comparison between realistic and repainting performance.
5. **`optimize_fixed.py`**: Script to re-run the parameter optimization.
