"""
Backtest results analysis and reporting utilities.
"""

import pandas as pd
from typing import Dict, Optional
import sys
import os

# Add project root to path for config access
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from config.config import BACKTEST_TRADES_PATH, LIVE_TRADES_PATH
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class BacktestAnalyzer:
    """
    Analyzes backtest results and provides statistics.
    """
    
    def __init__(self, trades_path: Optional[str] = None):
        """
        Initialize analyzer.
        
        Args:
            trades_path: Path to backtest trades CSV (defaults to config)
        """
        self.trades_path = trades_path or BACKTEST_TRADES_PATH
    
    def load_trades(self) -> pd.DataFrame:
        """
        Load trades from CSV file.
        
        Returns:
            DataFrame with trade data
        """
        if not os.path.exists(self.trades_path):
            logger.warning(f"Trades file not found: {self.trades_path}")
            return pd.DataFrame()
        
        df = pd.read_csv(self.trades_path)
        
        # Convert timestamps if present
        if 'EntryTime' in df.columns:
            df['EntryTime'] = pd.to_datetime(df['EntryTime'])
        if 'ExitTime' in df.columns:
            df['ExitTime'] = pd.to_datetime(df['ExitTime'])
        
        return df
    
    def calculate_statistics(self) -> Dict:
        """
        Calculate backtest statistics.
        
        Returns:
            Dictionary with statistics
        """
        trades = self.load_trades()
        
        if trades.empty:
            return {
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'win_rate': 0,
                'total_pnl': 0,
                'average_pnl': 0,
                'max_win': 0,
                'max_loss': 0,
                'profit_factor': 0
            }
        
        # Basic statistics
        total_trades = len(trades)
        
        if 'PnL' in trades.columns:
            winning_trades = len(trades[trades['PnL'] > 0])
            losing_trades = len(trades[trades['PnL'] < 0])
            win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
            
            total_pnl = trades['PnL'].sum()
            average_pnl = trades['PnL'].mean()
            max_win = trades['PnL'].max()
            max_loss = trades['PnL'].min()
            
            # Profit factor
            gross_profit = trades[trades['PnL'] > 0]['PnL'].sum()
            gross_loss = abs(trades[trades['PnL'] < 0]['PnL'].sum())
            profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0
        else:
            winning_trades = 0
            losing_trades = 0
            win_rate = 0
            total_pnl = 0
            average_pnl = 0
            max_win = 0
            max_loss = 0
            profit_factor = 0
        
        return {
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': win_rate,
            'total_pnl': total_pnl,
            'average_pnl': average_pnl,
            'max_win': max_win,
            'max_loss': max_loss,
            'profit_factor': profit_factor
        }
    
    def print_summary(self):
        """Print a formatted summary of backtest results."""
        stats = self.calculate_statistics()
        
        print("\n" + "="*50)
        print("BACKTEST RESULTS SUMMARY")
        print("="*50)
        print(f"Total Trades:        {stats['total_trades']}")
        print(f"Winning Trades:      {stats['winning_trades']}")
        print(f"Losing Trades:       {stats['losing_trades']}")
        print(f"Win Rate:            {stats['win_rate']:.2f}%")
        print(f"Total PnL:           ${stats['total_pnl']:.2f}")
        print(f"Average PnL:         ${stats['average_pnl']:.2f}")
        print(f"Max Win:             ${stats['max_win']:.2f}")
        print(f"Max Loss:            ${stats['max_loss']:.2f}")
        print(f"Profit Factor:       {stats['profit_factor']:.2f}")
        print("="*50 + "\n")
    
    def compare_with_live(self, live_trades_path: Optional[str] = None) -> Dict:
        """
        Compare backtest results with live trading results.
        
        Args:
            live_trades_path: Path to live trades CSV (defaults to config)
            
        Returns:
            Dictionary with comparison statistics
        """
        backtest_trades = self.load_trades()
        live_path = live_trades_path or LIVE_TRADES_PATH
        
        if not os.path.exists(live_path):
            logger.warning(f"Live trades file not found: {live_path}")
            return {}
        
        live_trades = pd.read_csv(live_path)
        
        comparison = {
            'backtest_trades': len(backtest_trades),
            'live_trades': len(live_trades),
            'backtest_pnl': backtest_trades['PnL'].sum() if 'PnL' in backtest_trades.columns else 0,
            'live_pnl': live_trades['pnl'].sum() if 'pnl' in live_trades.columns else 0
        }
        
        return comparison

