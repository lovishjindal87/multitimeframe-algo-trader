"""
Binance API wrapper for fetching market data and executing trades.
"""

import pandas as pd
from typing import Dict, List, Optional
from binance.spot import Spot
import sys
import os

# Add project root to path for config access
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from config.config import (
    API_KEY, API_SECRET, BINANCE_TESTNET_BASE_URL, 
    SYMBOL, TRADING_INTERVAL_15M, TRADING_INTERVAL_1H
)
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class BinanceExchange:
    """
    Wrapper for Binance Testnet API operations.
    Handles data fetching and order execution.
    """
    
    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None,
                 base_url: Optional[str] = None, symbol: Optional[str] = None):
        """
        Initialize Binance exchange client.
        
        Args:
            api_key: Binance API key (defaults to config)
            api_secret: Binance API secret (defaults to config)
            base_url: Base URL for API (defaults to testnet)
            symbol: Trading symbol (defaults to BTCUSDT)
        """
        self.api_key = api_key or API_KEY
        self.api_secret = api_secret or API_SECRET
        self.base_url = base_url or BINANCE_TESTNET_BASE_URL
        self.symbol = symbol or SYMBOL
        
        if not self.api_key or not self.api_secret:
            raise ValueError("API keys not found. Set BINANCE_API_KEY and BINANCE_API_SECRET in .env file")
        
        self.client = Spot(
            api_key=self.api_key,
            api_secret=self.api_secret,
            base_url=self.base_url
        )
        
        logger.info(f"Connected to Binance Testnet (Symbol: {self.symbol})")
    
    def fetch_candles(self, interval: str, limit: int = 100) -> pd.DataFrame:
        """
        Fetch candlestick data from Binance.
        
        Args:
            interval: Time interval (e.g., '15m', '1h')
            limit: Number of candles to fetch (default: 100)
            
        Returns:
            DataFrame with OHLCV data
        """
        try:
            klines = self.client.klines(
                symbol=self.symbol,
                interval=interval,
                limit=limit
            )
            
            df = pd.DataFrame(
                klines,
                columns=[
                    "open_time", "open", "high", "low", "close",
                    "volume", "close_time", "quote_asset_volume",
                    "num_trades", "taker_buy_base", "taker_buy_quote", "ignore"
                ]
            )
            
            df["close"] = df["close"].astype(float)
            df["open"] = df["open"].astype(float)
            df["high"] = df["high"].astype(float)
            df["low"] = df["low"].astype(float)
            df["volume"] = df["volume"].astype(float)
            df["open_time"] = pd.to_datetime(df["open_time"], unit='ms')
            df.set_index("open_time", inplace=True)
            
            return df
            
        except Exception as e:
            logger.error(f"Error fetching candles: {e}")
            raise
    
    def fetch_15m_candles(self, limit: int = 100) -> pd.DataFrame:
        """Fetch 15-minute candles."""
        return self.fetch_candles(TRADING_INTERVAL_15M, limit)
    
    def fetch_1h_candles(self, limit: int = 100) -> pd.DataFrame:
        """Fetch 1-hour candles."""
        return self.fetch_candles(TRADING_INTERVAL_1H, limit)
    
    def place_market_order(self, side: str, quantity: float) -> Dict:
        """
        Place a market order on Binance.
        
        Args:
            side: 'BUY' or 'SELL'
            quantity: Order quantity
            
        Returns:
            Order response dictionary
        """
        try:
            order = self.client.new_order(
                symbol=self.symbol,
                side=side,
                type="MARKET",
                quantity=quantity
            )
            
            logger.info(f"Order executed: {side} {quantity} {self.symbol}")
            return order
            
        except Exception as e:
            logger.error(f"Error placing order: {e}")
            raise
    
    def get_account_balance(self) -> Dict:
        """
        Get account balance information.
        
        Returns:
            Account balance dictionary
        """
        try:
            account = self.client.account()
            return account
        except Exception as e:
            logger.error(f"Error fetching account balance: {e}")
            raise

