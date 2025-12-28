"""
Base strategy class that defines the interface for all trading strategies.
"""

from abc import ABC, abstractmethod
from typing import Tuple
import pandas as pd


class BaseStrategy(ABC):
    """
    Abstract base class for trading strategies.
    All strategies must implement compute_indicators and generate_signal methods.
    """
    
    @abstractmethod
    def compute_indicators(self, df_15m: pd.DataFrame, df_1h: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Compute technical indicators on the given dataframes.
        
        Args:
            df_15m: 15-minute timeframe dataframe
            df_1h: 1-hour timeframe dataframe
            
        Returns:
            Tuple of (df_15m, df_1h) with indicators added
        """
        pass
    
    @abstractmethod
    def generate_signal(self, df_15m: pd.DataFrame, df_1h: pd.DataFrame, current_position: float = 0) -> Tuple[str, float]:
        """
        Generate trading signal based on current market conditions.
        
        Args:
            df_15m: 15-minute timeframe dataframe with indicators
            df_1h: 1-hour timeframe dataframe with indicators
            current_position: Current position size (positive for long, 0 for no position)
            
        Returns:
            Tuple of (signal, quantity) where:
            - signal: 'BUY', 'SELL', or 'HOLD'
            - quantity: Position size to trade (0 for HOLD)
        """
        pass

