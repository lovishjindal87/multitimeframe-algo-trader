"""
Utility script to generate synthetic historical OHLCV data for backtesting.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add project root to path for config access
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from config.config import HISTORICAL_DATA_PATH

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

df.set_index("timestamp", inplace=True)
os.makedirs(os.path.dirname(HISTORICAL_DATA_PATH) if os.path.dirname(HISTORICAL_DATA_PATH) else '.', exist_ok=True)
df.to_csv(HISTORICAL_DATA_PATH)

print(f"{HISTORICAL_DATA_PATH} generated with {len(df)} rows")

