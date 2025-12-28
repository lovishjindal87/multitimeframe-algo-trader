#!/usr/bin/env python3
"""
Entry point for running backtests.
"""

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.backtesting.backtest import run_backtest
from src.backtesting.analyzer import BacktestAnalyzer

if __name__ == "__main__":
    print("Running backtest...")
    stats = run_backtest()
    
    # Print summary
    analyzer = BacktestAnalyzer()
    analyzer.print_summary()
    
    print("\nBacktest completed successfully!")

