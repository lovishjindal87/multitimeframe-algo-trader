"""
Data handling utilities for loading and processing market data.
"""

import pandas as pd
from typing import Optional
import os
import sys

# Add project root to path for config access
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from config.config import HISTORICAL_DATA_PATH


def load_historical_data(filepath: Optional[str] = None) -> pd.DataFrame:
    """
    Load historical OHLCV data from CSV file.
    
    Args:
        filepath: Path to CSV file (defaults to config HISTORICAL_DATA_PATH)
        
    Returns:
        DataFrame with OHLCV data, indexed by timestamp
    """
    path = filepath or HISTORICAL_DATA_PATH
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"Historical data file not found: {path}")
    
    df = pd.read_csv(path, index_col=0, parse_dates=True)
    
    required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    
    return df


def resample_to_1h(df_15m: pd.DataFrame) -> pd.DataFrame:
    """
    Resample 15-minute data to 1-hour timeframe.
    
    Args:
        df_15m: 15-minute OHLCV dataframe
        
    Returns:
        1-hour OHLCV dataframe
    """
    df_1h = (
        df_15m
        .resample("1h")
        .agg({
            "Open": "first",
            "High": "max",
            "Low": "min",
            "Close": "last",
            "Volume": "sum"
        })
        .dropna()
    )
    
    return df_1h


def prepare_dataframes_for_strategy(df_15m: pd.DataFrame, df_1h: pd.DataFrame) -> tuple:
    """
    Prepare dataframes for strategy.
    
    Args:
        df_15m: 15-minute dataframe
        df_1h: 1-hour dataframe
        
    Returns:
        Tuple of (df_15m, df_1h) with 'close' column
    """
    if 'Close' in df_15m.columns and 'close' not in df_15m.columns:
        df_15m = df_15m.rename(columns={"Close": "close"})
    if 'Close' in df_1h.columns and 'close' not in df_1h.columns:
        df_1h = df_1h.rename(columns={"Close": "close"})
    
    return df_15m, df_1h

