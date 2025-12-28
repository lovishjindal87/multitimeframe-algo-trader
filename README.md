# Multi-Timeframe Trading Strategy

Python trading system with backtesting and live trading on Binance Testnet.

## Project Overview

Simple algorithmic trading system using historical and live market data. Both backtesting and live trading use the same strategy class to maintain consistency.

## Strategy Logic (High-Level)

Simple Moving Averages on two timeframes:

**Entry:** Long when 15m and 1h close prices are both above their 20-period SMAs  
**Exit:** Close when 15m close drops below 15m SMA  
**Risk:** Fixed 0.001 BTC per trade, one position max, no stops

## Architecture Overview

```
├── config/config.py          # Configuration
├── src/
│   ├── strategy/            # Strategy (used by both backtest & live)
│   ├── backtesting/         # Backtesting engine
│   ├── trading/             # Binance API and execution
│   └── utils/               # Utilities
├── data/                     # Trade logs
├── scripts/generate_data.py  # Generate test data
├── run_backtest.py
└── run_live_trading.py
```

The strategy class is stateless and used by both backtest and live trading.

## How to Run

Install dependencies:
```bash
pip install -r requirements.txt
```

For live trading, you need API keys:
1. Get testnet keys from https://testnet.binance.vision/
2. Copy `.env.example` to `.env`
3. Add your keys to `.env`

Backtesting doesn't need API keys.

Generate test data:
```bash
python scripts/generate_data.py
```

Run backtest:
```bash
python run_backtest.py
```

Run live trading:
```bash
python run_live_trading.py
```

## How Parity Between Backtest and Live Execution Was Ensured

Both backtest and live trading use the same `MultiTimeframeStrategy` class. Same methods, same logic, same entry/exit rules. The strategy lives in one file (`src/strategy/multi_tf.py`) so there's no duplication. Both modes call `compute_indicators()` and `generate_signal()` identically.

Trade logs use the same format so you can compare results directly.

## Trade Logging

Trades are saved to CSV files in `data/`:

- `backtest_trades.csv`: EntryTime, ExitTime, Symbol, Side, EntryPrice, ExitPrice, PnL
- `live_trades.csv`: timestamp, symbol, side, price, quantity, entry_price, exit_price, pnl, metadata

Use `BacktestAnalyzer.compare_with_live()` to compare results.

## Observations from Trade Matching

When given the same market conditions, the strategy generates identical signals in both modes. Entry/exit logic is consistent.

Expected differences: timestamps (historical vs real-time), prices (market moves), trade frequency (volatility), and live execution includes fills/slippage.

Trade direction and entry/exit rules match between backtest and live.

## Notes / Assumptions

- Uses Binance Testnet only
- Simple strategy for clarity
- No stop-loss or take-profit
- Fixed 0.001 BTC position size
- Stateless strategy
- One position at a time
- For evaluation, not production

## Summary

The system uses a single strategy class for both backtesting and live trading, ensuring consistent behavior. Focus is on correctness and system design, not performance.

---

**By LOVISH JINDAL**
