"""
Trade execution logic for live trading.
Handles order placement and trade logging.
"""

import time
from typing import Optional
import sys
import os

# Add project root to path for config access
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from config.config import SYMBOL, LIVE_TRADES_PATH
from src.trading.exchange import BinanceExchange
from src.utils.logger import setup_logger, log_trade_to_csv

logger = setup_logger(__name__)


class TradeExecutor:
    """
    Handles trade execution and logging for live trading.
    """
    
    def __init__(self, exchange: BinanceExchange):
        """
        Initialize trade executor.
        
        Args:
            exchange: BinanceExchange instance
        """
        self.exchange = exchange
        self.symbol = exchange.symbol
        self.position = 0.0
        self.entry_price = 0.0
        
        # Initialize trade log file
        self._init_trade_log()
    
    def _init_trade_log(self):
        """Initialize trade log directory."""
        os.makedirs(os.path.dirname(LIVE_TRADES_PATH) if os.path.dirname(LIVE_TRADES_PATH) else '.', exist_ok=True)
    
    def execute_buy(self, quantity: float) -> Optional[float]:
        """
        Execute a buy order and log the trade.
        
        Args:
            quantity: Quantity to buy
            
        Returns:
            Execution price if successful, None otherwise
        """
        try:
            order = self.exchange.place_market_order("BUY", quantity)
            
            if order and "fills" in order and len(order["fills"]) > 0:
                price = float(order["fills"][0]["price"])
                executed_qty = float(order["fills"][0]["qty"])
                
                self.position += executed_qty
                if self.entry_price == 0:
                    self.entry_price = price
                else:
                    total_value = (self.position - executed_qty) * self.entry_price + executed_qty * price
                    self.entry_price = total_value / self.position
                
                # Log trade
                log_trade_to_csv(
                    LIVE_TRADES_PATH,
                    time.time(),
                    self.symbol,
                    'BUY',
                    price,
                    executed_qty,
                    entry_price=price,
                    exit_price=None,
                    pnl=None,
                    metadata={'order_id': order.get('orderId')}
                )
                
                logger.info(f"BUY executed: {executed_qty} {self.symbol} @ {price}")
                return price
            else:
                logger.error("Order executed but no fills found")
                return None
                
        except Exception as e:
            logger.error(f"Error executing BUY order: {e}")
            return None
    
    def execute_sell(self, quantity: float) -> Optional[float]:
        """
        Execute a sell order and log the trade.
        
        Args:
            quantity: Quantity to sell
            
        Returns:
            Execution price if successful, None otherwise
        """
        try:
            order = self.exchange.place_market_order("SELL", quantity)
            
            if order and "fills" in order and len(order["fills"]) > 0:
                price = float(order["fills"][0]["price"])
                executed_qty = float(order["fills"][0]["qty"])
                
                pnl = (price - self.entry_price) * executed_qty if self.entry_price > 0 else 0
                log_trade_to_csv(
                    LIVE_TRADES_PATH,
                    time.time(),
                    self.symbol,
                    'SELL',
                    price,
                    executed_qty,
                    entry_price=self.entry_price,
                    exit_price=price,
                    pnl=pnl,
                    metadata={'order_id': order.get('orderId')}
                )
                
                self.position = max(0, self.position - executed_qty)
                if self.position == 0:
                    self.entry_price = 0.0
                
                logger.info(f"SELL executed: {executed_qty} {self.symbol} @ {price} (PnL: {pnl:.2f})")
                return price
            else:
                logger.error("Order executed but no fills found")
                return None
                
        except Exception as e:
            logger.error(f"Error executing SELL order: {e}")
            return None
    
    def get_position(self) -> float:
        """Get current position size."""
        return self.position
    
    def reset_position(self):
        """Reset position tracking (for testing/debugging)."""
        self.position = 0.0
        self.entry_price = 0.0

