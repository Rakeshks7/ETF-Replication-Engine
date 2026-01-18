ETF_NAME = "Nifty50_Tracker_Fund"
INITIAL_CAPITAL = 10_000_000  

DRIFT_THRESHOLD = 0.0005  
MIN_TRADE_VALUE = 1000    

TARGET_WEIGHTS = {
    'RELIANCE': 0.10,
    'HDFCBANK': 0.09,
    'ICICIBANK': 0.08,
    'INFY': 0.06,
    'TCS': 0.05,
    'CASH': 0.62 
}

TICKERS = list(TARGET_WEIGHTS.keys())