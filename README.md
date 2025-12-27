# Numatix Quant Developer Assignment Submission

## Project Overview
This project implements a simple algorithmic trading system using historical 
and live market data. It includes a backtesting engine and a live trading 
engine that both execute the same strategy logic to ensure consistency.


## Strategy Logic
The strategy is a simple moving-average–based system:
- A long position is opened when the current price crosses above the moving average.
- The position is closed when the price crosses back below the moving average.
- Only one position can be open at a time.
- No leverage or complex risk management is used.
- This logic is intentionally minimal to make behavior easy to verify and compare between backtesting and live execution.

## Architecture Overview
strategy.py        → Contains trading logic and indicator calculations
backtest.py        → Runs historical backtests using Backtesting.py
live_trading.py    → Executes live trades on Binance testnet
historical_data.csv → OHLCV data used for backtesting


## How to run
# Run backtest
python backtest.py
# Run live trading (testnet)
python live_trading.py

## Backtesting & Live Trading Parity
The same strategy logic is used in both modes:
- Backtesting runs on historical OHLCV data
- Live trading consumes real-time market data from Binance Testnet
While timestamps and prices differ due to real-world market movement, the trade logic and signal generation are identical.

## Trade Logging
Trades are logged to CSV files for transparency and validation.
Each trade includes:
- Timestamp
- Symbol
- Trade direction (BUY / SELL)
- Entry price
- Exit price
These logs allow verification that backtest and live execution behave consistently.

## Notes / Assumptions
- Strategy is intentionally simple for clarity and not optimized for profitability.
- No stop-loss or take-profit logic is implemented.
- The system is designed for demonstration and evaluation purposes
- Live trading uses Binance Testnet.

## Summary
This project demonstrates:
- Correct implementation of a trading strategy
- Consistent behavior between backtest and live execution
- Proper data handling and logging
- Clean and modular code structure
The focus is correctness, reproducibility, and system design. It does not represent trading performance
# By LOVISH JINDAL
