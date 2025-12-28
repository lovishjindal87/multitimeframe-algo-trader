"""
Configuration settings for the trading system.
"""

import os
from typing import Optional

# Load .env file if python-dotenv is available
try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except ImportError:
    pass

# Binance Testnet API Configuration
BINANCE_TESTNET_BASE_URL = "https://testnet.binance.vision"

# API Keys - Load from environment variables for security
API_KEY: Optional[str] = os.getenv("BINANCE_API_KEY")
API_SECRET: Optional[str] = os.getenv("BINANCE_API_SECRET")

# Trading Configuration
SYMBOL = "BTCUSDT"
TRADING_INTERVAL_15M = "15m"
TRADING_INTERVAL_1H = "1h"

# Strategy Parameters
SMA_15M_PERIOD = 20
SMA_1H_PERIOD = 20
FIXED_QUANTITY = 0.001  # BTC per trade

# Backtesting Configuration
BACKTEST_INITIAL_CASH = 1000000
BACKTEST_COMMISSION = 0.001

# Data Paths
DATA_DIR = "data"
HISTORICAL_DATA_PATH = os.path.join(DATA_DIR, "historical_data.csv")
BACKTEST_TRADES_PATH = os.path.join(DATA_DIR, "backtest_trades.csv")
LIVE_TRADES_PATH = os.path.join(DATA_DIR, "live_trades.csv")

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

