import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Parameters
START_PRICE = 87500
INTERVAL_MIN = 15
DAYS = 7
ROWS = int((24 * 60 / INTERVAL_MIN) * DAYS)

np.random.seed(42)

timestamps = [
    datetime.now() - timedelta(minutes=INTERVAL_MIN * i)
    for i in range(ROWS)
][::-1]

prices = [START_PRICE]

for _ in range(ROWS - 1):
    change = np.random.normal(0, 30)  # realistic BTC volatility
    prices.append(max(1000, prices[-1] + change))

data = []

for i in range(len(prices)):
    open_ = prices[i]
    high = open_ + abs(np.random.normal(20, 10))
    low = open_ - abs(np.random.normal(20, 10))
    close = open_ + np.random.normal(0, 10)
    volume = np.random.uniform(5, 25)

    data.append([
        timestamps[i],
        round(open_, 2),
        round(high, 2),
        round(low, 2),
        round(close, 2),
        round(volume, 2)
    ])

df = pd.DataFrame(
    data,
    columns=["timestamp", "Open", "High", "Low", "Close", "Volume"]
)

df.to_csv("historical_data.csv", index=False)

print("✅ historical_data.csv generated with", len(df), "rows")
