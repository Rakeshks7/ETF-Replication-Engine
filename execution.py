from logger import setup_logger

logger = setup_logger("Execution")

class ExecutionHandler:
    def execute_orders(self, orders, portfolio):
        if not orders:
            return
            
        logger.info(f"--- EXECUTING {len(orders)} ORDERS ---")
        
        for order in orders:
            fill_price = order['price'] 
            
            logger.info(f"ORDER SENT: {order['action']} {order['abs_qty']} {order['ticker']} @ {fill_price:.2f} | {order['reason']}")

            execution_report = {
                'ticker': order['ticker'],
                'quantity': order['quantity'],
                'price': fill_price
            }
            portfolio.update_holdings(execution_report)