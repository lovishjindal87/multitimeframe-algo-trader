import pandas as pd

class MovingAverageStrategy:
    """
    Stateless, deterministic strategy used for both backtest and live
    """
    
    def __init__(self, sma_15m=20, sma_1h=20):
        self.sma_15m = sma_15m
        self.sma_1h = sma_1h
    
    def compute_indicators(self, df_15m, df_1h):
        """Add moving averages to dataframes"""
        df_15m = df_15m.copy()
        df_1h = df_1h.copy()
        
        df_15m['sma_15m'] = df_15m['close'].rolling(self.sma_15m).mean()
        df_1h['sma_1h'] = df_1h['close'].rolling(self.sma_1h).mean()
        
        return df_15m, df_1h
    
    def generate_signal(self, df_15m, df_1h, current_position=0):
        """
        Returns: ('BUY', quantity) or ('SELL', quantity) or ('HOLD', 0)
        Uses fixed quantity for simplicity
        """
        if len(df_15m) < self.sma_15m or len(df_1h) < self.sma_1h:
            return 'HOLD', 0
        
        latest_15m = df_15m.iloc[-1]
        latest_1h = df_1h.iloc[-1]
        
        # Entry: Long when both timeframes above SMA
        if current_position == 0:
            if (latest_15m['close'] > latest_15m['sma_15m'] and 
                latest_1h['close'] > latest_1h['sma_1h']):
                return 'BUY', 0.001  # Fixed: 0.001 BTC per trade
        
        # Exit: When 15m trend reverses
        elif current_position > 0:
            if latest_15m['close'] < latest_15m['sma_15m']:
                return 'SELL', current_position  # Exit full position
        
        return 'HOLD', 0