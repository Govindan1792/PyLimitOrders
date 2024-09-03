from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener


class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        """

        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        super().__init__()
        self.execution_client = execution_client
        self.orders = []

    def on_price_tick(self, product_id: str, price: float):
        # see PriceListener protocol and readme file
        for order in self.orders[:]:
            if order["product_id"] == product_id:
                if (order["side"] == "buy" and price <= order["limit_price"]) or \
                   (order["side"] == "sell" and price >= order["limit_price"]):
                    self.execution_client.execute_order(order["side"], product_id, order["amount"], price)
                    self.orders.remove(order)
