#!/usr/bin/env python3
"""
Entry point for running live trading bot.
"""

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.trading.live_trader import LiveTrader

if __name__ == "__main__":
    # API keys can be set via environment variables or config file
    trader = LiveTrader()
    trader.run(interval_seconds=60)

