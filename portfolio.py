import pandas as pd
from config import INITIAL_CAPITAL, TICKERS
from logger import setup_logger

logger = setup_logger("PortfolioManager")

class Portfolio:
    def __init__(self):
        self.holdings = {ticker: 0 for ticker in TICKERS}
        self.holdings['CASH'] = INITIAL_CAPITAL
        
    def update_holdings(self, order_execution):
        ticker = order_execution['ticker']
        qty = order_execution['quantity']
        price = order_execution['price']
        cost = qty * price

        self.holdings[ticker] += qty

        self.holdings['CASH'] -= cost
        
        logger.info(f"Ledger Updated: {ticker} | Qty: {qty} | New Cash: {self.holdings['CASH']:.2f}")

    def get_portfolio_state(self, live_prices):
        df = pd.DataFrame(index=TICKERS)
        df['holdings'] = pd.Series(self.holdings)
        df['price'] = live_prices

        df['market_value'] = df['holdings'] * df['price']
        
        total_nav = df['market_value'].sum()

        df['current_weight'] = df['market_value'] / total_nav
        
        return df, total_nav