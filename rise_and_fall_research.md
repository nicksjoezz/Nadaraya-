# Nadaraya-Watson Envelope Research: Rise and Fall (5-Candle Expiry)

## Overview
This section covers our research into using the Nadaraya-Watson Envelope (NWE) for Binary Options (Rise/Fall) trading on the Deriv R_100 (15m) index.

## Rise/Fall Strategy Rules
- **Entry**: Signal occurs on Bar A close (Price > Upper or Price < Lower). Trade is placed at the **Open of Bar B**.
- **Expiry**: The result is determined at the **Close of the 5th candle** (Bar B + 4 more).
- **Result**:
  - **Rise (Call)**: Win if Close of 5th candle > Open of 1st candle.
  - **Fall (Put)**: Win if Close of 5th candle < Open of 1st candle.

## Research Findings
Using approximately **10,000 candles**, we tested various parameters for the non-repainting NWE to find the highest win rate for this 5-candle expiry.

### Best Parameters for Rise/Fall
| Parameter | Value |
|-----------|-------|
| **Bandwidth (h)** | 9.0 |
| **Multiplier (mult)** | 1.5 |

### Performance Metrics
- **Win Rate**: 50.38%
- **Total Signals**: 2,364

### Analysis
The results show a win rate very close to **50%**, which indicates that on its own, the NWE indicator at a 5-candle expiry acts similarly to a random entry for binary options on the R_100 index.

Compared to the **Mean Reversion (3% TP / 1% SL)** strategy, which achieved a **65% total PnL**, the Rise/Fall approach with a fixed time expiry is significantly less effective.

## Comparison Table
| Strategy | Expiry/Exit | Win Rate | Profitability |
|----------|-------------|----------|---------------|
| **Mean Reversion** | Fixed TP (3%) / SL (1%) | 26.4% | **High (65% PnL)** |
| **Binary Rise/Fall** | Fixed 5 Candles | 50.4% | **Break-even / Low** |

## Conclusion
For trading the Nadaraya-Watson Envelope on Deriv R_100 (15m), we **strongly recommend the Mean Reversion strategy with a 3:1 Reward-to-Risk ratio** over a fixed-time Rise/Fall strategy.
