"""
Multi-timeframe trading strategy implementation.
Combines 15-minute entries with 1-hour confirmations using moving averages.
"""

from typing import Tuple
import pandas as pd
from .base import BaseStrategy
import sys
import os

# Add project root to path for config access
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from config.config import SMA_15M_PERIOD, SMA_1H_PERIOD, FIXED_QUANTITY


class MultiTimeframeStrategy(BaseStrategy):
    """
    Multi-timeframe strategy that uses:
    - 15-minute timeframe for entry signals
    - 1-hour timeframe for trend confirmation
    - Simple Moving Averages (SMA) for both timeframes
    """
    
    def __init__(self, sma_15m: int = SMA_15M_PERIOD, sma_1h: int = SMA_1H_PERIOD):
        """
        Initialize the multi-timeframe strategy.
        
        Args:
            sma_15m: Period for 15-minute SMA (default: 20)
            sma_1h: Period for 1-hour SMA (default: 20)
        """
        self.sma_15m = sma_15m
        self.sma_1h = sma_1h
    
    def compute_indicators(self, df_15m: pd.DataFrame, df_1h: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Add moving averages to both timeframes.
        
        Args:
            df_15m: 15-minute timeframe dataframe
            df_1h: 1-hour timeframe dataframe
            
        Returns:
            Tuple of (df_15m, df_1h) with SMA indicators added
        """
        df_15m = df_15m.copy()
        df_1h = df_1h.copy()
        
        df_15m['sma_15m'] = df_15m['close'].rolling(self.sma_15m).mean()
        df_1h['sma_1h'] = df_1h['close'].rolling(self.sma_1h).mean()
        
        return df_15m, df_1h
    
    def generate_signal(self, df_15m: pd.DataFrame, df_1h: pd.DataFrame, current_position: float = 0) -> Tuple[str, float]:
        """
        Generate trading signal.
        
        Entry: Long when both 15m and 1h close > SMA
        Exit: Close when 15m close < SMA
        
        Args:
            df_15m: 15-minute dataframe
            df_1h: 1-hour dataframe
            current_position: Current position size
            
        Returns:
            (signal, quantity) tuple
        """
        if len(df_15m) < self.sma_15m or len(df_1h) < self.sma_1h:
            return 'HOLD', 0
        
        latest_15m = df_15m.iloc[-1]
        latest_1h = df_1h.iloc[-1]
        
        if current_position == 0:
            if (latest_15m['close'] > latest_15m['sma_15m'] and 
                latest_1h['close'] > latest_1h['sma_1h']):
                return 'BUY', FIXED_QUANTITY
        
        elif current_position > 0:
            if latest_15m['close'] < latest_15m['sma_15m']:
                return 'SELL', current_position
        
        return 'HOLD', 0

