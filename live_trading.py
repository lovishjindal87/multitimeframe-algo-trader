import time
import pandas as pd
from binance.spot import Spot
from strategy import MovingAverageStrategy


class LiveTrader:
    def __init__(self, api_key, api_secret):
        self.client = Spot(
            api_key="RKBcA97e4mUA4viXxEsEDvSzU19hr2gpDgRBHZlGkrHLpVz5s199mjnNfBR4ZkJ6",
            api_secret="QWfc5KoCamVvWbzcSEp2C7frvzyPD6hGy9KfVkhU13D40W0iUeXHA610nH6ytWgm",
            base_url="https://testnet.binance.vision"
        )

        self.symbol = "BTCUSDT"
        self.position = 0
        self.strategy = MovingAverageStrategy()

        print("Connected to Binance Testnet")

        # CSV log
        with open("live_trades.csv", "a") as f:
            if f.tell() == 0:
                f.write("timestamp,symbol,side,price,quantity\n")

    def fetch_candles(self, interval, limit=100):
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
        return df

    def log_trade(self, side, price, quantity):
        with open("live_trades.csv", "a") as f:
            f.write(f"{time.time()},{self.symbol},{side},{price},{quantity}\n")

    def place_market_order(self, side, quantity):
        order = self.client.new_order(
            symbol=self.symbol,
            side=side,
            type="MARKET",
            quantity=quantity
        )
        price = float(order["fills"][0]["price"])
        self.log_trade(side, price, quantity)
        print(f"Executed {side} @ {price}")

    def run_once(self):
        print("\nRunning trading cycle...")

        df_15m = self.fetch_candles("15m")
        df_1h = self.fetch_candles("1h")

        if df_15m.empty or df_1h.empty:
            print("Not enough data")
            return

        df_15m, df_1h = self.strategy.compute_indicators(df_15m, df_1h)
        signal, qty = self.strategy.generate_signal(df_15m, df_1h, self.position)

        print("Signal:", signal)

        if signal == "BUY":
            self.place_market_order("BUY", qty)
            self.position += qty

        elif signal == "SELL":
            self.place_market_order("SELL", qty)
            self.position = 0

    def run(self):
        print("🚀 Trading bot started")
        while True:
            self.run_once()
            time.sleep(60)


if __name__ == "__main__":
    API_KEY = "YOUR_API_KEY"
    API_SECRET = "YOUR_SECRET_KEY"

    trader = LiveTrader(API_KEY, API_SECRET)
    trader.run()
