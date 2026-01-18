import time
import pandas as pd
from data_feed import LiveDataFeed
from portfolio import Portfolio
from strategy import RebalanceEngine
from execution import ExecutionHandler
from logger import setup_logger

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.float_format', '{:.4f}'.format)

logger = setup_logger("Main")

def run_etf_engine():
    feed = LiveDataFeed()
    portfolio = Portfolio()
    engine = RebalanceEngine()
    broker = ExecutionHandler()
    
    logger.info("Starting ETF Replication Engine...")
    logger.info("Press Ctrl+C to stop.")

    try:
        while True:

            live_prices = feed.get_live_prices()

            portfolio_state, total_nav = portfolio.get_portfolio_state(live_prices)

            drift_analysis = engine.calculate_drift(portfolio_state, total_nav)

            orders = engine.generate_orders(drift_analysis, total_nav)

            if orders:
                broker.execute_orders(orders, portfolio)
                # Re-print state after trading
                portfolio_state, total_nav = portfolio.get_portfolio_state(live_prices)

            print("\n" + "="*50)
            print(f"NAV: INR {total_nav:,.2f}")
            print("-" * 50)
            view_cols = ['price', 'current_weight', 'target_weight', 'drift']
            print(drift_analysis[view_cols])
            print("="*50)

            time.sleep(5)
            
    except KeyboardInterrupt:
        logger.info("Engine Shutdown Requested.")
        print("Final Portfolio State Saved.")

if __name__ == "__main__":
    run_etf_engine()