#!/usr/bin/env python3
"""
Utility script to compare backtest and live trades.
"""

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.backtesting.analyzer import BacktestAnalyzer

if __name__ == "__main__":
    print("="*60)
    print("TRADE COMPARISON: Backtest vs Live Trading")
    print("="*60)
    
    analyzer = BacktestAnalyzer()
    
    # Print backtest summary
    print("\n Backtest Results:")
    analyzer.print_summary()
    
    # Compare with live
    print("\n Live Trading Comparison:")
    comparison = analyzer.compare_with_live()
    
    if comparison:
        print(f"Backtest Trades: {comparison.get('backtest_trades', 0)}")
        print(f"Live Trades:     {comparison.get('live_trades', 0)}")
        print(f"Backtest PnL:    ${comparison.get('backtest_pnl', 0):.2f}")
        print(f"Live PnL:        ${comparison.get('live_pnl', 0):.2f}")
        
        if comparison.get('backtest_trades', 0) > 0 and comparison.get('live_trades', 0) > 0:
            trade_ratio = comparison.get('live_trades', 0) / comparison.get('backtest_trades', 1)
            print(f"\nTrade Ratio (Live/Backtest): {trade_ratio:.2f}")
            if 0.8 <= trade_ratio <= 1.2:
                print("Trade counts are closely matched!")
            else:
                print("Trade counts differ significantly (expected due to market conditions)")
    else:
        print("Live trades file not found or empty")
    
    print("="*60)

