import pandas as pd
import numpy as np
import time
from config import TICKERS

class LiveDataFeed:
    def __init__(self):
        self.prices = {ticker: 1000.0 for ticker in TICKERS}
        self.prices['CASH'] = 1.0 

    def get_live_prices(self):
        for ticker in TICKERS:
            if ticker != 'CASH':
                shock = np.random.uniform(0.995, 1.005) # +/- 0.5% volatility
                self.prices[ticker] *= shock
        
        return pd.Series(self.prices)