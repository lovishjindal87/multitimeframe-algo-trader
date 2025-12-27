import pandas as pd
from backtesting import Backtest, Strategy
from strategy import MovingAverageStrategy

class BacktestStrategy(Strategy):
    def init(self):
        self.strategy = MovingAverageStrategy()

    def next(self):
        # Build 15m dataframe up to current bar
        df_15m = self.data.df.iloc[:len(self.data)]

        # Build 1h dataframe from same window
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

        # Rename to match strategy expectations
        df_15m = df_15m.rename(columns={"Close": "close"})
        df_1h = df_1h.rename(columns={"Close": "close"})

        df_15m, df_1h = self.strategy.compute_indicators(df_15m, df_1h)

        signal, size = self.strategy.generate_signal(df_15m, df_1h, self.position.size)

        if signal == "BUY" and self.position.size == 0:
            self.buy(size=0.2)

        elif signal == "SELL" and self.position.size > 0:
            self.position.close()

def run_backtest():
    """Run and save backtest results"""
    # Load your historical data
    # Note: You need to provide this file
    data = pd.read_csv('historical_data.csv', index_col=0, parse_dates=True)
    
    bt = Backtest(data, BacktestStrategy, cash=1000000, commission=0.001)
    stats = bt.run()

    
    # Save trades
    trades_df = stats['_trades'][[
            "EntryTime",
        "ExitTime",
        "EntryPrice",
        "ExitPrice"
    ]].copy()

    trades_df["Symbol"] = "BTCUSDT"
    trades_df["Side"] = trades_df.apply(
        lambda row: "BUY" if row["EntryPrice"] < row["ExitPrice"] else "SELL",
        axis=1
    )

    # Reorder columns
    trades_df = trades_df[
        ["EntryTime", "ExitTime", "Symbol", "Side", "EntryPrice", "ExitPrice"]
    ]

    trades_df.to_csv("backtest_trades.csv", index=False)

    
    return stats

if __name__ == "__main__":
    run_backtest()