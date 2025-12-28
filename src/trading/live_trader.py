"""
Live trading bot that executes the multi-timeframe strategy on Binance Testnet.
"""

import time
import sys
import os

# Add project root to path for config access
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from config.config import TRADING_INTERVAL_15M, TRADING_INTERVAL_1H
from src.strategy.multi_tf import MultiTimeframeStrategy
from src.trading.exchange import BinanceExchange
from src.trading.executor import TradeExecutor
from src.utils.data import prepare_dataframes_for_strategy
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class LiveTrader:
    """
    Main live trading bot that runs the multi-timeframe strategy.
    """
    
    def __init__(self, api_key: str = None, api_secret: str = None):
        """
        Initialize live trader.
        
        Args:
            api_key: Binance API key (defaults to config)
            api_secret: Binance API secret (defaults to config)
        """
        self.exchange = BinanceExchange(api_key=api_key, api_secret=api_secret)
        self.executor = TradeExecutor(self.exchange)
        self.strategy = MultiTimeframeStrategy()
        
        logger.info("Live trading bot initialized")
    
    def run_once(self):
        """Execute one trading cycle."""
        logger.info("\n" + "="*50)
        logger.info("Running trading cycle...")
        
        try:
            # Fetch market data
            df_15m = self.exchange.fetch_15m_candles()
            df_1h = self.exchange.fetch_1h_candles()
            
            if df_15m.empty or df_1h.empty:
                logger.warning("Not enough data available")
                return
            
            logger.info(f"Fetched {len(df_15m)} 15m candles and {len(df_1h)} 1h candles")
            
            df_15m, df_1h = prepare_dataframes_for_strategy(df_15m, df_1h)
            df_15m, df_1h = self.strategy.compute_indicators(df_15m, df_1h)
            current_position = self.executor.get_position()
            signal, quantity = self.strategy.generate_signal(df_15m, df_1h, current_position)
            
            logger.info(f"Current Position: {current_position}")
            logger.info(f"Signal: {signal}, Quantity: {quantity}")
            
            if signal == "BUY" and current_position == 0:
                self.executor.execute_buy(quantity)
            elif signal == "SELL" and current_position > 0:
                self.executor.execute_sell(quantity)
            else:
                logger.info("No action taken (HOLD)")
                
        except Exception as e:
            logger.error(f"Error in trading cycle: {e}", exc_info=True)
    
    def run(self, interval_seconds: int = 60):
        """
        Run the trading bot continuously.
        
        Args:
            interval_seconds: Seconds to wait between trading cycles (default: 60)
        """
        logger.info("Trading bot started")
        logger.info(f"Running every {interval_seconds} seconds")
        logger.info("Press Ctrl+C to stop")
        
        try:
            while True:
                try:
                    self.run_once()
                except Exception as e:
                    logger.error(f"Error in trading cycle: {e}", exc_info=True)

                time.sleep(interval_seconds)
        except KeyboardInterrupt:
            logger.info("\nTrading bot stopped by user")
        except Exception as e:
            logger.error(f"Fatal error: {e}", exc_info=True)


if __name__ == "__main__":
    trader = LiveTrader()
    trader.run()

