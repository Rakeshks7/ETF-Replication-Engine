import pandas as pd
from config import TARGET_WEIGHTS, DRIFT_THRESHOLD, MIN_TRADE_VALUE
from logger import setup_logger

logger = setup_logger("ETF_Engine")

class RebalanceEngine:
    def __init__(self):
        self.target_weights = pd.Series(TARGET_WEIGHTS)

    def calculate_drift(self, portfolio_df, total_nav):
        df = portfolio_df.copy()
        df['target_weight'] = self.target_weights

        df['drift'] = df['target_weight'] - df['current_weight']

        df['is_actionable'] = df['drift'].abs() > DRIFT_THRESHOLD
        
        return df

    def generate_orders(self, drift_df, total_nav):

        orders = []

        actionable_df = drift_df[drift_df['is_actionable']]
        
        for ticker, row in actionable_df.iterrows():
            if ticker == 'CASH': continue 
            
            drift_pct = row['drift']

            trade_value = drift_pct * total_nav

            if abs(trade_value) < MIN_TRADE_VALUE:
                continue
                
            price = row['price']
            qty = int(trade_value / price)
            
            if qty != 0:
                orders.append({
                    'ticker': ticker,
                    'action': 'BUY' if qty > 0 else 'SELL',
                    'quantity': qty, 
                    'abs_qty': abs(qty),
                    'price': price,
                    'reason': f"Drift: {drift_pct*100:.4f}%"
                })
        
        return orders