from typing import Protocol, List


class ExecutionException(Exception):
    pass


class ExecutionClient(Protocol):

    def buy(self, product_id: str, amount: int):
        """
        Execute a buy order, throws ExecutionException on failure
        :param product_id: the product to buy
        :param amount: the amount to buy
        :return: None
        """
        raise ExecutionException("Buy execution failed.")

    def sell(self, product_id: str, amount: int):
        """
        Execute a sell order, throws ExecutionException on failure
        :param product_id: the product to sell
        :param amount: the amount to sell
        :return: None
        """
        raise ExecutionException("Sell execution failed.")
