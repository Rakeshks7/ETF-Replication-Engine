import unittest
import pandas as pd
from portfolio import Portfolio
from strategy import RebalanceEngine
from config import TICKERS

class TestETFEngine(unittest.TestCase):
    
    def setUp(self):
        self.portfolio = Portfolio()
        self.engine = RebalanceEngine()
        
        # Mock Prices: Everything is 100.0, Cash is 1.0
        self.mock_prices = pd.Series({t: 100.0 for t in TICKERS})
        self.mock_prices['CASH'] = 1.0

    def test_nav_accounting(self):
        self.portfolio.holdings['RELIANCE'] = 10
        self.portfolio.holdings['CASH'] = 5000

        df, total_nav = self.portfolio.get_portfolio_state(self.mock_prices)
        
        self.assertEqual(total_nav, 6000.0, "NAV Calculation Error: Assets do not match Equity.")

    def test_drift_calculation_logic(self):
        
        df, total_nav = self.portfolio.get_portfolio_state(self.mock_prices)
        drift_df = self.engine.calculate_drift(df, total_nav)
        
        reliance_drift = drift_df.loc['RELIANCE', 'drift']
        
        self.assertAlmostEqual(reliance_drift, 0.10, places=4, msg="Drift logic failed.")

    def test_order_generation_threshold(self):
        df, total_nav = self.portfolio.get_portfolio_state(self.mock_prices)

        df['drift'] = 0.0001 
        df['is_actionable'] = False 
        
        orders = self.engine.generate_orders(df, total_nav)

        self.assertEqual(len(orders), 0, "Engine generated orders for noise/dust trades.")

    def test_buy_signal(self):
        df, total_nav = self.portfolio.get_portfolio_state(self.mock_prices)

        drift_df = self.engine.calculate_drift(df, total_nav)

        orders = self.engine.generate_orders(drift_df, total_nav)

        reliance_order = next((o for o in orders if o['ticker'] == 'RELIANCE'), None)
        
        self.assertIsNotNone(reliance_order, "No order generated for Reliance.")
        self.assertEqual(reliance_order['action'], "BUY", "Engine sold when it should have bought.")

if __name__ == '__main__':
    unittest.main()