# Nadaraya-Watson Envelope Optimization (Deriv R_100)

## Overview
This project optimizes the LuxAlgo Nadaraya-Watson Envelope (NWE) indicator for the Deriv Volatility 100 Index (R_100) on the 15-minute timeframe. The primary goal was to address the "repainting" issue of the original indicator and find robust parameters for a mean reversion strategy.

## Repainting vs. Non-Repainting
The original NWE indicator often uses **Kernel Regression** across the entire data window. This means that as new data arrives, the calculations for previous bars are updated to reflect the "best fit" for the new data. This creates a high win rate in backtests that is impossible to achieve in live trading.

### The Solution: End-Point Method
We implemented the **End-Point method** (non-repainting version), where the indicator value for each bar is calculated using *only* historical and current data. This makes the backtest results realistic and tradable.

## Optimization Process
We fetched approximately **20,000 historical 15-minute candles** (the maximum available) from the Deriv API. We then conducted a deep grid search optimization across the following parameters:
- **Bandwidth (h)**: Controls the smoothness of the midpoint.
- **Multiplier (mult)**: Controls the width of the envelope.
- **Stop Loss Multiplier (sl_mult)**: Defines the stop loss based on the current band width.

### Best Parameters Found
| Parameter | Value |
|-----------|-------|
| **Bandwidth (h)** | 8.0 |
| **Multiplier (mult)** | 1.8 |
| **Stop Loss (sl_mult)** | 3.0 |
| **Take Profit** | Midpoint |

## Performance Metrics (Non-Repainting)
On the 20,000 candle dataset (approx. 7 months of data):
- **Win Rate**: 73.08%
- **Total PnL**: 69.44%
- **Total Trades**: 572
- **Max Drawdown**: 31.77%

## Strategy Rules
1. **Entry Long**: Price closes below the lower band.
2. **Entry Short**: Price closes above the upper band.
3. **Take Profit**: Exit when price reaches the midpoint of the envelope.
4. **Stop Loss**: Exit if price goes further beyond the entry point by `3.0 * (upper - lower) / 2`.

## Using the Python Scripts
1. **`fetch_large_data.py`**: Downloads historical data from Deriv API.
2. **`nwe.py`**: Contains the Nadaraya-Watson Envelope logic (both versions).
3. **`backtest_v3.py`**: Contains the mean reversion strategy backtester.
4. **`run_comparison.py`**: Runs a final comparison between the repainting, original non-repainting, and optimized non-repainting versions.

To run the full comparison, use:
```bash
python run_comparison.py
```
