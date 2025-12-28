"""
Backtesting engine for the multi-timeframe trading strategy.
"""

import pandas as pd
from backtesting import Backtest, Strategy
import sys
import os

# Add project root to path for config access
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from config.config import BACKTEST_INITIAL_CASH, BACKTEST_COMMISSION, BACKTEST_TRADES_PATH, FIXED_QUANTITY
from src.strategy.multi_tf import MultiTimeframeStrategy
from src.utils.data import load_historical_data, resample_to_1h, prepare_dataframes_for_strategy
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class BacktestStrategy(Strategy):
    """
    Strategy wrapper for backtesting library.
    Implements the multi-timeframe strategy logic.
    """
    
    def init(self):
        """Initialize strategy for backtesting."""
        self.strategy = MultiTimeframeStrategy()
    
    def next(self):
        """Called on each bar during backtesting."""
        df_15m = self.data.df.iloc[:len(self.data)]
        df_1h = resample_to_1h(df_15m)
        df_15m, df_1h = prepare_dataframes_for_strategy(df_15m, df_1h)
        df_15m, df_1h = self.strategy.compute_indicators(df_15m, df_1h)
        signal, size = self.strategy.generate_signal(df_15m, df_1h, self.position.size)
        
        if signal == "BUY" and self.position.size == 0:
            self.buy(size=0.2)
        elif signal == "SELL" and self.position.size > 0:
            self.position.close()


def run_backtest(data_path: str = None) -> dict:
    """
    Run backtest and save results.
    
    Args:
        data_path: Path to historical data CSV (defaults to config)
        
    Returns:
        Backtest statistics dictionary
    """
    logger.info("Starting backtest...")
    
    try:
        data = load_historical_data(data_path)
        logger.info(f"Loaded {len(data)} bars of historical data")
    except Exception as e:
        logger.error(f"Error loading historical data: {e}")
        raise
    
    bt = Backtest(data, BacktestStrategy, cash=BACKTEST_INITIAL_CASH, commission=BACKTEST_COMMISSION)
    stats = bt.run()
    
    logger.info("Backtest completed")
    logger.info(f"Total Return: {stats['Return [%]']:.2f}%")
    logger.info(f"Sharpe Ratio: {stats['Sharpe Ratio']:.2f}")
    logger.info(f"Max Drawdown: {stats['Max. Drawdown [%]']:.2f}%")
    
    if '_trades' in stats and len(stats['_trades']) > 0:
        trades_df = stats['_trades'][[
            "EntryTime",
            "ExitTime",
            "EntryPrice",
            "ExitPrice"
        ]].copy()
        
        trades_df["Symbol"] = "BTCUSDT"
        trades_df["Side"] = trades_df.apply(
            lambda row: "LONG" if row["EntryPrice"] < row["ExitPrice"] else "SHORT",
            axis=1
        )
        
        trades_df["PnL"] = trades_df.apply(
            lambda row: (row["ExitPrice"] - row["EntryPrice"]) * 0.2,
            axis=1
        )
        
        trades_df = trades_df[
            ["EntryTime", "ExitTime", "Symbol", "Side", "EntryPrice", "ExitPrice", "PnL"]
        ]
        os.makedirs(os.path.dirname(BACKTEST_TRADES_PATH) if os.path.dirname(BACKTEST_TRADES_PATH) else '.', exist_ok=True)
        trades_df.to_csv(BACKTEST_TRADES_PATH, index=False)
        logger.info(f"Saved {len(trades_df)} trades to {BACKTEST_TRADES_PATH}")
    
    return stats


if __name__ == "__main__":
    run_backtest()

