# PyLimitOrders/limit/limit_order_agent.py

from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener

class LimitOrderAgent(PriceListener):
    def __init__(self, execution_client: ExecutionClient) -> None:
        """
        :param execution_client: used to execute buy or sell orders
        """
        super().__init__()
        self.execution_client = execution_client
        self.orders = []

    def add_order(self, side: str, product_id: str, amount: int, limit_price: float):
        """
        Add an order to the agent's order list.
        :param side: 'buy' or 'sell'
        :param product_id: the product id
        :param amount: the amount to buy/sell
        :param limit_price: the limit price to execute the order
        """
        order = {
            "side": side,
            "product_id": product_id,
            "amount": amount,
            "limit_price": limit_price
        }
        self.orders.append(order)

    def on_price_tick(self, product_id: str, price: float):
        """
        Called when a price tick occurs.
        :param product_id: product id for the price tick
        :param price: the updated price of the product
        """
        for order in self.orders[:]:
            if order["product_id"] == product_id:
                if (order["side"] == "buy" and price <= order["limit_price"]) or
                   (order["side"] == "sell" and price >= order["limit_price"]):
                    # Execute the order
                    self.execution_client.execute_order(order["side"], product_id, order["amount"], price)
                    self.orders.remove(order)
